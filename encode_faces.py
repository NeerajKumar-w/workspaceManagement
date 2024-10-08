from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
imagePaths = list(paths.list_images("./dataset"))
print(imagePaths)
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    print(imagePath)
    name = imagePath.split(os.path.sep)[-2]
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

data = {"encodings": knownEncodings, "names": knownNames}
f = open("./encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
