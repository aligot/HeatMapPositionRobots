import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])

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
			cv2.circle(image, (int(centers[0]), int(centers[1])), int(radius), (0,0,255), 2)
			print(radius)


	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)
