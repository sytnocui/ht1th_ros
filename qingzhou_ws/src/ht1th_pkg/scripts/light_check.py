#! /usr/bin/python3
# -*- coding:utf-8 _*-

from _02CalculatePositon import *
from _03TrafficLight import *

# from cam_capture import *

np.set_printoptions(suppress=True, precision=4)

def LightDetect(ImgOri):
    CamPosition, MarkerROI = DealMarker(ImgOri)  # CamPosition：(x,y,z)
    # %% 实现交通灯颜色检测
    if MarkerROI is not None:
        print('########ARUCO DETECTED!########')
        LightColors, LightImg = TrafficLight(MarkerROI, ImgOri)  # LightColors：0-'Red', 1-'Yellow', 2-'Green
        Distance = 0
        for Position in CamPosition:
            Distance = Distance + Position**2

        if (0 in LightColors) or (1 in LightColors):
            #TODO Distance阈值待定
            print('stop!')
            print('Distance:', Distance)
            return 0
    else:
        print('pass! Because MarkerROI is None!')
        return 1
    print('Pass because of other reasons')
    return 1
    
