# Step 1: Install required libraries
# Run this command in your terminal
# pip install firebase-admin

import firebase_admin
from firebase_admin import credentials, firestore
import base64
import argparse

# Step 1: Parse command line arguments
parser = argparse.ArgumentParser(description='Send a file as base64 string to Firestore.')
parser.add_argument('projectID', type=str, help='The project ID for the Firestore document.')
parser.add_argument('partID', type=str, help='The part ID for the Firestore document.')
parser.add_argument('filePath', type=str, help='The path to the file to be sent.')
args = parser.parse_args()

# Step 2: Initialize Firebase Admin SDK
# cred = credentials.Certificate('path/to/serviceAccountKey.json')
# firebase_admin.initialize_app(cred)
firebase_admin.initialize_app()

# Step 3: Connect to Firestore
db = firestore.client()

# Step 4: Read and encode file
file_path = args.filePath
with open(file_path, 'rb') as file:
    file_content = file.read()
    encoded_string = base64.b64encode(file_content).decode('utf-8')

doc_ref = db.collection('projects').document(args.projectID)
doc = doc_ref.get()

if doc.exists:
    data = doc.to_dict()
    parts = data.get('parts', {})
    part = parts.get(args.partID, {})
    attributes = part.get('attributes', {})
    attributes['iso_code'] = encoded_string
    part['attributes'] = attributes
    parts[args.partID] = part
    doc_ref.update({'parts': parts})
    print("File content sent to Firestore successfully.")
else:
    print(f"Document with projectID {args.projectID} does not exist.")