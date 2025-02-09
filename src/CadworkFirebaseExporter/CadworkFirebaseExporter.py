# import modules
import  sys            
import os                     
import  utility_controller as uc
import cadwork as cw 
import element_controller as ec 
import visualization_controller as vc
import dimension_controller as dc
import menu_controller as mc
import attribute_controller as ac
import bim_controller as bim
import shop_drawing_controller as sd
import menu_controller as mec
USERPROFIL = uc.get_3d_userprofil_path()   
# appending a path
sys.path.append(USERPROFIL + '\\api.x64\\CadworkFirebaseExporter\\venv31\\Lib\\site-packages')
import firebase_admin
from firebase_admin import firestore, credentials

# you need to have a venv31 in the CW APIx64 folder where you installed the firebase_admin module
# for this you need to make the venv with the same python version as of cadwork 3.10


import logging


PROJECTS = 'projects'
PARTS = 'parts'

TEST_PROJECT_NAME = 'hackathon_test'
TEST_PROJECT_GUID = 'b029a9b6-4c39-4b57-806a-65335185d063'
TEST_PROJECT_PART_GUIDS = [
    '139f2a63-bbf7-4c46-a6c9-cdda14e7349e',
    '33555ad1-0326-4da5-a2bf-7106eba243d4'
]

# Step 2: Initialize Firebase Admin SDK
cred_path = USERPROFIL + '\\api.x64\\CadworkFirebaseExporter\\projects-talking-firebase-config.json'


cred = credentials.Certificate(cred_path)

if len(firebase_admin._apps.keys()) == 0:
  firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()


def main():
  # get folder to export IFC files in form user 
  export_dir_path = get_user_desktop_path()
  # create log file and start logging
  logger = set_up_logger(export_dir_path)
  projects = fetch_all_projects()
  
  cw_prj,cw_prj_guid = get_cw_project_data()
  exists,prj_id = check_if_project_exists(cw_prj,projects)
  if exists:
    logger.info("Project already exists")
  else:
    prj_id = create_project(cw_prj[1],cw_prj[0])
    logger.info("Project created")
  
  # get user input which user attribute to use for container IFC AssemblyElement export
  # user_id = uc.get_user_int("Enter User Attribute ID to use for sorting parts into clipboards:")
  # if user_id == None or user_id == 0:
  #     logger.error('User Attribute ID not provided. Exiting.')
  #     uc.print_error('User Attribute ID not provided. Exiting.')
  #     return
  # logger.info('Export runs for User Attribute ID: %s'%(user_id))
  # get all elements and sort them by the chosen user attribute into a dict
  element_dict = get_all_elements_sort_by_subgroup()
  logger.info('Found %s clipboard groups to export.'%(len(element_dict.keys())))



  # prepare the progress bar
  count = len(element_dict.keys())
  progress_bar_portion = int(100/count)
  uc.show_progress_bar()

  all_parts = fetch_all_parts()
  # for each container export the container element to IFC
  for i,key in enumerate(sorted(element_dict.keys())):
      element_ids = element_dict[key]
      for element_id in element_ids:
        if check_if_part_exists(element_id,all_parts)[0] == True:
            logger.info("Part already exists in Firebase")
            continue
        else:
            part_dict = create_cw_element_part_dict(element_id,prj_id)
            create_part(part_dict)
            logger.info("Part created in Firebase")

      uc.update_progress_bar(progress_bar_portion*(i+1))
      logger.info("Exported grp %s ESZ to clipboard: %s"%(key,i+1))
  uc.hide_progress_bar()
  logger.info('FINISHED:'+'Exported %s ESZ to clipboards'%(count))
  # uc.print_message('Exported %s ESZ to clipboard to'%(count))    
  logging.shutdown()
  return

def create_cw_element_part_dict(id,prj_guid):
   part_dict = {}
   cw_dict = {}
   part_dict["project_id"] = prj_guid
   cw_dict["cw_id"] = id
   name = ac.get_name(id)
   cw_dict["name"] = name
   mat = ac.get_element_material_name(id)
   cw_dict["material"] = mat
   print(ac.get_user_attribute_count())
   for i in range(ac.get_user_attribute_count()):
      value = ac.get_user_attribute(id,i)
      if value == None or len(value) == 0:
         continue
      key = ac.get_user_attribute_name(i)
      cw_dict[key] = value

   part_dict["cw_attributes"] = cw_dict
   return part_dict

