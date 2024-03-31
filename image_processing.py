from PIL import Image
from tqdm import tqdm
import os

def convert_png_to_jpg(path):
    image_names = os.listdir(path)
    image_names = [name for name in image_names if ".png" in name]
    image_names = [name for name in image_names if not name.split(".png")[0]+".jpg" in os.listdir(path)]
    for i in tqdm(range(len(image_names)), desc="PNG to JPG conversion progress"):
        name = image_names[i]
        image = Image.open(f"{path}/{name}")
        rgb_image = image.convert('RGB')
        rgb_image.save(path+"/"+name.split(".png")[0]+".jpg")
    
def resize():
    pass
def get_folder_size(folder_path):
    total_size = 0
    png_size = 0
    jpg_size = 0
    
    # Walk through all files and subdirectories in the folder
    for dirpath, _, filenames in os.walk(folder_path):
        # Add the size of each file to the total size
        png_files = [fn for fn in filenames if ".png" in fn]
        jpg_files = [gn for gn in filenames if ".jpg" in gn]
        for pf in png_files:
            file_path = os.path.join(dirpath, pf)
            size = os.path.getsize(file_path)
            total_size += size
            png_size += size
        for jf in jpg_files:
            file_path = os.path.join(dirpath, jf)
            size = os.path.getsize(file_path)
            total_size += size
            jpg_size += size

    # Convert the total size to gigabytes
    gb_converter = 1024**3
    total_size_gb = total_size / gb_converter
    png_size_gb = png_size / gb_converter
    jpg_size_gb = jpg_size / gb_converter
    
    return total_size_gb, png_size_gb, jpg_size_gb

if __name__ == "__main__":
    # path to images
    folder = "/Users/ethan/Documents/GeoGuessrAI/andorra"
    convert_png_to_jpg(folder)
    t, p, j = get_folder_size(folder)
    print(f"Folder size: {t} GB")
    print(f"Total size of PNGs: {p} GB")
    print(f"Total size of JPGs: {j} GB")