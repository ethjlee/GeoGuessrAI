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

if __name__ == "__main__":
    # path to images
    folder = "/Users/ethan/Documents/GeoGuessrAI/andorra"
    convert_png_to_jpg(folder)
