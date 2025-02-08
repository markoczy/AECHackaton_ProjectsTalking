# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

import firebase_admin
from firebase_admin import firestore, credentials

from CONFIG import *

# Step 2: Initialize Firebase Admin SDK
cred = credentials.Certificate("./projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()

def find_project_by_name(name):
  projects = db.collection(PROJECTS).where(u'name', u'==', name).stream()
  return [project for project in projects]

def find_project_by_guid(guid):
  projects = db.collection(PROJECTS).where(u'guid', u'==', guid).stream()
  return [project for project in projects]

def find_part_by_guid(guid):
  parts = db.collection(PARTS).where(u'guid', u'==', guid).stream()
  return [part for part in parts]

def delete_prject_by_guid(guid):
  projects = find_project_by_guid(guid)
  for project in projects:
    project.reference.delete()

def create_project(guid, attrs: dict = None):
  doc_ref = db.collection(PROJECTS).document()
  id = doc_ref.id
  project_data = {
    u'guid': guid,
    u'id': id
  }
  if attrs:
    project_data.update(attrs)
  doc_ref.set(project_data)
  return find_project_by_guid(guid)[0]

def create_part(guid, attrs: dict = None):
  doc_ref = db.collection(PARTS).document()
  id = doc_ref.id
  part_data = {
      u'guid': guid,
      u'id': id
  }
  if attrs:
    part_data.update(attrs)
  doc_ref.set(part_data)
  return find_part_by_guid(guid)[0]

def delete_part_by_guid(guid):
  parts = db.collection(PARTS).where(u'guid', u'==', guid).stream()
  for part in parts:
    part.reference.delete()

def get_or_create_project(guid):
  projects = find_project_by_guid(guid)
  if projects:
    log.info(f'Found project with guid: {guid}')
    return projects[0]
  else:
    log.info(f'Creating project with guid: {guid}')
    create_project(guid)
    return find_project_by_guid(guid)[0]

def fetch_all_projects():
  projects = db.collection(PROJECTS).stream()
  return [project for project in projects]


def delete_all_projects():
  projects = db.collection(PROJECTS).stream()
  for project in projects:
    project.reference.delete()

def get_project_name(id):
  project = db.collection(PROJECTS).document(id).get()
  return project.to_dict()['name']

def set_project_name(project_id, name):
  log.info(f'Setting name for project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'name': name
  })

def add_cam_data(project_id, cam_data):
  log.info(f'Adding cam data to project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'cam_data': cam_data
  })

def set_project_guid(project_id, guid):
  log.info(f'Setting guid for project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'guid': guid
  })

# Use this function to (re-)generate test data
def generate_test_data():
  delete_prject_by_guid(TEST_PROJECT_GUID)
  project = create_project(TEST_PROJECT_GUID, {u'name': TEST_PROJECT_NAME})
  project_data = project.to_dict()
  for part_guid in TEST_PROJECT_PART_GUIDS:
    delete_part_by_guid(part_guid)
    create_part(part_guid, {u'project_guid': project_data['guid']})

if __name__ == '__main__':
  # delete_prject_by_guid(TEST_PROJECT_GUID)
  # project = create_project(TEST_PROJECT_GUID, {u'name': TEST_PROJECT_NAME})
  # # set_project_name(project.id, TEST_PROJECT_NAME)

  # cam_data = {
  #   u'est_production_time_ms': 123456,
  #   u'load': 1,
  #   u'reverse': 0,
  # }
  # add_cam_data(project.id, cam_data)

  generate_test_data()
  project = get_or_create_project(TEST_PROJECT_GUID)
  print(project.to_dict())

  # # iterate TEST_PART_GUIDS and create parts
  # for part_guid in TEST_PROJECT_PART_GUIDS:
  #   delete_part_by_guid(part_guid)
  #   create_part(part_guid, {u'project_guid': project.to_dict()['guid']})


  # print(project_data['cam_data'])