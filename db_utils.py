import firebase_admin
from firebase_admin import credentials, firestore, db
import re

def insert_to_realtime_db(email: str):
    try:
        cred = credentials.Certificate("serviceAccountsKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://eqw-violationeye-42382-default-rtdb.firebaseio.com/',
            'storageBucket': 'eqw-violationeye-42382.appspot.com'
        })

        # cred = credentials.Certificate("path/to/serviceAccountKey.json")
        # firebase_admin.initialize_app(cred)

        with open('output.txt', 'r') as file:
            data = file.read()
            number_plate = re.findall('[A-Z]{2}\\d{2}[A-Z]{2}\\d{4}', data)

        user_name = re.sub('@.*','',email)

        # Get a reference to the 'number_plates' node in the database
        ref = db.reference().child(user_name).child('pending')

        number_plate_ref = ref.child('number_plates')
        data = ','.join(str(n) for n in set(number_plate))
        number_plate_ref.set(data)
        timestamps = ref.get()

        # save video to firestore
        firestore_db = firestore.client()

        # Save video to Firestore
        with open('assets/uploaded_video.mp4', 'rb') as video_file:
            video_data = video_file.read()

        video_ref = firestore_db.collection(u'videos').document()
        file_name = f'{user_name}_{video_ref.id}.mp4'
        video_ref.set({
            u'video_data': firebase_admin.firestore.Blob(video_data),
            u'video_name': file_name
        })

        # Get the download URL of the video file from Firestore
        video_url = video_ref.get().get('video_name')


        # Iterate over each key in the timestamps dictionary and check if it has a child 'number_plates'
        for timestamp in timestamps:
            timestamp_ref = ref.child(timestamp)
            if not timestamp_ref.get().get('number_plates'):
                number_plate_ref = timestamp_ref.child('number_plates')
                data = ','.join(str(n) for n in set(number_plate))
                number_plate_ref.set(data)
                video_ref_realtime = timestamp_ref.push()
                video_ref_realtime.set({
                    'video_url': video_url,
                    'video_name': file_name
                })
                break

        return "Data stored successfully", 200
    except Exception as e:
        print(f"{e.args}")