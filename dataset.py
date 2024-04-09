import pandas as pd
import os, sys

def main(countries_list):
    df = pd.DataFrame()
    names = []
    cl = []
    i = 0
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"), topdown=False):
        for folder in dirs:
            if folder in countries_list:
                for dirpath, _, filenames in os.walk(os.path.join(root, folder)):
                    img_paths = [os.path.join(root, folder, name) for name in filenames] # python list
                    names += img_paths
                    cl += [i] * len(img_paths)
                i += 1
    
    df["images"] = names
    df["class"] = cl
    print(df)
    return df
if __name__ == "__main__":
    dim = 224
    countries = ["andorra", "taiwan", "south-korea", "malta"] # taiwan may not be a "country"!!!
    for i in range(len(countries)):
        countries[i] = f"{countries[i]}{dim}x{dim}"
    
    df = main(countries_list=countries)
    
    
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, "output.csv")
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)  # Set index=False to exclude the index from the CSV file

