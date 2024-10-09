from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

data = pickle.loads(open("./encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier("./haarcascade_frontal_default.xml")

rasp_ip = '192.168.0.108'
url = f'http://{rasp_ip}:5000/video_feed'

vs = cv2.VideoCapture(url)
time.sleep(2.0)

fps = FPS().start()

names = set()
while True:
    ret,frame = vs.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                      minNeighbors=5,
                                      minSize=(30, 30))
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        if(name != "unknown"):
            names.add(name)
        else:
            continue
    for((top, right, bottom, left) , name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top -15 if top -15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(5) & 0xFF
    if key == ord("q"):
        break
    fps.update()
print(names)
f = open('./attendance/presentees.txt', 'w')
for name in names:
    f.write(f'{name}\n')

