#!bin/bash

parent_folder="/Users/aidan/Documents/GeoGuessrAI"
country="andorra"

source_folder="${parent_folder}/${country}"
echo "From: $source_folder"
destination_folder="${parent_folder}/${country}_pngs"
echo "To: $destination_folder"

find "${source_folder}" -type f -name "*.png" -exec mv {} "${destination_folder}" \;

echo "Finished"
