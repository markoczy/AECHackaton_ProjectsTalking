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

    doc_ref.set({"name": name, "id": id})


def fetch_all_projects():
    projects = db.collection(PROJECTS).stream()
    return [project for project in projects]


def fetch_all_project_names():
    projects = fetch_all_projects()
    for i in projects:
        print(i.to_dict())


if __name__ == "__main__":
    # create_project("blaaaaaaa")
    fetch_all_project_names()
