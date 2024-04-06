from PIL import Image
from tqdm import tqdm
import os, shutil, sys, getpass
import asyncio, tracemalloc
"""
IMPORTANT:
After image capture, your directory set up should look like this.

Your_parent_directory/
│
├── GeoGuessrAI/
│   ├── image_capture.py
│   ├── image_processing.py
│   └── ...
│
├── YourCountryFolder1/
│   ├── Image1.jpg
│   ├── Image2.jpg
│   └── ...
│
└── YourCountryFolder1_pngs/
    ├── Image1.jpg
    ├── Image2.jpg
    └── ...
"""
def convert_png_to_jpg(path):
    country = os.path.split(path)[-1]
    image_names = os.listdir(path)
    image_names = [name for name in image_names if name.endswith(".png")]
    for i in tqdm(range(len(image_names)), desc=f"({country}) PNG to JPG conversion progress"):
        name = image_names[i]
        image = Image.open(os.path.join(path, name))
        rgb_image = image.convert('RGB')
        new_name = name.split(".png")[0] + ".jpg"
        rgb_image.save(os.path.join(path, new_name))
    
def resize(folder_path, output_path, width, height):
    folder_path # ./GGAI/country
    parent_folder = os.path.dirname(folder_path) # ./GGAI
    separator = "/" if "/" in folder_path else "\\"
    country = folder_path.split(separator)[-1] # /country
    folder_path = os.path.join(parent_folder, country)
    if not os.path.exists(output_path): 
        os.makedirs(output_path)
    
    
    for filename in tqdm(os.listdir(folder_path), desc=f"({country}) Resizing images", unit="pics"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(folder_path, filename)
            image = Image.open(input_path)
            
            # Get current dimensions
            img_width, img_height = image.size
            
            # Calculate cropping coordinates
            left = (img_width - width) / 2
            top = (img_height - height) / 2
            right = left + width
            bottom = top + height
            
            # Cropping image
            cropped_image = image.crop((left, top, right, bottom))
            output_file_path = os.path.join(output_path, filename)
            cropped_image.save(output_file_path)


def is_black(image_path, threshold=10):
    with Image.open(image_path) as img:
        grayscale = img.convert('L')  # Convert to grayscale
        black_pixels = sum(1 for pixel in grayscale.getdata() if pixel <= threshold)
        total_pixels = grayscale.size[0] * grayscale.size[1]  # Width * Height
        ratio_black = black_pixels / total_pixels

    return ratio_black > 0.95  # If 95% or more of the image is black, consider it as a black image

def remove_black_images(folder_path):
    i = 0
    country = os.path.split(folder_path)[-1]
    directory = [i for i in os.listdir(folder_path) if ".jpg" in i]
    for filename in tqdm(directory, desc=f"({country}) Removing bad images", unit="pics"):
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

def move_pngs(source_folder):
    # Move pngs to a separate directory.
    source_folder # ./GGAI/country
    parent_folder = os.path.dirname(source_folder) # ./GGAI
    separator = "/" if "/" in source_folder else "\\"
    country = source_folder.split(separator)[-1] # /country
    
    # Assign source -> destination folders
    #print("From:", source_folder)
    destination_folder = os.path.join(parent_folder, f"{country}_pngs")
    #print("To:", destination_folder)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    i = 0
    for root, _, files in os.walk(source_folder):
        files = [f for f in files if f.endswith(".png")]
        if len(files) > 0:
            for file in tqdm(files, desc=f"({country}) Moving PNGs out", unit="pngs"):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file)
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(source_file_path, destination_file_path)
                i += 1
    print(f"Moved {i} PNGs from {source_folder} to {destination_folder}.")

async def process_images(w_and_h, country):
    path_to_images = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), country)
    path_to_resized_images = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"{country}{w_and_h}x{w_and_h}")

    await asyncio.to_thread(convert_png_to_jpg, path_to_images)
    t, p, j, np, nj = await asyncio.to_thread(get_folder_size, path_to_images)
    
    print(f"\n{country} Folder size: {t} GB\n{country} Total size of PNGs: {p} GB\n{country} Total size of JPGs: {j} GB\n{country} Number of PNGs: {np}\n{country} Number of JPGs: {nj}\n")
    
    await asyncio.to_thread(move_pngs, path_to_images)
    await asyncio.to_thread(remove_black_images, path_to_images)
    
    await asyncio.to_thread(resize, path_to_images, path_to_resized_images, w_and_h, w_and_h)     

async def main(w_and_h, countries_list):
    await asyncio.gather(*(process_images(w_and_h, country) for country in countries_list))

if __name__ == "__main__":

    """Only need to change the country name. Then hit run."""
    countries_list = ["andorra", "south-korea", "colombia", "testing", "taiwan"]


    tracemalloc.start()
    w_and_h = int(input("Enter width and height: "))
    
    asyncio.run(main(w_and_h, countries_list))