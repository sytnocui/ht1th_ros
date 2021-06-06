#! /usr/bin/python3
#-*- coding:utf-8 _*-

"""
@author:Cui Baoyi
@time: 2021/03/20
"""

import numpy as np
import cv2
import cv2.aruco as aruco

dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)  # 编码点的类型,与生成的时候对应
K = np.array([[228.82, 0, 601.32],
              [0, 228.59, 363.39],
              [0, 0, 1]])
Dis = np.array([0.00490, 0.00105, 0.00012, 0.00047])
EMap = np.loadtxt('EMap.txt')

# 解算位姿的函数
def CalculatePositon(Point3D, Point2D, K, Dis):
	Center = np.mean(Point3D, axis=0)
	Point3D = Point3D - Center  # 去中心化
	ret, RvecW2C, tW2C = cv2.solvePnP(Point3D, Point2D, K, Dis)  # 解算位姿
	RW2C = cv2.Rodrigues(RvecW2C)[0]
	RC2W = np.linalg.inv(RW2C)
	tC2W = -np.linalg.inv(RW2C).dot(tW2C)
	CamPosition = tC2W.flatten() + Center  # 相机在世界坐标系下的坐标
	return CamPosition

def DealMarker(Img):
	CamPosition = None
	MarkerROI = None
	Corners, IDs, _ = aruco.detectMarkers(Img, dict)
	if len(Corners) != 0:  # 如果检测点
		Point3D = np.empty((0, 3))
		Point2D = np.empty((0, 2))

		for i, Corner in enumerate(Corners):  # 剔除超出索引的Aruco码
			ID = IDs.flatten()[i]
			if ID > 3:  # 判断是否为红绿灯上的Aruco码
				IDs = np.delete(IDs, (i), axis=0)
				del Corners[i]
				del Corner
				del ID

		for i, Corner in enumerate(Corners):
			Point2D = np.vstack((Point2D, Corner.reshape(-1, 2)))
			ID = IDs.flatten()[i]
			Point3D = np.vstack((Point3D, np.hstack((EMap[ID, 3:].reshape(-1, 2), np.zeros((4, 1))))))
			CamPosition = CalculatePositon(Point3D, Point2D, K, Dis)
			aruco.drawDetectedMarkers(Img,Corners,IDs)
			cv2.putText(Img, str(CamPosition), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
			MarkerROI = np.hstack((np.min(Point2D,axis=0),np.max(Point2D,axis=0))).astype(np.int)  # xmin,ymin,xmax,ymax
			#else:
			#	print('删除前的Corners:')
			#	print(Corners)
			#	IDs = np.delete(IDs, (i), axis=0)
			#	del Corners[i]
			#print(ID)
			#print(IDs)
			#print(Corners)
			#print(Corner)
	return CamPosition, MarkerROI
