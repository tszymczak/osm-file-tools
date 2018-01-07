# OSM File Tools
This is a small collection of tools to work with .osm files. I wrote these
utilities to help me manage offline OSM data.

## osmdownloader.py
A Python script that downloads OpenStreetMap data in a certain area to a file.
The area is specified with a [bounding box](https://wiki.openstreetmap.org/wiki/Bounding_Box). For example:

./osmdownloader.py -80.010782,40.432707,-79.985398,40.448335 ./downtown-pittsburgh.osm

This script doesn't overwrite files, so it will exit with an error if you try
to do that.

## osmupdater.py
A python script that updates data in a .osm file. It opens the file, parses
it to figure out the bounding box, and then downloads a new version of the
data from OSM, deleting whatever was in the file previously. It makes backup
copes of the files when updating them in case the download fails or there
were changes in the old file that weren't uploaded to OSM.

The usage of this utility is rather simple:

./osmupdater.py file1 file2 ... fileN
