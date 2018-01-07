#!/usr/bin/python
# A python program that downloads updated versions of OpenStreetMap data files.
# The old files are moved to a different location instead of being deleted,
# in case this script screws up or there is un-uploaded data in the files.
# This is a bit of a kludge, but it works well enough as long as you don't
# forget to delete the backup files when no longer needed.
# Usage:
# ./osmupdater.py file1 file2 ... fileN

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

import argparse    
import os
import shutil
import urllib2
from xml.etree import ElementTree


def get_copy_name(infile):
    dest = infile + ".old"
    if not os.path.exists(dest):
        return dest

    # Don't let more than 100 files build up.
    for i in range (1, 100):
        dest = infile + "." + str(i) + ".old"
        if not os.path.exists(dest):
            return dest

    # If there are more than 100 files, the user needs to clean stuff up.
    # We shrug our shoulders and quit.
    raise IOError('Too many backup files. Delete the old ones.')


# Get the bounding box of an OpenStreetMap date file by parsing the markup.
# Note that right now, only files with one bounding box are supported.
def get_osm_bbox(infile):
    tree = ElementTree.parse(infile)
    root = tree.getroot()
    count = 0
    bboxline = "junk"
    
    for child in root:
        if child.tag == "bounds":
            bboxline = child.attrib
            count += 1
            
    if count > 1:
        raise('File with more than one bounding box not supported right now.')
    
    # Parse the dictionary to get the bbox.
    minlat = bboxline['minlat']
    maxlat = bboxline['maxlat']
    minlon = bboxline['minlon']
    maxlon = bboxline['maxlon']
    
    return minlon + "," + minlat + "," + maxlon + "," + maxlat


parser = argparse.ArgumentParser(description='Update the data within OSM files.')
parser.add_argument('infile', nargs='*')
args = parser.parse_args()

for infile in args.infile:
    print("Processing OSM File " + infile)
    if os.path.exists(infile):
        # Make a backup file
        bbox = get_osm_bbox(infile)
        print(bbox)
        dest = get_copy_name(infile)
        shutil.move(infile, dest)
        # Download the OSM data file.
        print("Downloading new version of " + infile)
        url = "https://api.openstreetmap.org/api/0.6/map?bbox=" + bbox
        try:
            url_file_handle = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            raise RuntimeError("An error occurred when trying to download file: HTTP Error " + str(e.code))
        except urllib2.URLError as e:
            raise RuntimeError("An error occurred when trying to download file: " + e.reason)
        
        with open(infile, 'wb') as output:
            shutil.copyfileobj(url_file_handle, output)
    else:  
        print("Warning: " + infile + " does not exist. Skipping.")

print("Finished.");

# The end.
