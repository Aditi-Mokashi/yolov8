import firebase_admin
from firebase_admin import credentials, firestore, db, storage
import re


def insert_to_realtime_db(email: str):
    cred = credentials.Certificate("serviceAccountsKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://eqw-violationeye-42382-default-rtdb.firebaseio.com/',
        'storageBucket': 'eqw-violationeye-42382.appspot.com'
    })

    with open('output.txt', 'r') as file:
        data = file.read()
        number_plate = re.findall('[A-Z]{2}\\d{2}[A-Z]{2}\\d{4}', data)

    user_name = re.sub('@.*','',email)

    # Get a reference to the 'number_plates' node in the database
    ref = db.reference().child(user_name).child('pending')

    # Store number plates and video metadata in Realtime Database
    timestamps = ref.get()
    data = ','.join(str(n) for n in set(number_plate))

    for timestamp in timestamps:
        timestamp_ref = ref.child(timestamp)
        if 'number_plates' not in timestamp_ref.get():
            # Upload video to Firebase Storage
            bucket = storage.bucket()
            print(str(timestamp))
            file_name = f'{user_name}_{str(timestamp)}.mp4'
            with open('assets/uploaded_video.mp4', 'rb') as video_file:
                video_blob = bucket.blob(file_name)
                video_blob.upload_from_file(video_file)
                video_blob.make_public()

            # Get the download URL of the video file from Firebase Storage
            video_url = video_blob.public_url
            timestamp_ref.update({
                'number_plates': data,
                'video_name': file_name,
                'video_url': video_url
            })

    return "Data stored successfully", 200