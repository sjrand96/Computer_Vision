# import the necessary packages
import argparse
#import imutils
import numpy as np
from matplotlib import pyplot as plt
import cv2
#
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to the input image")
# args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
# image = cv2.imread(args["image"])

img_list = ["/home/spencer/PycharmProjects/Computer_Vision/SMacLean 0118110121120_0001.jpg",
            "/home/spencer/PycharmProjects/Computer_Vision/SMacLean 0118110121120_0002.jpg",
            "/home/spencer/PycharmProjects/Computer_Vision/SMacLean 0118110121120_0003.jpg",
            "/home/spencer/PycharmProjects/Computer_Vision/SMacLean 0118110121120_0004.jpg",
            ]

datasets = []

for image in img_list:
    image = cv2.imread(image)
    # # Rotate and rescale
    # (h, w) = image.shape[:2]
    # center = (w / 2, h / 2)
    # M = cv2.getRotationMatrix2D(center, 90, 1.0)
    # rotated = cv2.warpAffine(image, M, (w, h))
    # scaled = cv2.resize(rotated,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
    #scaled = cv2.resize(image,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
    #scaled = scaled[110:720,0:600]

    # grayscale and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=170, param2=30, minRadius=80, maxRadius=200)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        print(i)
        # draw the outer circle
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), -1)
        # draw the center of the circle
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    scaled = cv2.resize(image,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('img',scaled)
    cv2.waitKey(0)

## Results:
# [1826  740   93]
# [340 408  94]
# [1588 2142   95]
# [ 516 2516   94]
# [336 410  95]
# [1586 2142   95]
# [1824  740   92]
# [ 514 2514   95]
# [340 408  95]
# [1826  738   94]
# [1588 2140   95]
# [ 516 2514   95]
# [1828  740   94]
# [340 408  95]
# [1590 2142   95]
# [ 516 2516   94]