def create_part(part_dict, attrs: dict = None):
    doc_ref = db.collection(PARTS).document()
    id = doc_ref.id
    part_dict["id"] = id
    if attrs:
      part_dict.update(attrs)
    doc_ref.set(part_dict)
    return


def get_user_desktop_path():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop

def fetch_all_projects():
  projects = db.collection(PROJECTS).stream()
  return [project for project in projects]

def fetch_all_parts():
    parts = db.collection(PARTS).stream()
    return [parts for parts in parts]

def fetch_all_parts_and_select():
  all_parts = fetch_all_parts()
   
  cw_ids = []
  for i,part in enumerate(all_parts):
      part_dict = part.to_dict()
      cw_attributes = part_dict.get("cw_attributes")
      cw_id = int(cw_attributes.get('cw_id'))
      if vc.is_selectable(cw_id):
        for i in range(ac.get_user_attribute_count()):
           if ac.get_user_attribute_name(i) in cw_attributes.keys():
              up_value = cw_attributes.get(ac.get_user_attribute_name(i))
              if up_value != ac.get_user_attribute(cw_id,i):
                 ac.set_user_attribute([cw_id],i,up_value)

      cw_ids.append(int(cw_id))
    
  vc.set_active(cw_ids)

def get_cw_project_data():
  cw_prj_name = uc.get_project_name()
  cw_prj_guid = uc.get_project_guid()
  return cw_prj_name, cw_prj_guid

def find_project_by_guid(guid):
    projects = db.collection(PROJECTS).where(u'guid', u'==', guid).stream()
    return [project for project in projects]

def check_if_project_exists(cw_prj,exiting_fb_prjs):
  does_exist = False
  id = None
  for fb_prj in exiting_fb_prjs:
    prj_dict = fb_prj.to_dict()
    if not "name" in prj_dict.keys():
      continue
    if prj_dict['name'] == cw_prj:
      does_exist = True
      id = prj_dict['id']
      break
  print("Does exist: %s, ID: %s"%(does_exist,id))
  return does_exist,id

def check_if_part_exists(cw_part_id,exiting_fb_parts):
  does_exist = False
  id = None
  for fb_part in exiting_fb_parts:
    prj_dict = fb_part.to_dict()
    if not "cw_id" in prj_dict.get("cw_attributes").keys():
      continue
    if prj_dict.get("cw_attributes").get('cw_id') == cw_part_id:
      does_exist = True
      id = prj_dict['id']
      break
  print("Part Exists: %s, ID: %s"%(does_exist,id))

  return does_exist,id

def create_project(guid, name, attrs: dict = None):
    doc_ref = db.collection(PROJECTS).document()
    id = doc_ref.id
    project_data = {"guid": guid,
                    "id": id,
                    "name": name,
                    "duedate": "27.02.2025"}
    if attrs:
        project_data.update(attrs)
    doc_ref.set(project_data)
    return id

def get_all_elements_sort_by_subgroup(attribute_number=6):
    # element_ids = ec.get_visible_identifiable_element_ids()
    element_ids = ec.get_active_identifiable_element_ids()
    if len(element_ids) == 0:
       uc.print_error("No elements selected. Please select elements and try again.")
    element_dict = {}
    for element_id in element_ids:
        sub_grp_str = ac.get_user_attribute(element_id,attribute_number)
        # sub_grp_str = ac.get_subgroup(element_id)
        if len(sub_grp_str) == 0:
            continue
        if sub_grp_str not in element_dict.keys():
            element_dict[sub_grp_str] = []
        element_dict[sub_grp_str].append(element_id)
    return element_dict

def set_up_logger(dir_path):
  logger = logging.getLogger("Hackabout")
  logger.setLevel(logging.INFO)
  fh = logging.FileHandler(dir_path+'/' + 'Hackabout.log')
  fh.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  logger.addHandler(fh)
  logger.info("STARTED")
  return logger

def menu_bar():
  menu_options = 'Projects Talking', '⬆ Upload Parts', '⬇ Fetch Parts',

  while True:
      menu = mec.display_simple_menu(menu_options)

      if menu == menu_options[0]:
          return

      elif menu == menu_options[1]:
          main()
          return

      elif menu == menu_options[2]:
          fetch_all_parts_and_select()
          return

      elif menu == 'Return':
          break
  return


if __name__ == '__main__':
  menu_bar()