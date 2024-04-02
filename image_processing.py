from PIL import Image
from tqdm import tqdm
import os

def convert_png_to_jpg(path):
    image_names = os.listdir(path)
    image_names = [name for name in image_names if ".png" in name]
    image_names = [name for name in image_names if not name.split(".png")[0]+".jpg" in os.listdir(path)]
    image_names = [name for name in image_names if not name.split(".png")[0]+".jpg" in os.listdir(path)]
    for i in tqdm(range(len(image_names)), desc="PNG to JPG conversion progress"):
        name = image_names[i]
        separator = "/" if "/" in path else "\\"                
        image = Image.open(f"{path}{separator}{name}")
        rgb_image = image.convert('RGB')
        rgb_image.save(path+separator+name.split(".png")[0]+".jpg")
    
def resize():
    pass
   
def is_black(image_path, threshold=10):
    with Image.open(image_path) as img:
        grayscale = img.convert('L')  # Convert to grayscale
        black_pixels = sum(1 for pixel in grayscale.getdata() if pixel <= threshold)
        total_pixels = grayscale.size[0] * grayscale.size[1]  # Width * Height
        ratio_black = black_pixels / total_pixels

    return ratio_black > 0.95  # If 95% or more of the image is black, consider it as a black image

def remove_black_images(folder_path):
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if is_black(image_path):
            os.remove(image_path)
            print(f"Removed black image: {filename}")

   
def is_black(image_path, threshold=10):
    with Image.open(image_path) as img:
        grayscale = img.convert('L')  # Convert to grayscale
        black_pixels = sum(1 for pixel in grayscale.getdata() if pixel <= threshold)
        total_pixels = grayscale.size[0] * grayscale.size[1]  # Width * Height
        ratio_black = black_pixels / total_pixels

    return ratio_black > 0.95  # If 95% or more of the image is black, consider it as a black image

def remove_black_images(folder_path):
    i = 0
    directory = [i for i in os.listdir(folder_path) if ".jpg" in i]
    for filename in tqdm(directory, desc="Removing bad images", unit="pics"):
        image_path = os.path.join(folder_path, filename)
        if is_black(image_path):
            os.remove(image_path)
            print(f"Removed black image: {filename}")
            i += 1
    print(f"Removed {i} bad images.")
def get_folder_size(folder_path):
    png_size = 0
    jpg_size = 0
    num_pngs = 0
    num_jpgs = 0
    total_size = 0
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is a PNG file
        if filename.endswith('.png'):
            # Get the size of the PNG file
            size = os.path.getsize(file_path)
            total_size += size
            png_size += size
            num_pngs += 1
        
        # Check if the file is a JPG file
        elif filename.endswith('.jpg'):
            # Get the size of the JPG file
            size = os.path.getsize(file_path)
            total_size += size
            jpg_size += size
            num_jpgs += 1

    # Convert the total size to gigabytes
    gb_converter = 1024**3
    total_size_gb = total_size / gb_converter
    png_size_gb = png_size / gb_converter
    jpg_size_gb = jpg_size / gb_converter
    
    return total_size_gb, png_size_gb, jpg_size_gb, num_pngs, num_jpgs

if __name__ == "__main__":
    # path to images
    folder = "/Users/ethan/Documents/GeoGuessrAI/andorra"
    convert_png_to_jpg(folder)
    t, p, j, np, nj = get_folder_size(folder)
    print(f"Folder size: {t} GB")
    print(f"Total size of PNGs: {p} GB")
    print(f"Total size of JPGs: {j} GB")
    print(f"Total number of PNGs: {np}")
    print(f"Total number of JPGs: {nj}")
    remove_black_images(folder)