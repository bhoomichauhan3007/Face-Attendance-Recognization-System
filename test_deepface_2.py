import cv2
from deepface import DeepFace
import os

img_path = os.path.join("dataset_fast", "ansh_images", os.listdir(os.path.join("dataset_fast", "ansh_images"))[0])
print(f"Testing on {img_path}")

img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_detector.detectMultiScale(gray, 1.1, 5)

if len(faces) > 0:
    x, y, w, h = faces[0]
    face_crop = img[y:y+h, x:x+w]
    print("Cropped face. Running DeepFace.find...")
    try:
        dfs = DeepFace.find(img_path=face_crop, db_path="dataset_fast", model_name="Facenet", enforce_detection=False, silent=True)
        print("Result:", dfs)
    except Exception as e:
        print("Error:", e)
else:
    print("No face detected in reference image by Haar cascade!")

