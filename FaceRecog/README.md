# Face recognition

## Usage
From the directory `FaceRecog`, run this command to train the model on the pictures in the directory `training_faces`:

`"venv/scripts/python.exe" quickstart.py train` 
The training pictures should have the format `<name>_<number>.jpg`
Make sure you are the only face in the picture.  The model is stored in the cloud so you only need to retrain it if you are adding new pictures.


From the directory `FaceRecog`, run this command to identify who is in the picture:

`"venv/scripts/python.exe" quickstart.py <filename>` 