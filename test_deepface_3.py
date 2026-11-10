from deepface import DeepFace
import os
import cv2

print("Running representation build...")
# Force DeepFace to build representations
try:
    # Use a blank image just to trigger DB build
    blank = cv2.imread(os.path.join("dataset_fast", "ansh_images", os.listdir(os.path.join("dataset_fast", "ansh_images"))[0]))
    DeepFace.find(img_path=blank, db_path="dataset_fast", model_name="Facenet", enforce_detection=False)
except Exception as e:
    print(e)
