import sys
import os
import subprocess
import time
import collections
import numpy as np


def count_matching(condition, seq):
    """Returns the amount of items in seq that return true from condition"""
    return sum(1 for item in seq if condition(item))


def isError(i):
    # any return code above 2000 is an unexpected error
    return i > 2000


exe_path = "..\\source\\ExternalDLL\\Release\\ExternalDLL.exe"

os.sep = '\\'
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])

results = dict()

timeDiff = 0
pathsToFoundImages = list()
counter = 0


for subPathName in os.listdir(images_path):
    # subpath is the path to all files in the working directory
    subPath = os.path.join(images_path, subPathName)
    batchNumber = subPath.split("\\")[len(subPath.split("\\"))-1]
    results[batchNumber] = list()
    startTime = None
    endTime = None
    if os.path.isdir(subPath):
        for subSubPathName in os.listdir(subPath):
            if counter % 100 == 0:
                print("analysed", str(counter), "files,",
                      "total time spent processing:", str(timeDiff), "seconds")
            # loop over all sub files
            subSubPath = os.path.join(subPath, subSubPathName)
            #print("working on:", subSubPath)
            # time the execution
            startTime = time.time()
            result = subprocess.call([exe_path, subSubPath])
            endTime = time.time()
            if results == 1:
                pathsToFoundImages.append(subSubPath)
            # append results to the correct batch
            results[batchNumber].append(result)
            timeDiff += endTime-startTime

            counter += 1
    elif os.path.isfile(subPath):
        if counter % 100 == 0:
            print("analysed", str(counter), "files,",
                  "total time spent processing:", str(timeDiff), "seconds")
        #print("working on:", subPath)
        # time the execution
        startTime = time.time()
        result = subprocess.call([exe_path, subPath])
        endTime = time.time()
        if results == 1:
            pathsToFoundImages.append(subPath)
        # append results to the correct batch
        results[batchNumber].append(result)
        timeDiff += endTime-startTime

        counter += 1


goodsPerBatch = np.full(len(results), 0)
errorsPerBatch = np.full(len(results), 0)
good = 0
totalCount = 0
allResults = list()

# loop over every batch
for key in results:
    for i in results[key]:
        allResults.append(i)
    goodsPerBatch[int(key)] = results[key].count(1)
    errorsPerBatch[int(key)] = count_matching(isError, results[key])
    totalCount += len(results[key])
    good += results[key].count(1)

totalErrors = count_matching(isError, allResults)


print()
print()
print()
print()
print()
for i in pathsToFoundImages:
    print(i)


print()
print()
print("--------------------results--------------------")
print("total images:", str(totalCount))
print("total faces recognised:", str(good),
      "percentage correct:", str(good/totalCount*100), "%")
print("total errors:", str(totalErrors),
      "error percentage:", str(totalErrors/totalCount*100), "%")
print("standard deviation faces found:", np.std(goodsPerBatch))
print("standard deviation error:", np.std(errorsPerBatch))
print("total execution time:", str(timeDiff), "seconds")
print("avarage execution time:", str(timeDiff/len(allResults)), "seconds")
