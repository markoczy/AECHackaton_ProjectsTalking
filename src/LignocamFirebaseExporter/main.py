# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin

import firebase_admin
from firebase_admin import firestore, credentials

from CONFIG import PROJECTS

# Step 2: Initialize Firebase Admin SDK
cred = credentials.Certificate("./projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()


def create_project(name):
  doc_ref = db.collection(PROJECTS).document()

  # assigning the id
  id = doc_ref.id

  doc_ref.set({
    u'name': name,
    u'id': id
  })

def fetch_all_projects():
  projects = db.collection(PROJECTS).stream()
  return [project for project in projects]


if __name__ == '__main__':
  create_project('blaaaaaaa')
  print(fetch_all_projects())