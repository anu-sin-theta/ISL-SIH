import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("inventory-students-firebase-adminsdk-l7t2b-2de4da153b.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://inventory-students-default-rtdb.firebaseio.com/'
})
ref1 = db.reference('lightStatus')
# ref2 = db.reference('fanStatus')


while True:
    print(ref1.get())
    ref1.set("ON")

