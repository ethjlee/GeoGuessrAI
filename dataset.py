import pandas as pd
import os, sys

def main(countries_list):
    df = pd.DataFrame()
    names = []
    cl = []
    i = 0
    for root, dirs, files in os.walk(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), topdown=False):
        for folder in dirs:
            if folder in countries_list:
                f = os.path.join(root, folder)
                imgs = [im for im in os.listdir(f) if im.endswith(".jpg")] # python list
                cl += [i] * len(imgs)
                names += imgs
                i += 1
    
    df["images"] = names
    df["class"] = cl
    print(df)
    return df
if __name__ == "__main__":
    dim = 224
    countries = ["andorra", "taiwan", "south-korea"] # taiwan may not be a "country"!!!
    for i in range(len(countries)):
        countries[i] = f"{countries[i]}{dim}x{dim}"

    main(countries_list=countries)

