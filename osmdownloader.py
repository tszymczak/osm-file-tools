#!/usr/bin/python
# A python program that downloads OpenStreetMap data files based on the URL.
# Refuses to overwrite files.

import sys
import os
import urllib2
import shutil

def parse_bbox(inbbox):
    # Remove any spaces.
    bbox = inbbox.replace(" ", "")
    return bbox
    
usage = "Usage: ./osmupdate.py bbox filename. The bounding box must be in \
OpenStreetMap format. For example: \
./osmdownloader.py -80.010782,40.432707,-79.985398,40.448335 ./downtown-pittsburgh.osm \
Note: This program will quit with an error instead of overwriting files."

if len(sys.argv) == 3:
    inbbox = sys.argv[1];
    outfile = sys.argv[2];
else:
    print(usage)
    raise RuntimeError("Wrong number of arguments.")
    
# Parse the input bounding box to convert it into a format the OSM server
# understands.
bbox = parse_bbox(inbbox)

print("Downloading data within bounding box " + bbox)
if os.path.exists(outfile):
    raise RuntimeError("Output file already exists. Choose a different file name.");
    
# Download the OSM data file.
url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + bbox


try:
    url_file_handle = urllib2.urlopen(url)
except urllib2.HTTPError as e:
    raise RuntimeError("An error occurred when trying to download file: HTTP Error " + str(e.code))
except urllib2.URLError as e:
    raise RuntimeError("An error occurred when trying to download file: " + e.reason)

with open(outfile,'wb') as output:
    shutil.copyfileobj(url_file_handle, output)

print("Finished.");
