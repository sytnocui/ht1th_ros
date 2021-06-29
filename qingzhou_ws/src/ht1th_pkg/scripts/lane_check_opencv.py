#! /usr/bin/python3
# -*- coding:utf-8 _*-

import numpy as np
import cv2


H = np.array([[-0.51050696, -2.11815651, 642.48018518],
              [0.00253205, 0.04427529, -167.26350596],
              [-0.00008633, -0.00427193, 1.]])

Dist = np.array([-0.37959, 0.20457, 0.00046, -0.00029, 0.00000], dtype=np.float32)
K = np.array([[315.51468, 0, 326.07501],
              [0, 313.49477, 222.20442],
              [0, 0, 1]], dtype=np.float32)


def TrafficLinePosition(ImgOri):
    WarpedImg = cv2.warpPerspective(ImgOri, H, (1000, 1000))
    ImgGray = cv2.cvtColor(WarpedImg, cv2.COLOR_BGR2GRAY)
    th, MaskImg = cv2.threshold(ImgGray, 165, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    MaskImg = cv2.dilate(MaskImg, kernel, iterations=1)
    MaskImg = cv2.erode(MaskImg, kernel, iterations=2)
    MaskImg = cv2.dilate(MaskImg, kernel, iterations=1)
    TestPosition2 = 400
    TestPosition1 = TestPosition2 - 50
    TestPosition3 = TestPosition2 + 50
    LinePosition1 = np.where(MaskImg[TestPosition1, :] > 0)
    LinePosition2 = np.where(MaskImg[TestPosition2, :] > 0)
    LinePosition3 = np.where(MaskImg[TestPosition3, :] > 0)
    isNaN1 = np.size(LinePosition1)
    isNaN2 = np.size(LinePosition2)
    isNaN3 = np.size(LinePosition3)
    isNaNList = [isNaN1, isNaN2, isNaN3]
    print('isNaNList:', isNaNList)
    isNaN = 0
    for i in isNaNList:
        if i != 0:
            isNaN = isNaN + 1
    print('isNaN:', isNaN)

    LinePosition1 = np.sum(LinePosition1) / np.size(LinePosition1) - 500
    LinePosition2 = np.sum(LinePosition2) / np.size(LinePosition2) - 500
    LinePosition3 = np.sum(LinePosition3) / np.size(LinePosition3) - 500
    LinePositions = [LinePosition1, LinePosition2, LinePosition3]
    LinePosition = 0
    for j in LinePositions:
        if np.isnan(j) == 0:
            LinePosition = LinePosition + j
    if isNaN != 0:
        LinePosition = LinePosition / isNaN
    LinePosition = -1*LinePosition
    print(LinePosition)
    if isNaN > 0:
        isNaN = 1
    if 50 < LinePosition < 400:
        print('Left')
    elif -50 > LinePosition > -400:
        print('Right')
    else:
        print('Straight')

    # cv2.imshow('MaskImg', MaskImg)
    # cv2.imshow('WarpedImg', WarpedImg)
    cv2.waitKey(10)
    return isNaN, LinePosition
