#prints image EXIF data
import exifread
import os
"""
Prints all EXIF keys and values with minimal formatting
"""
def ExifPrint(path):
    f = open(path, 'rb')
    e = exifread.process_file(f, details=False)
    for a, b in e.items():
        print(a, ':  ', b)


def ExifDir(DirectoryPath):
    for file in os.listdir(DirectoryPath):
        f = open(os.path.join(DirectoryPath, file), 'rb')
        tags = exifread.process_file(f, details=False)
        if 'GPS GPSAltitude' in tags:            
            altString = str(tags['GPS GPSAltitude'])
            altList = altString.split('/')
            altNum = int(altList[0])/int(altList[1])
            print(file + "," + str(altNum))
        else:
            pass
