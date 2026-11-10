import cv2
import os
import numpy as np
import pickle

def train_model(dataset_path="dataset", model_dir="models"):
    print("=" * 50)
    print("  LBPH Face Recognizer Training")
    print("=" * 50)
    
    if not hasattr(cv2, 'face'):
        print("ERROR: opencv-contrib-python not installed!")
        return

    # Use LBPH with default params - the large real dataset provides enough variation
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(face_cascade_path)

    names = {}
    current_id = 0

    # First pass: build name mapping
    for directory in sorted(os.listdir(dataset_path)):
        person_path = os.path.join(dataset_path, directory)
        if os.path.isdir(person_path) and not directory.startswith('.'):
            name = directory.replace("_images", "").replace("_image", "").title()
            names[current_id] = name
            current_id += 1

    id_map = {v: k for k, v in names.items()}
    
    faces = []
    face_labels = []
    
    print(f"\nScanning dataset: {dataset_path}")
    print(f"Found {len(names)} people: {list(names.values())}\n")

    for directory in sorted(os.listdir(dataset_path)):
        person_path = os.path.join(dataset_path, directory)
        if not os.path.isdir(person_path) or directory.startswith('.'):
            continue
            
        person_name = directory.replace("_images", "").replace("_image", "").title()
        if person_name not in id_map:
            continue
        
        label_id = id_map[person_name]
        img_count = 0
        
        for file in os.listdir(person_path):
            if not file.lower().endswith(('.jpg', '.png', '.jpeg')):
                continue
                
            path = os.path.join(person_path, file)
            img = cv2.imread(path)
            if img is None:
                continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            detected = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            if len(detected) == 0:
                continue
            
            # ONLY use the LARGEST face per image (most likely the actual person)
            # This prevents background faces from being mislabeled
            largest = max(detected, key=lambda r: r[2] * r[3])
            x, y, w, h = largest
            
            face_roi = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            faces.append(face_resized)
            face_labels.append(label_id)
            img_count += 1
        
        print(f"  {person_name}: {img_count} training samples")

    if len(faces) == 0:
        print("\nERROR: No faces found!")
        return

    print(f"\nTotal training samples: {len(faces)}")
    print("Training LBPH Recognizer (this may take a minute)...")
    
    recognizer.train(faces, np.array(face_labels))

    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "model.yml")
    recognizer.save(model_path)
    
    names_path = os.path.join(model_dir, "names.pkl")
    with open(names_path, 'wb') as f:
        pickle.dump(names, f)
        
    print(f"\nModel saved to: {model_path}")
    print(f"Names saved to: {names_path}")
    print(f"Mapping: {names}")
    print("\nTraining complete!")

if __name__ == "__main__":
    train_model()
