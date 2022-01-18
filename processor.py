from ast import Not
from genericpath import isdir
import os, pyunpack, sys, glob, shutil

#https://xranks.com/alternative/3d-load.net
#https://render-state.to
toExtractPath = "./to-extract"
extractedPath = "./extracted"
toExtractDir = os.listdir(toExtractPath) 
extractedDir = os.listdir(extractedPath) 

targetedPaths = ["./extracted", "./extracted/Content"]
pathVariations = ["Runtime", "data", "People", "aniBlocks", "General", "Environments"]
mainDestinationPath = "./extracted/My DAZ 3D Library"
directoriesToCreate = ["__main_daz/aniBlocks", "__main_daz/General", "__main_daz/Environments"]
dazLibraryPath = "/Users/macpro/Documents/DAZ 3D/Studio/My Library"
def argIs(value):
    return len(sys.argv) > 1 and sys.argv[1] == value

def argInList(list):
    return len(sys.argv) > 1 and sys.argv[1] in list

def noArgGiven():
    return len(sys.argv) <= 1

if argIs("extract") or noArgGiven():
    for toExtractFile in toExtractDir:
        if toExtractFile.endswith(".rar") or toExtractFile.endswith(".zip"):
            filePath = os.path.join(toExtractPath,toExtractFile)
            try:
                arch = pyunpack.Archive(filePath)
                arch.extractall(directory=extractedPath)
                # os.remove(os.path.join(toExtractPath,toExtractFile))
            except Exception as e:
                print("error on {}".format(filePath))
                print(e)
    print("extraction ended")

elif argIs("order"):
    for toExtractFile in extractedDir:
        if toExtractFile.endswith(".rar") or toExtractFile.endswith(".zip"):
            filePath = os.path.join(extractedPath,toExtractFile)
            try:
                arch = pyunpack.Archive(filePath)
                arch.extractall(directory=extractedPath)
                os.remove(filePath)
            except Exception as e:
                print("error on {}".format(filePath))
                print(e)
    print("ordering ended")

elif argIs("to-library"):
    for directoryToCreate in directoriesToCreate:
        cmd = 'mkdir {}'.format(directoryToCreate.replace("__main_daz",mainDestinationPath))
    for targetedPath in targetedPaths:
        targetedDir = os.listdir(targetedPath) 
        for currentPath in targetedDir:
            if isdir(os.path.join(targetedPath, currentPath)):
                for pathVariation in pathVariations:
                    if pathVariation in os.path.join(targetedPath, currentPath) and ("My DAZ 3D Library" in os.path.join(targetedPath, currentPath)) == False :
                        # destination = os.path.join(mainDestinationPath, pathVariation)
                        # movingCmd = 'mv "{0}/*" "{1}"'.format(os.path.join(targetedPath, currentPath), destination)
                        movingCmd = 'cp -r "{0}" "{1}"'.format(os.path.join(targetedPath, currentPath), mainDestinationPath)
                        os.system(movingCmd)
                        break
    finalCmd = 'mv "{0}" "{1}"'.format(os.path.abspath(mainDestinationPath), dazLibraryPath)
    os.system(finalCmd)
    for root, dirs, files in os.walk(extractedPath):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    print("Successfully move to Library")

elif argIs("clean"):
    for root, dirs, files in os.walk(extractedPath):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    print("cleaning ended")

elif argIs("clean-to-extact"):
    for root, dirs, files in os.walk(toExtractPath):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    print("cleaning ended")

elif argIs("exec-all"):
    cmds = ["extract",  "order", "to-library"]
    for cmd in cmds:
        os.system("python3 processor.py {}".format(cmd))
else:
    print("know arguments are extract extract, order and clean")


