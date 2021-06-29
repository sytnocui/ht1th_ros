#! /usr/bin/python3
# -*- coding:utf-8 _*-
import cv2
import torch, os
from _02PipeDatasetLoader import *
from _03Unet import *
from PIL import Image

from cam_capture import *

# 设置参数
Device = torch.device('cuda:0')  # 指定CUDA设备
ModelPath = '/home/wheeltec/ht1th_ros/qingzhou_ws/src/ht1th_pkg/model/0200data3_best.pt'  # 模型路径

# 模型初始化
Unet = UNet(in_channels=1, out_channels=1, init_features=4, WithActivateLast=False, ActivateFunLast=torch.sigmoid).to(Device)
Unet.load_state_dict(torch.load(ModelPath, map_location=Device))

np.set_printoptions(suppress=True, precision=4)

# 逆透视参数设定
H = np.array([[  -0.61869793,   -2.24344654,  672.50410257],
              [   0.00583877,    0.05218149, -226.93620917],
              [  -0.00011433,   -0.00451613,    1.        ]])



InputImgSize = (128, 128)

# 模型输入的Transform方法
ImgTransform = transforms.Compose([
    transforms.Resize(InputImgSize),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.46], std=[0.10]),
])

# TODO 定义车道线检测函数

def TrafficLinePosition(ImgOri):
    ImgOri = cv2.cvtColor(ImgOri, cv2.COLOR_RGB2GRAY)
    ImgOri = cv2.flip(ImgOri, 1)
    ImgOri = cv2.warpPerspective(ImgOri, H, (1000,1000))
    ImgOri = Image.fromarray(ImgOri)
    fusionimg = ImgTransform(ImgOri)
    fusionimg = fusionimg.unsqueeze(dim=0)
    fusionimg = fusionimg.float().to('cuda')
    OutputImg = Unet(fusionimg)
    OutputImg = OutputImg.cpu().detach().numpy()[0, 0]
    OutputImg[OutputImg < 0] = 0
    OutputImg = (OutputImg * 255).astype(np.uint8)
    OutputImg = cv2.morphologyEx(OutputImg, cv2.MORPH_OPEN, kernel=(3,3), iterations=1)

    # 取testposition行检测车道线位置
    TestPosition2 = 60
    TestPosition1 = TestPosition2 - 8
    TestPosition3 = TestPosition2 + 8
    LinePosition1 = np.where(OutputImg[TestPosition1, :] > 0)
    LinePosition2 = np.where(OutputImg[TestPosition2, :] > 0)
    LinePosition3 = np.where(OutputImg[TestPosition3, :] > 0)
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

    LinePosition1 = np.sum(LinePosition1) / np.size(LinePosition1) - 64
    LinePosition2 = np.sum(LinePosition2) / np.size(LinePosition2) - 64
    LinePosition3 = np.sum(LinePosition3) / np.size(LinePosition3) - 64
    LinePositions = [LinePosition1, LinePosition2, LinePosition3]
    LinePosition = 0
    for j in LinePositions:
        if np.isnan(j) == 0:
            LinePosition = LinePosition + j
    if isNaN != 0:
        LinePosition = LinePosition / isNaN
    # LinePosition = -1 * LinePosition
    print(LinePosition)
    if isNaN > 0:
        isNaN = 1
    if 5 < LinePosition < 60:
        print('-----------Left-----------')
    elif -5 > LinePosition > -60:
        print('-----------Right-----------')
    else:
        print('-----------Straight-----------')
    cv2.waitKey(10)
    # 返回前瞻处偏差
    return isNaN , LinePosition
