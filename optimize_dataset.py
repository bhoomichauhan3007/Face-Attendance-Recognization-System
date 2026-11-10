import os
import shutil

src_dir = "dataset"
dest_dir = "dataset_fast"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Iterate over each person folder
for person_folder in os.listdir(src_dir):
    person_path = os.path.join(src_dir, person_folder)
    
    if os.path.isdir(person_path):
        # Create corresponding folder in dataset_fast
        dest_person_path = os.path.join(dest_dir, person_folder)
        if not os.path.exists(dest_person_path):
            os.makedirs(dest_person_path)
            
        # Get all images
        images = [f for f in os.listdir(person_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Copy only the FIRST image
        if images:
            src_img = os.path.join(person_path, images[0])
            dest_img = os.path.join(dest_person_path, images[0])
            shutil.copy2(src_img, dest_img)
            print(f"Added 1 reference image for {person_folder}")

print("\nOptimized fast dataset created containing only required 1-shot learning references!")
