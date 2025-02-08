import firebase_admin
from firebase_admin import credentials, firestore

collection_name = "project"

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("../projects-talking-firebase-adminsdk-fbsvc-1de3cff566.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore service
db = firestore.client()

# Function to add a document to a collection
def add_document():
    try:
        doc_ref = db.collection(collection_name).add({
            'birc': {
              "field1": "value1",
              "field2": "value2",
              "field3": "value3"
            }
        })
        print("Document added with ID: ", doc_ref[1].id)
    except Exception as e:
        print("Error adding document: ", e)

# Call the function to add a document
add_document()