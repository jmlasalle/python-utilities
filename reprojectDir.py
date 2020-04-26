import os
import pandas as import pd
import geopandas as gpd

validFileTypes = ['.shp', '.geojson']

def reprojectDir(dir, crs, copy=False):
    # check that arguments are valid

    # build list of GIS files
    fileList = []
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if os.path.splitext(os.path.join(subdir, file))[1] in validFileTypes:
                fileList.append(os.path.join(subdir, file))
            else:
                pass

    print(f'Found {len(fileList)} GIS files.'')

    # iterate through file list
    for filePath in fileList:
        print(f'Reading {os.path.basename(filePath)}')
        contents = gpd.read_file(filePath)
        if contents.crs != crs:
            print(f'Reprojecting {os.path.basename(filePath)}')
            contents = contents.to_crs(crs)
            print(f'Saving {os.path.basename(filePath)}')
            contents.to_file(filePath)
        else:
            print(f'{os.path.basename(filePath)} already in correct CRS')
