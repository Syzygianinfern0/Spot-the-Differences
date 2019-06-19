"""
Author Name : S P Sharan
Domain: Tronix
Sub-Domain: Signal Processing & ML

Functions:
    nothing - for the trackbar callback

Global Variables:
    UNO     - PySerial Instance
    matrix  - Storage of the led to be glown.
              [6][6] size
              1's in places to glown and 0's where not
    done    - Status of Code Termination

"""

import cv2
import numpy as np
import imutils
import serial
import time
import struct

UNO = serial.Serial('COM5')
time.sleep(2)
print('Arduino UNO Connected')


# Just for the callback for the createtrackbar call
def nothing():
    pass


matrix = np.zeros([6, 6], dtype=int)

cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("Area", "image", 29, 200, nothing)  # 29 - Optimum Value for given image
cv2.createTrackbar("Thresh", "image", 8, 200, nothing)  # 8  - Optimum Value for given image

done = 0
while not done:

    if cv2.waitKey(1) & 0xFF == 27:  # The quit line
        done = 1

    # READ THE IMAGE AND SPLIT
    # ----------------------- #

    ori = cv2.imread('Difference.png', -1)
    img = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
    cols = img.shape[1]
    right, left = ori[:, :int(cols / 2)], ori[:, int(cols / 2):]  # Splitting the image

    # FIND THE DIFFERENCE
    # ------------------ #
    """
    The difference is just the pixel-wise 
    subtraction. We do a two-way subtraction 
    to preserve differences between the two sides
    """
    diff = cv2.subtract(left, right) + cv2.subtract(right, left)
    cv2.imshow('diff', diff)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # REMOVE NOISE
    # ----------- #
    """
    A Threshold on the intensity of 
    the differences is created to neglect 
    noise. This is further eroded to give a 
    more favourable result
    """
    thresh = cv2.getTrackbarPos("Thresh", "image")
    retval, threshold = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 2), np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=1)

    # FIND THE CONTOURS
    # ---------------- #
    """Now that we have the binary image of the 
    favourable parts, it's time to generate contours.
    We get the minimum area from the user through the 
    trackbar
    """
    min_area = cv2.getTrackbarPos("Area", "image")
    cnts = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    filtered_cnts = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            filtered_cnts.append(c)
            # ^^^^^^^^ Our list of favourable contours

    # DRAW THE CONTOURS
    """
    We have circles where the difference is
    Also matrix variable needs to be made
    """
    for c in filtered_cnts:
        """
        Compute center and generate row and
        column block number. 
        """
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.circle(ori, (cX, cY), 25, (0, 255, 0), 2)   # Draw a circle at the difference

        for i in range(0, right.shape[0], int(right.shape[0] / 6)):
            if cY <= i:
                break
        i = round(i * 6 / right.shape[0])               # conversion to an int containing the row
                                                        # block number in a 6x6 matrix

        for j in range(0, right.shape[1], int(right.shape[1] / 6)):
            if cX <= j:
                break
        j = round(j * 6 / right.shape[1])               # conversion to an int containing the column
                                                        # block number in a 6x6 matrix

        if done:
            matrix[i - 1][j - 1] = 1                    # Ones in the places with differences

    # RESULTS
    cv2.imshow('threshold', threshold)
    cv2.imshow('image', ori)
    if done:
        break

cv2.destroyAllWindows()
print(matrix)
time.sleep(2)
UNO.flush()
UNO.flushInput()
for i in range(6):
    for j in range(6):
        UNO.write(struct.pack('>B', matrix[i][j]))      # Sends the list after the proper encoding
UNO.flushOutput()
while True:
    print(UNO.readline())
