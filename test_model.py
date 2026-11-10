import cv2
import pickle
import os

# Load model & names
MODEL_PATH = "models/model.yml"
NAMES_PATH = "models/names.pkl"
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

print("=== CHECKING MODEL ===")
print(f"Model exists: {os.path.exists(MODEL_PATH)}")
print(f"Names exists: {os.path.exists(NAMES_PATH)}")
print(f"cv2.face available: {hasattr(cv2, 'face')}")

with open(NAMES_PATH, 'rb') as f:
    names = pickle.load(f)
print(f"\nNames mapping: {names}")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

face_detector = cv2.CascadeClassifier(CASCADE_PATH)

# Test against every person's first image in dataset
print("\n=== TESTING PREDICTIONS ===")
for folder in os.listdir("dataset"):
    folder_path = os.path.join("dataset", folder)
    if not os.path.isdir(folder_path):
        continue
    
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not images:
        continue
    
    img_path = os.path.join(folder_path, images[0])
    img = cv2.imread(img_path)
    if img is None:
        print(f"  Could not read: {img_path}")
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        # Try more lenient detection
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20))
    
    if len(faces) == 0:
        print(f"  {folder}: NO FACE DETECTED in {images[0]}")
        continue
    
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    
    id_pred, confidence = recognizer.predict(face_roi)
    predicted_name = names.get(id_pred, "???")
    
    print(f"  {folder} -> Predicted: {predicted_name} (id={id_pred}, confidence={confidence:.1f})")
