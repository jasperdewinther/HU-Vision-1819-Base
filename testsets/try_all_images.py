import sys
import os
import subprocess
import time
import collections
import numpy as np

exe_path = "..\\source\\ExternalDLL\\Release\\ExternalDLL.exe"

os.sep = '\\'
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])

results = dict()

timeDiff = 0



for subPathName in os.listdir(images_path):
    subPath = os.path.join(images_path, subPathName)
    batchNumber = subPath.split("\\")[len(subPath.split("\\"))-1]
    results[batchNumber] = list()
    startTime = None
    endTime = None
    if os.path.isdir(subPath):
        for subSubPathName in os.listdir(subPath):
            subSubPath = os.path.join(subPath, subSubPathName)
            print("working on:", subSubPath)
            startTime = time.time()
            result = subprocess.call([exe_path, subSubPath])
            endTime = time.time()
            results[batchNumber].append(result)
    elif os.path.isfile(subPath):
        print("working on:", subPath)
        startTime = time.time()
        result = subprocess.call([exe_path, subPath])
        endTime = time.time()
        results[batchNumber].append(result)
    timeDiff += endTime-startTime

try:
    goodsPerBatch = np.full(len(results), 0)
    good = 0
    totalCount = 0

    for key in results:
        goodsPerBatch[int(key)] = results[key].count(1)
        totalCount += len(results[key])
        good += results[key].count(1)
except:
    pass
try:
    print("standard deviation:", np.std(goodsPerBatch))
    print("percentage correct faces recognised:", good/totalCount)
except:
    pass
print("total execution time:", str(timeDiff), "seconds")
print("avarage execution time:", str(timeDiff/len(results)), "seconds")