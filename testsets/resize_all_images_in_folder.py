import sys
import os
import cv2
import numpy as np


os.sep = '/'
out_folder = os.path.join(os.getcwd(), "scaled_output")
dir_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(dir_path, sys.argv[1])

results = list()

timeDiff = 0

if not os.path.isdir(out_folder):
    os.mkdir(out_folder)

for subPathName in os.listdir(images_path):
    subPath = os.path.join(images_path, subPathName)
    if os.path.isfile(subPath):
        print("scaling:", subPath)
        img = cv2.imread(subPath)
        img = cv2.resize(img, (250,250), interpolation = cv2.INTER_LANCZOS4)
        print("writing:", os.path.join(out_folder, subPath.split('/')[-1]))
        cv2.imwrite(os.path.join(out_folder, subPath.split('/')[-1]),img)