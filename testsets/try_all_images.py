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


def run_analysis(exe_path, dir_name):
    results = dict()

    timeDiff = 0
    pathsToFoundImages = list()
    counter = 0
    times = list()

    for subPathName in os.listdir(dir_name):
        # subpath is the path to all files in the working directory
        subPath = os.path.join(dir_name, subPathName)
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
                # time the execution
                startTime = time.time()
                result = None
                try:
                    result = subprocess.call([exe_path, subSubPath], timeout=1)
                except subprocess.TimeoutExpired:
                    result = 99999999
                endTime = time.time()
                if result == 1:
                    pathsToFoundImages.append(subSubPath)
                # append results to the correct batch
                results[batchNumber].append(result)
                times.append(endTime-startTime)
                timeDiff += endTime-startTime

                counter += 1
        elif os.path.isfile(subPath):
            if counter % 100 == 0:
                print("analysed", str(counter), "files,",
                      "total time spent processing:", str(timeDiff), "seconds")
            # time the execution
            startTime = time.time()
            result = None
            try:
                result = subprocess.call([exe_path, subPath], timeout=1)
            except subprocess.TimeoutExpired:
                result = 99999999
            endTime = time.time()
            if result == 1:
                pathsToFoundImages.append(subPath)
            # append results to the correct batch
            results[batchNumber].append(result)
            times.append(endTime-startTime)
            timeDiff += endTime-startTime

            counter += 1

    goodsPerBatch = np.full(len(results), 0)
    errorsPerBatch = np.full(len(results), 0)
    detected = 0
    totalCount = 0
    allResults = list()

    # loop over every batch
    for key in results:
        for i in results[key]:
            allResults.append(i)
        goodsPerBatch[int(key)] = results[key].count(1)
        errorsPerBatch[int(key)] = count_matching(isError, results[key])
        totalCount += len(results[key])
        detected += results[key].count(1)

    totalErrors = count_matching(isError, allResults)

    return totalCount, detected, totalErrors, goodsPerBatch, errorsPerBatch, timeDiff, pathsToFoundImages, times


def print_results(analysis_name, totalCount, detected, totalErrors, goodsPerBatch, errorsPerBatch, timeDiff, pathsToFoundImages, times):
    print("--------------------results--------------------")
    print("total images:", str(totalCount))
    print("total faces recognised:", str(detected),
          "percentage correct:", str(detected/totalCount*100), "%")
    print("total errors:", str(totalErrors),
          "error percentage:", str(totalErrors/totalCount*100), "%")
    print("standard deviation faces found:", np.std(goodsPerBatch))
    print("standard deviation error:", np.std(errorsPerBatch))
    print("total execution time:", str(timeDiff), "seconds")
    print("avarage execution time:", str(timeDiff/totalCount), "seconds")
    print("standard deviation time:",  np.std(times))
    print("link to images that were found:")
    for i in pathsToFoundImages:
        print(i)


exe_path = "..\\source\\ExternalDLL\\Release\\ExternalDLL.exe"
os.sep = '\\'
dir_path = os.path.dirname(os.path.realpath(__file__))
faces_path = os.path.join(dir_path, "batched_LFW_face_database")
false_detections_path = os.path.join(dir_path, "batched_coco2017_val_250x250")

faces_results = run_analysis(exe_path, faces_path)
false_results = run_analysis(exe_path, false_detections_path)

print_results("faces", *faces_results)
print_results("false detections", *false_results)
