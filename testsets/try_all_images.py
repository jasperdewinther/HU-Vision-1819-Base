import sys
import os
import subprocess
import time

exe_path = "..\source\ExternalDLL\Release\ExternalDLL.exe"

os.sep = '\\'
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])
print(images_path)

results = list()

startTime = time.time()

for subPathName in os.listdir(images_path):
    subPath = os.path.join(images_path, subPathName)
    if os.path.isdir(subPath):
        for subSubPathName in os.listdir(subPath):
            subSubPath = os.path.join(subPath, subSubPathName)
            print("analyzing:", subSubPath)
            result = subprocess.call([exe_path, subSubPath])
            print("result:", result)
            results.append(result)
    elif os.path.isfile(subPath):
        print("analyzing:", subPath)
        result = subprocess.call([exe_path, subPath])
        print("result:", result)
        results.append(result)

endTime = time.time()

print(results)
print("total execution time:", str(endTime-startTime), "seconds")
print("avarage execution time:", str((endTime-startTime)/len(results)), "seconds")