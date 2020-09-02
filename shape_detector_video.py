import cv2
import argparse
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import time


ts = time.gmtime()
ts = time.strftime("%Y%m%d%H%M%S", ts)
# 2020-08-24 09:18:01


# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help = "path to the video")
# args = vars(ap.parse_args())
# load the video
#cap = cv2.VideoCapture(args["video"])
mypath = "/home/aligot/Desktop/Arena/HeatmapPositionRobots/Videos/median_runs/"

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

all_videos = getListOfFiles(mypath)

for i, v in enumerate(all_videos):
    f = v.split('/')
    name = f[len(f)-2] + "_" + f[len(f)-1]
    output_file_name = os.path.splitext(name)[0] + ".txt"
    print(i, " / ", len(all_videos)-1)
    output_file = open("Positions/" + output_file_name, 'w')

    cap = cv2.VideoCapture(v)

    frame_cnt = 0
    # Loop untill the end of the video
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is None:
            break

        # frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,
                             # interpolation = cv2.INTER_CUBIC)
        if (frame_cnt % 6 == 0):
            frame = frame[30:1230, 150:1350]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 3)
            sharpen_kernel = np.array([[-1,-1,-1], [-1,7.8,-1], [-1,-1,-1]])
            sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
            #
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            close = cv2.morphologyEx(sharpen, cv2.MORPH_CLOSE, kernel, iterations=2)
            #
            #Filtering the noise
            filtered = cv2.fastNlMeansDenoising(close, None, 10, 7, 21)
            kernel = np.ones((2,2),np.uint8)
            erosion = cv2.erode(filtered,kernel,iterations = 5)
            filtered = cv2.fastNlMeansDenoising(erosion, None, 10, 7, 21)
            #
            #
            ret,final= cv2.threshold(filtered,40,255,0)
            #
            #cv2.imshow("final",final)
            #
            cnts = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
            #
            nb_robots = 0
            for c in cnts:
                area = cv2.contourArea(c)
                x,y,w,h = cv2.boundingRect(c)
                centers, radius = cv2.minEnclosingCircle(c)
                if (radius > 3):
                    cv2.circle(frame, (int(centers[0]), int(centers[1])), int(radius), (36,255,5), 2)
                    output_file.write("%d,%d,%d,%d\n" % (frame_cnt, int(centers[0]), int(centers[1]), int(radius)))

        frame_cnt += 1
    output_file.close()
    #cv2.imshow('Thresh', frame)
    #LastFrameName = "LastFrame_" + output_file_name + ".jpg"
    #cv2.imwrite(LastFrameName, frame)


# release the video capture object
