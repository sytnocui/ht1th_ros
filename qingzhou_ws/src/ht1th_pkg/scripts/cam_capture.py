#! /usr/bin/python3
#coding=utf-8

import cv2
import numpy as np

# 相机参数设定
Dist = np.array([-0.37959, 0.20457, 0.00046, -0.00029, 0.00000], dtype=np.float32)
K = np.array([[315.51468, 0, 326.07501],
              [0, 313.49477, 222.20442],
              [0, 0, 1]], dtype=np.float32)

def gstreamer_pipeline(  # 定义GStreamerPipeline
        capture_width=640,
        capture_height=480,
        display_width=640,
        display_height=480,
        framerate=21,
        flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )

def cam_capture():#拍摄照片函数
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    print(cap.isOpened())
    if cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            UndistImg = cv2.undistort(img, K, Dist)
            return UndistImg
