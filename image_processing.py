from PIL import Image
from tqdm import tqdm
import os

def convert_png_to_jpg(path):
    image_names = os.listdir(path)
    image_names = [name for name in image_names if ".png" in name]
    for i in tqdm(range(len(image_names)), desc="PNG to JPG conversion progress"):
        name = image_names[i]
        image = Image.open(f"{path}/{name}")
        rgb_image = image.convert('RGB')
        rgb_image.save(path+"/"+name.split(".png")[0]+".jpg")
    
def resize():
    pass
def get_folder_size(folder_path):
    total_size = 0
    
    # Walk through all files and subdirectories in the folder
    for dirpath, _, filenames in os.walk(folder_path):
        # Add the size of each file to the total size
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    
    # Convert the total size to gigabytes
    total_size_gb = total_size / (1024**3)
    
    return total_size_gb

if __name__ == "__main__":
    # path to images
    folder = "/Users/ethan/Documents/GeoGuessrAI/andorra"
    convert_png_to_jpg(folder)
    print("Folder size:", get_folder_size(folder), "GB")
