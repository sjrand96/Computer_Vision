# import the necessary packages
from matplotlib import pyplot as plt
import math
import cv2
import glob

#/home/spencer/PycharmProjects/PongAMatic/venv/bin/python /home/spencer/PycharmProjects/Computer_Vision/Measure_Distance.py
# 0.05832549019607843
# 0.042270833333333334
# 0.05063921568627451
#
# 0.13503529411764706
# 0.07094166666666667
# 0.06845322327044025

# load images
img_list = ["/home/spencer/PycharmProjects/Computer_Vision/Scanned_Tests/SMacLean 0118110714180_0007.jpg",
            "/home/spencer/PycharmProjects/Computer_Vision/Scanned_Tests/key.jpg"]

datasets = []

tests = [(400,1400,300,2000),(400,1400,2900,4500),(2000,3000,300,2000)]

for crop_area in tests:
    datasets = []
    for image in img_list:
        image = cv2.imread(image)

        scaled = image[crop_area[0]:crop_area[1],crop_area[2]:crop_area[3]]

        # convert to gray scale and threshold
        gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow('thresholded',thresh)
        h_new, w_new = scaled.shape[:2]
        line_points = []

        # find highest coordinate y value of black
        for c in range(w_new):
            for r in range(h_new):
                if thresh[r,c] == 0:
                    line_points.append((c,r))
                    break

        # copy of image to draw on
        draw_img = scaled.copy()
        for i in line_points:
            draw_img = cv2.circle(draw_img, i, 1, (255,0,0), thickness=-1, lineType=8, shift=0)

        draw_img = cv2.resize(draw_img, None, fx=.25, fy=.25, interpolation=cv2.INTER_CUBIC)
        #cv2.imshow('draw image',draw_img)
        x = [i[0] for i in line_points]
        y = [i[1] for i in line_points]
        trial_data = (x,y)
        datasets.append(trial_data)

        cv2.waitKey(0)

        with open('d2.txt', 'w') as file:
            for i in line_points:
                file.write("%d,%d\n"%(i[0],i[1]))

    # compute average type 1 error:
    length = min(len(datasets[0][0]),len(datasets[1][0]))
    total_error = 0

    for val in range(length):
        error_squared = (datasets[1][1][val] - datasets[0][1][val])**2
        actual_error = math.sqrt(error_squared)
        total_error += actual_error

    average_error_inch = total_error/(300*length)
    print("Average error was %.3f inch" % average_error_inch)

    plt.scatter(datasets[0][0],datasets[0][1]) #,datasets[1][0],datasets[1][1])
    plt.scatter(datasets[1][0],datasets[1][1]) #,datasets[1][0],datasets[1][1])
    #plt.savefig('scan_output.png')
    plt.show()

