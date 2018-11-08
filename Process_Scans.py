# Process_Scans.py
# Spencer Adams-Rand
# Written for Engs89
#

import math
import cv2
import glob

#scans must be 300 dpi, and done on the right scanner and stuff

def test_area(crop_area, test_image_path, key_image_path, thresh=90, debug=False): # don't forget thresh = 90 ya idiot
    img_list = [test_image_path, key_image_path]
    test_image = cv2.imread(test_image_path)
    draw_img = test_image[crop_area[0]:crop_area[1], crop_area[2]:crop_area[3]]
    datasets = []

    for img in img_list:

        image = cv2.imread(img)
        cropped = image[crop_area[0]:crop_area[1],crop_area[2]:crop_area[3]]

        # convert to gray scale and threshold
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        threshholded_immage = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

        if debug:
            cv2.imshow('thresholded',thresh)
            cv2.waitKey(0)

        line_points = []
        height_pixels, width_pixels = cropped.shape[:2]
        # find highest coordinate y value of black
        for c in range(width_pixels):
            for r in range(height_pixels):
                if threshholded_immage[r,c] == 0:
                    line_points.append((c,r))
                    break

        # for i in line_points:
        #     draw_img = cv2.circle(draw_img, i, 1, (255,0,0), thickness=-1, lineType=8, shift=0)

        x = [i[0] for i in line_points]
        y = [i[1] for i in line_points]
        trial_data = (x,y)
        datasets.append(trial_data)

    # compute average type 1 error:
    length = min(len(datasets[0][0]),len(datasets[1][0]))
    total_error = 0

    for val in range(length):

        draw_img = cv2.line(draw_img, (datasets[0][0][val],datasets[0][1][val]),
                            (datasets[1][0][val],datasets[1][1][val]), (255, 0, 0), thickness=1, lineType=8, shift=0)
        error_squared = (datasets[1][1][val] - datasets[0][1][val])**2
        actual_error = math.sqrt(error_squared)
        total_error += actual_error
    average_error_inch = total_error/(300*length)

    result_string = ("Mean error = %.3f inch" % average_error_inch)

    draw_img = cv2.putText(draw_img,result_string,(100,70),cv2.FONT_HERSHEY_SIMPLEX, 2, 255,thickness=5)
    return average_error_inch,draw_img


ki = "/home/spencer/PycharmProjects/Computer_Vision/Scanned_Tests/key.jpg" # path to key image

pathlist = glob.glob("/home/spencer/PycharmProjects/Computer_Vision/inputs/*.jpg")
tests = [(400,1400,300,2000),(400,1400,2900,4500),(2000,3000,300,2000)]

with open('outputs/Processed_Output.txt', 'w') as file:
    for p in pathlist:
        print("Currently processing image " + p)
        composite_image = cv2.imread(p)
        results_string = ""

        for t in tests:
            result = test_area(t,p,ki)
            results_string = results_string + str(result[0]) + ","
            composite_image[t[0]:t[1], t[2]:t[3]] = result[1]

        scaled = cv2.resize(composite_image, (0, 0), fx=0.25, fy=0.25)
        file_id = p[53:-4]

        file.write(file_id + "," + results_string + "\n")

        output_path = "/home/spencer/PycharmProjects/Computer_Vision/outputs/" + file_id + "_Processed.jpg"
        cv2.imwrite(output_path,composite_image)
        cv2.waitKey(0)

