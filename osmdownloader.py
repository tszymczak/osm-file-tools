#!/usr/bin/python
# A python program that downloads OpenStreetMap data files based on the URL.
# Refuses to overwrite files.

# Copyright 2018 Thomas Szymczak
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
