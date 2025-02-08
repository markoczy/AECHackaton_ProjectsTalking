# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin

import firebase_admin
from firebase_admin import firestore, credentials

from CONFIG import PROJECTS


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

# Step 2: Initialize Firebase Admin SDK
cred = credentials.Certificate("./projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()

def find_project_by_name(name):
  projects = db.collection(PROJECTS).where(u'name', u'==', name).stream()
  return [project for project in projects]

def create_project(name):
  doc_ref = db.collection(PROJECTS).document()

  # assigning the id
  id = doc_ref.id

  doc_ref.set({
    u'name': name,
    u'id': id
  })

def get_or_create_project(name):
  projects = find_project_by_name(name)
  if projects:
    log.info(f'Found project with name: {name}')
    return projects[0]
  else:
    log.info(f'Creating project with name: {name}')
    create_project(name)
    return find_project_by_name(name)[0]

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

def add_cam_data(project_id, cam_data):
  log.info(f'Adding cam data to project: {project_id}')
  project_ref = db.collection(PROJECTS).document(project_id)
  project_ref.update({
    u'cam_data': cam_data
  })


if __name__ == '__main__':
  project = get_or_create_project('lignocam_test')
  cam_data = {
    'est_production_time_ms': 123456,
    'load': 1,	
  }
  add_cam_data(project.id, cam_data)

  project = get_or_create_project('lignocam_test')
  project_data = project.to_dict()
  print(project_data['cam_data'])