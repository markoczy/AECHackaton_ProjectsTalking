# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin

import firebase_admin
from firebase_admin import firestore, credentials

from CONFIG import PROJECTS
from CONFIG import PARTS

# Step 2: Initialize Firebase Admin SDK
cred = credentials.Certificate("./src/LignocamFirebaseExporter/projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

# Step 3: Connect to Firestore
db = firestore.client()


def create_project(guid, name, date, attrs: dict = None):
    doc_ref = db.collection(PROJECTS).document()
    id = doc_ref.id
    project_data = {"guid": guid,
                    "id": id,
                    "name": name,
                    "duedate": date}
    if attrs:
        project_data.update(attrs)
    doc_ref.set(project_data)


def find_project_by_guid(guid):
    projects = db.collection(PROJECTS).where(u'guid', u'==', guid).stream()
    return [project for project in projects]


def delete_prject_by_guid(guid):
    projects = find_project_by_guid(guid)
    for project in projects:
        project.reference.delete()


def update_duedate(guid, date):
    doc_ref = db.collection(PROJECTS).where('guid', '==', guid).stream()
    for doc in doc_ref:
        doc.reference.update({'duedate': date})
    print(f"Updated 'duedate' for GUID: {guid}")


def fetch_all_projects():
    projects = db.collection(PROJECTS).stream()
    return [project for project in projects]


def fetch_all_parts():
    parts = db.collection(PARTS).stream()
    return [parts for parts in parts]


def fetch_all_project_names():
    projects = fetch_all_projects()
    for i in projects:
        print(i.to_dict())


def fetch_all_part_names():
    projects = fetch_all_parts()
    for i in projects:
        print(i.to_dict())


def creat_column(guid, columnname, value):
    doc_ref = db.collection(PROJECTS).where('guid', '==', guid).stream()
    for doc in doc_ref:
        doc_dict = doc.to_dict()
        if columnname not in doc_dict:
            doc.reference.update({columnname: value})
            print(f"Added field for GUID: {guid}")
        else:
            print(f"field already exists for GUID: {guid}")


if __name__ == "__main__":
    # create_project("QGkOUVLZNqNhRpkXFjXd", "EFH Maienfeld")
    # update_duedate("QGkOUVLZNqNhRpkXFjXd", '03.03.2025')
    # delete_prject_by_guid("EFH Maienfeld")
    creat_column("QGkOUVLZNqNhRpkXFjXd", "materialstatus", "Ordered")
    fetch_all_project_names()
