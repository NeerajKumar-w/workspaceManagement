import cv2
import os

student_name = input("Enter student_name in lowercase without space")

cam = cv2.VideoCapture(0)
output_dir = f'./dataset/{student_name}/'
os.makedirs(output_dir, exist_ok=True)

images = []
while True:
    ret, frame = cam.read()
    cv2.imshow('Camera', frame)
    images.append(frame)
    if(len(images) >= 20):
        break

count = 0
for image in images:
    output_path = os.path.join(output_dir, f'{student_name}_{count:04d}.png')
    cv2.imwrite(output_path, image)
    count += 1    

cam.release()
cv2.destroyAllWindows()
