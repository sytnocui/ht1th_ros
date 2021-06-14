#! /usr/bin/python3
# -*- coding:utf-8 _*-

"""
@author:Cui Baoyi
@time: 2021/03/20
"""
import cv2
import numpy as np
import os
import sys

Red = np.array([38, 28, 230.])
Yellow = np.array([11, 81, 178.])
Green = np.array([35, 128, 10.]) # 35,128,10.
Colors = (Red, Yellow, Green)
ColorsName = ('Red', 'Yellow', 'Green')
DistThreshold = 8000    # 颜色距离阈值


def JudgeLightColor(Light):
	Dist = np.empty((0,))
	for Color in Colors:
		Dist = np.append(Dist, np.sum(abs(Color - Light) ** 2))
	return np.argmin(Dist), np.min(Dist)




def TrafficLight(MarkerROI, Img):
	LightColors = []
	LightImg = []
	if MarkerROI is not None:  # 如果检测到Marker，CamPosition和MarkerROI就不是None
		# global lastROI
		# lastROI = MarkerROI # 用全局变量lastROI保存前一时刻的状态
		# ROIdist = np.sum(abs(lastROI - MarkerROI) ** 2)
		# if ROIdist > 50:
		# 	MarkerROI = lastROI
		W = MarkerROI[2] - MarkerROI[0]
		H = MarkerROI[3] - MarkerROI[1]
		MinY = max(MarkerROI[1] - int(2.2 * H), 0)
		MaxY = min(MarkerROI[3] - H, Img.shape[0])
		if MaxY <= MinY + 10:
			return LightColors
		LightImg = Img[MinY:MaxY, MarkerROI[0]:MarkerROI[2], :]  # 提取交通灯的小块区域图像

		# 提取亮点中心轮廓
		LightImgGray = cv2.cvtColor(LightImg, cv2.COLOR_BGR2GRAY)
		#简单阈值 th, MaskImg = cv2.threshold(LightImgGray, 200, 255, cv2.THRESH_TOZERO)
		#高斯滤波 LightImgGray = cv2.GaussianBlur(LightImgGray, (5, 5), 0)
		th, MaskImg = cv2.threshold(LightImgGray, 170, 255, cv2.THRESH_TOZERO)
		#自适应阈值
		#MaskImg = cv2.adaptiveThreshold(LightImgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
		MaskImg = cv2.morphologyEx(MaskImg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
		contours, hierarchy = cv2.findContours(MaskImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		# a = cv2.findContours(MaskImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		# print(a)
		# exit()
		sel_contours = []

		# 根据面积筛选轮廓
		for index, contour in enumerate(contours):
			Area = cv2.contourArea(contour)
			Hull = cv2.convexHull(contour, False)
			HullArea = cv2.contourArea(Hull)
			if Area > 8 and Area < 100 and Area / HullArea > 0.8:
				sel_contours.append(contour)
				# 形态学提取外轮廓区域
				MaskImg = np.zeros_like(LightImgGray)
				cv2.drawContours(MaskImg, [contour], -1, 255, cv2.FILLED)
				kernel = np.ones((int(H / 8), int(H / 8)), np.uint8)
				dilation = cv2.dilate(MaskImg, kernel, iterations=1)  # 膨胀
				MaskImg = dilation - MaskImg
				MaskImg = cv2.cvtColor(MaskImg, cv2.COLOR_GRAY2BGR)
				OutSide = LightImg & MaskImg
				Index = np.argwhere(np.sum(OutSide, axis=2) > 0)
				GrayLevel = OutSide[Index[:, 0], Index[:, 1], :]
				Light = np.mean(GrayLevel, axis=0)
				Color, Dist = JudgeLightColor(Light)
				if Dist < DistThreshold:    # 颜色空间L2距离足够小，完成颜色判断
					LightColors.append(Color)

		# %% 显示交通灯小块区域
		cv2.drawContours(LightImg, sel_contours, -1, (255, 0, 0), 3)
		cv2.putText(Img, str([ColorsName[LightColor] for LightColor in LightColors]), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

		#cv2.imshow('LightImg', LightImg)
		cv2.waitKey(15)
		return LightColors, LightImg
