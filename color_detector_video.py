import cv2
import argparse
import numpy as np

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

			boundaries = [
				([0, 255, 255], [0, 255, 255])
			]

			# loop over the boundaries
			for (lower, upper) in boundaries:
				# create NumPy arrays from the boundaries
				lower = np.array(lower, dtype = "uint8")
				upper = np.array(upper, dtype = "uint8")
				# find the colors within the specified boundaries and apply
				# the mask
				mask = cv2.inRange(image, lower, upper)
				output = cv2.bitwise_and(image, image, mask = mask)

				gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

				blur = cv2.medianBlur(gray, 3)
				sharpen_kernel = np.array([[-1,-1,-1], [-1,7.8,-1], [-1,-1,-1]])
				sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
				close = cv2.morphologyEx(sharpen, cv2.MORPH_CLOSE, kernel, iterations=2)


				cv2.imshow("gray", close)

				cnts = cv2.findContours(close, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
				nb_robots = 0
				for c in cnts:
					area = cv2.contourArea(c)
					x,y,w,h = cv2.boundingRect(c)
					centers, radius = cv2.minEnclosingCircle(c)
					if (radius < 10):
						#cv2.circle(image, (int(centers[0]), int(centers[1])), int(radius), (0,0,255), 2)
						output_file.write("%d,%d,%d,%d\n" % (frame_cnt, int(centers[0]), int(centers[1]), int(radius)))

	        frame_cnt += 1
		output_file.close()
