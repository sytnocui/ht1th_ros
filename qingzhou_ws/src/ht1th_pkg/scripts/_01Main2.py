#! /usr/bin/python3
# coding=utf-8
"""
@Author  : Yu Tao
@Time    : 2020/3/19 11:37 
"""
import numpy as np
np.set_printoptions(suppress=True, precision=4)
import cv2, time, socket, json
import multiprocessing as mp
from _02GStreamer import *
import os

H = np.array([[-0.51050696, -2.11815651, 642.48018518],
              [0.00253205, 0.04427529, -167.26350596],
              [-0.00008633, -0.00427193, 1.]])

# 相机参数
Dist = np.array([-0.37959,   0.20457,   0.00046,   -0.00029,  0.00000 ], dtype=np.float32)
K = np.array([[315.51468, 0, 326.07501],
              [0, 313.49477, 222.20442],
              [0, 0, 1]], dtype=np.float32)

# Udp客户端
class Udp_send:
    def __init__(self, target):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target = target

    def send_line(self, line):
        time.sleep(0.001)
        self.udp_socket.sendto(line, self.target)

    def main(self, item):
        self.size = len(item)
        self.send_line(item)
        print(self.size)

    def close(self):
        self.udp_socket.close()

target = ('192.168.43.57', 8888)  # 要发送的地址

cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

udp_send = Udp_send(target)
if cap.isOpened():
	window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)

	while cv2.getWindowProperty('CSI Camera', 0) >= 0:
		ret, img = cap.read()
		img = cv2.undistort(img, K, Dist)
		resizedImg = cv2.resize(img, (int(img.shape[1] / 4), int(img.shape[0] / 4)))
		udp_send.main(resizedImg)
		cv2.imshow('CSI Camera', img)
		Key = cv2.waitKey(30) & 0xFF
		if Key == 27:# ESC键退出
			break

	cap.release()
	cv2.destroyAllWindows()


else:
	print('打开摄像头失败')

