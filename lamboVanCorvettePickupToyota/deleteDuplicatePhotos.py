print('hi deleteDuplicates')
import os
import hashlib
from PIL import Image

def compute_image_hash(image_path):
    """Compute the hash of an image file."""
    with Image.open(image_path) as img:
        # Convert the image to a consistent format (like RGB) and resize to standard size (optional)
        img = img.convert('RGB')
        
        # Generate a hash of the image data
        img_hash = hashlib.md5(img.tobytes()).hexdigest()
    return img_hash

def delete_duplicate_images(folder_path):
    """Delete duplicate images in the given folder based on hash comparison."""
    hash_dict = {}  # Dictionary to store image hashes and file paths

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                file_path = os.path.join(root, file)
                
                # Compute the hash of the current image
                img_hash = compute_image_hash(file_path)
                
                # Check if this hash already exists
                if img_hash in hash_dict:
                    print(f"Duplicate found: {file_path}. Deleting...")
                    os.remove(file_path)  # Delete duplicate image
                else:
                    hash_dict[img_hash] = file_path  # Store the hash if it's unique

#if __name__ == "__main__":
#    # Define the root folder where the car photos are stored
#    root_folder = r'C:\Noah\gitProjects\NoahRepo\carDetector\carPhotos'

    # Delete duplicates in each folder within carPhotos
#    delete_duplicate_images(root_folder)
#    print('deleteDuplicatePhotos.py was successfully run')





root_folder = r'carPhotos'
root_folder2 = r'carPhotosLamboAndVan'

delete_duplicate_images(root_folder)
delete_duplicate_images(root_folder2)