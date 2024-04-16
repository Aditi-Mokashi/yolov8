import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import re

def insert_to_realtime_db():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://eqw-violationeye-default-rtdb.firebaseio.com/'
    })

    with open('output.txt', 'r') as file:
        data = file.read()
        number_plate = re.findall('[A-Z]{2}\\d{2}[A-Z]{2}\\d{4}', data)

    # Get a reference to the 'number_plates' node in the database
    ref = db.reference()

    # Store the data in the database
    current_timestamp = time.time()
    number_plate_ref = ref.child('number_plates')
    data = ','.join(str(n) for n in number_plate)
    number_plate_ref.set(data)

    return "Data stored successfully", 200
