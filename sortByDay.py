###SortByDay###
#(c) John Michael LaSalle 2017
#Contact:
#jmlasalle.com
#johnmichaellasalle@gmail.com

#/Users/johnmichaellasalle/Desktop/sortbydaysrc
#/Users/johnmichaellasalle/Desktop/photostest

#import dependencies
import exifread, os, shutil, time

#define main funct
def sortbyday():
    print("SORT BY DAY")
    print("Copy JPGs to a new folder and sort them by the date they were taken or created.\n(c) John Michael LaSalle    2017    jmlasalle.com\nVersion 1.0 finished 13/8/2017\n")
    time.sleep(1)

    #input source and destination directories
    dirpath = input("Source directory path: ")  #set source directory
    target = input('Destination directory path: ')  #set destination directory

    #create lists used later
    fileset = []
    datetime = []
    dates = []
    directory = os.fsencode(dirpath)
    
    for file in os.listdir(directory): #find JPGs in directory
        filename = os.fsdecode(file)
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            fileset.append(filename)

    print("Number of images found: " + str(len(fileset))) #number of images found
    
    for filename in fileset: #collect all the DateTime EXIF values
        filepath = os.path.join(dirpath, filename)
        f = open(filepath, 'rb')
        t = exifread.process_file(f, details=False)
        for tag, value in t.items():
            if tag in ("Image DateTime"):
                datetime.append(str(value))
    print("Succesfully detected dates for {} images.".format(len(datetime)))
    
    for value in datetime: #Tag each file with target sub directory name
        value = value[:10] #discard the HH:MM:SS values
        dates.append(value.replace(":", "")) #reformat
    dictionary = dict(zip(dates, fileset)) #combine with the filenames as date:file
    print("Dictionary created.")
    
    dates = list(set(dates))
    print("Unique dates found: {}".format(len(dates)))

    #create sub directories in target for each unique date value
    for value in dates:
        p = os.path.join(target, value)
        if not os.path.exists(p): #check if folder exists
            os.mkdir(p) #create folder
            print("Folder {} was created.".format(value)) 
        else:
            print("ERROR: Folder {} already exists. Images will be copied into existing folder.".format(value))
        
    #copy images to target sub directories 
    for key in dictionary:
        src = os.path.join(dirpath, dictionary[key]) #add filname to source directory path
        dst = os.path.join(target, key) #add subfolder name to destination directory path
        if os.path.exists(os.path.join(dst, dictionary[key])):
            print("ERROR: {} already exists in that location and was not copied.".format(dictionary[key]))
        else:
            shutil.copy2(src,dst) 
            if os.path.exists(os.path.join(dst, dictionary[key])):
                print("{} copied succesfully.".format(dictionary[key]))
            else:
                print("ERROR: {} was not copied.".format(dictionary[key]))

    print("\nSort By Day is finished running.")
        
sortbyday()
