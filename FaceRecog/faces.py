import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import re

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'my-unique-person-group'

def train_group():

    # Used for the Snapshot and Delete Person Group examples.
    TARGET_PERSON_GROUP_ID = str(uuid.uuid4())  # assign a random ID (or name it anything)

    '''
    Create the PersonGroup
    '''
    # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
    print('Person group:', PERSON_GROUP_ID)
    face_client.person_group.delete(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

    simon = face_client.person_group_person.create(PERSON_GROUP_ID, "Simon")
    chris = face_client.person_group_person.create(PERSON_GROUP_ID, "Chris")
    andreas = face_client.person_group_person.create(PERSON_GROUP_ID, "Andreas")
    savvas = face_client.person_group_person.create(PERSON_GROUP_ID, "Savvas")

    names_to_ids = {"simon": simon.person_id, "chris": chris.person_id, "andreas": andreas.person_id,
                    "savvas": savvas.person_id}

    '''
    Detect faces and register to correct person
    '''
    # Find all jpeg images of friends in working directory
    images = glob.glob('training_faces/*.jpg')
    print(images)

    name_re = '([a-z]*)_[0-9]'

    for image in images:
        w = open(image, 'r+b')
        name = re.search(name_re, w.name).group(1)
        print("training on a photo of " + name)
        person_id = names_to_ids[name]
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person_id, w)

    '''
    Train PersonGroup
    '''
    print()
    print('Training the person group...')
    # Train the person group
    face_client.person_group.train(PERSON_GROUP_ID)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)

# train_group()

def who_is_it(filename):
    image = open(filename, 'r+b')

    # Detect faces
    face_ids = []
    faces = face_client.face.detect_with_stream(image)
    for face in faces:
        face_ids.append(face.face_id)

    # Identify faces
    if not face_ids:
        return ""
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    #print('Identifying faces in {}'.format(os.path.basename(image.name)))
    """if not results:
        print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
    for person in results:
        print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id,
                                                                                          os.path.basename(image.name),
                                                                                          person.candidates[
                                                                                              0].confidence))  # Get topmost confidence score
                                                                                              """
    if not results:
        return ""
    id = (results[0].candidates[0].person_id)
    return face_client.person_group_person.get(PERSON_GROUP_ID, id).name

def are_they_the_same_person(filename1, filename2):
    image1 = open(filename1, 'r+b')
    image2 = open(filename2, 'r+b')

    # Detect faces
    face_id1 = face_client.face.detect_with_stream(image1)[0].face_id
    face_id2 = face_client.face.detect_with_stream(image2)[0].face_id

    verify_result_same = face_client.face.verify_face_to_face(face_id1, face_id2)
    return verify_result_same.is_identical
    """print('Faces from {} & {} are of the same person, with confidence: {}'
          .format(filename1, filename2, verify_result_same.confidence)
          if verify_result_same.is_identical
          else 'Faces from {} & {} are of a different person, with confidence: {}'
          .format(filename1, filename2, verify_result_same.confidence))"""


def main():
    filename = sys.argv[1]
    if filename == "train":
        train_group()
        quit()
    print(who_is_it(filename))

if __name__ == "__main__":
    main()
