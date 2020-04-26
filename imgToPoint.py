import exifread
import os
import geojson

#Creates a GEOJSON point from a geotagged photo
def ImgToPoint(path):

    f = open(path, 'rb')
    fileName = os.path.basename(path)
    
    #create dictionary of GPS Exif tags
    exif = {}
    tags = exifread.process_file(f, details=False)
    for i in tags:
        if i[0:3] == 'GPS':
            #print(i, ':', tags[i])
            exif[i] = str(tags[i])       
    
    #Get Latitude
    latString = exif['GPS GPSLatitude']
    latString = latString.strip('[ ]')
    latList = latString.split(',')
    separate = latList[2].split('/')
    d = int(latList[0]) 
    m = int(latList[1])/60
    s = int(separate[0])/int(separate[1])
    s = s/3600
    Latitude = d + m + s
    if exif['GPS GPSLatitudeRef'] == 'S':
        Latitude = Latitude*-1
    

    #Get Longitude
    longString = exif['GPS GPSLongitude'].strip('[ ]')
    longList = longString.split(',')
    separate = longList[2].split('/')
    d = int(longList[0]) 
    m = int(longList[1])
    s = int(separate[0])/int(separate[1])
    Longitude = d + m/60 + s/3600
    if exif['GPS GPSLongitudeRef'] == 'W':
        Longitude = Longitude*-1

    #Get Altitude
    altString = str(exif['GPS GPSAltitude'])
    altList = altString.split('/')
    altNum = int(altList[0])/int(altList[1])
    
    #print(fileName)
    #print(Latitude, ', ', Longitude, sep='')
    point = geojson.Point((Longitude, Latitude))
    feature = geojson.Feature(id=len(featureList)+1,geometry=point, properties={"Name":fileName, "Path":path})

    return feature

#Iterates through directory and returns collection of all the points
def PointCollection(directory):
    imgs = []
    geoImgs = []
    #get jpgs
    for file in os.listdir(directory):
            if file.endswith(('.jpg', '.JPG')):
                imgs.append(file)
    #filter jpgs with gps tags
    for file in imgs:
        f = open(os.path.join(directory, file), 'rb')
        tags = exifread.process_file(f, details=False)
        f.close()
        for i in tags.keys():
            if 'GPS' in i[0:3]:
                geoImgs.append(file)
    
    """
    for file in os.listdir(directory):
            if file.endswith(('.jpg', '.JPG')):
                    featureList.append(
                        ImgToPoint(
                            os.path.join(directory, file)))
    """
    for file in geoImgs:
        featureList.append(ImgToPoint(os.path.join(directory, file))
    #collection = geojson.FeatureCollection(featureList)
    return geojson.FeatureCollection(featureList)

dataset = input('Directory Path:\n')
PointCollection(dataset)
