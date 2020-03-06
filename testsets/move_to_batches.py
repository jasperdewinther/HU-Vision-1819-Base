import sys
import os
import subprocess
import time
import collections
from shutil import copyfile

os.sep = '/'
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])

output_path = os.path.join(dir_path, "batched")
if not os.path.exists(output_path):
    os.mkdir(output_path)

batchSize = 100

counter = 0

for subPathName in os.listdir(images_path):
    subPath = os.path.join(images_path, subPathName)
    if os.path.isdir(subPath):
        for subSubPathName in os.listdir(subPath):
            subSubPath = os.path.join(subPath, subSubPathName)

            destination = os.path.join(output_path, str(int(counter/100)))
            if not os.path.exists(destination):
                os.mkdir(destination)

            destinationFile = os.path.join(destination, subSubPath.split('/')[len(subSubPath.split('/'))-1])
            print("copying:", subSubPath, "to:", destinationFile)
            copyfile(subSubPath, destinationFile)
            counter+=1
    elif os.path.isfile(subPath):
        destination = os.path.join(output_path, str(int(counter/100)))
        if not os.path.exists(destination):
            os.mkdir(destination)

        destinationFile = os.path.join(destination, subPath.split('/')[len(subPath.split('/'))-1])
        print("copying:", subPath, "to:", destinationFile)
        copyfile(subPath, destinationFile)
        counter+=1


