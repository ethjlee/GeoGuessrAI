#!bin/bash

parent_folder="/Users/ethan/Documents/GeoGuessrAI"
country="andorra"

source_folder="${parent_folder}/${country}"
echo $source_folder
destination_folder="${parent_folder}/${country}/pngs"
echo $destination_folder

find "${source_folder}" -type f -name "*.png" -exec mv {} "${destination_folder}" \;
