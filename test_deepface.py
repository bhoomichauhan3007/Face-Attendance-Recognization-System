from deepface import DeepFace
import time
import os

print("Testing DeepFace build...")
start = time.time()
try:
    # Just take 1 image to find
    img_path = os.path.join("dataset", "ansh_images", "IMG-20260318-WA0000.jpg")
    dfs = DeepFace.find(img_path=img_path, db_path="dataset", enforce_detection=False)
    print("Done in", time.time() - start)
except Exception as e:
    print("Error:", e)
