import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from firebase_admin import storage

#from google.cloud import storage

def send_to_token():
    send_to_token_param("MilkMan", "1574189290000", "015214-19012020", "Milk")

def send_to_token_param(culprit, time, image_location, item_stolen):
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = str(open("registrationToken.txt").readline())
    registration_token = "eyh7nfi4Ues:APA91bHenf3lRmwCjX2E_mc4HJasUB3tdabEUO8ThBVBFXK0E0NTHwO_n-3XpJ7Xu3ngBdH3WJVasJujZofa05HAWHWGD6bRS1jaMQZLcwaMCl6B11c_vAkDSqqdSmdRkN3LgXpjtmcE"

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'culprit': culprit,
            'time': time,
            'imageLocation': image_location,
            'itemStolen': item_stolen,
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]



if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('certificate.json') 
    default_app = firebase_admin.initialize_app(cred, 
    {'storageBucket': 'smartfridge-e5619.appspot.com'})

bucket = storage.bucket(name=None, app=None)

def upload_blob(bucket, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


#print(bucket)

#upload_blob(bucket, "img.jpg", "testBlob")
#send_to_token()
