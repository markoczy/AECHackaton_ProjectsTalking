# reading-a-project.py

import firebase_admin
from firebase_admin import credentials, firestore

# Use a service account
cred = credentials.Certificate("./projects-talking-firebase-config.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_object(collection_name, doc_id):
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print('No such document!')

# Example usage
fetch_object('project', 'bric')
