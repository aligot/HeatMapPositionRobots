import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 3)
sharpen_kernel = np.array([[-1,-1,-1], [-1,7.8,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(sharpen, cv2.MORPH_CLOSE, kernel, iterations=2)

# Filtering the noise
filtered = cv2.fastNlMeansDenoising(close, None, 10, 7, 21)
kernel = np.ones((2,2),np.uint8)
erosion = cv2.erode(filtered,kernel,iterations = 5)
filtered = cv2.fastNlMeansDenoising(erosion, None, 10, 7, 21)


ret,final= cv2.threshold(filtered,40,255,0)

#cv2.imshow("final",final)

cnts = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]

nb_robots = 0
for c in cnts:
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c)
    centers, radius = cv2.minEnclosingCircle(c)
    if (radius > 3):
        cv2.circle(image, (int(centers[0]), int(centers[1])), int(radius), (36,255,5), 2)
        print(radius)
        nb_robots += 1

cv2.imwrite('OutputDetection.jpg', image)
print("Number of robots detected = ", nb_robots)
cv2.waitKey()
