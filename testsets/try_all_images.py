import sys
import os
import subprocess
import time
import collections

exe_path = "..\source\ExternalDLL\Release\ExternalDLL.exe"

os.sep = '\\'
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])

results = list()

timeDiff = 0



for subPathName in os.listdir(images_path):
    subPath = os.path.join(images_path, subPathName)
    startTime = None
    endTime = None
    if os.path.isdir(subPath):
        for subSubPathName in os.listdir(subPath):
            subSubPath = os.path.join(subPath, subSubPathName)
            startTime = time.time()
            result = subprocess.call([exe_path, subSubPath])
            endTime = time.time()
            results.append(result)
    elif os.path.isfile(subPath):
        startTime = time.time()
        result = subprocess.call([exe_path, subPath])
        endTime = time.time()
        results.append(result)
    timeDiff += endTime-startTime





print(collections.Counter(results).keys())
print(collections.Counter(results).values())
print("percentage correct faces recognised:", results.count(1)/len(results)*100)
print("total execution time:", str(timeDiff), "seconds")
print("avarage execution time:", str(timeDiff/len(results)), "seconds")