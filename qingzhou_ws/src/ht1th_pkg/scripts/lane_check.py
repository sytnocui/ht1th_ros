#! /usr/bin/python3
# -*- coding:utf-8 _*-

import torch, os
from _02PipeDatasetLoader import *
from _03Unet import *
from PIL import Image

from cam_capture import *

# 设置参数
Device = torch.device('cuda:0')  # 指定CUDA设备
ModelPath = '/home/wheeltec/ht1th_ros/qingzhou_ws/src/ht1th_pkg/model/0200.pt'  # 模型路径

# 模型初始化
Unet = UNet(in_channels=3, out_channels=1, init_features=4, WithActivateLast=True, ActivateFunLast=torch.sigmoid).to(Device)
Unet.load_state_dict(torch.load(ModelPath, map_location=Device))

# 逆透视参数设定
H = np.array([[-0.51050696, -2.11815651, 642.48018518],
              [0.00253205, 0.04427529, -167.26350596],
              [-0.00008633, -0.00427193, 1.]])


InputImgSize = (128, 128)

# 模型输入的Transform方法
ImgTransform = transforms.Compose([
    transforms.Resize(InputImgSize),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.46], std=[0.10]),
])

# TODO 定义车道线检测函数

def TrafficLinePosition(ImgOri):
    WarpedImg = cv2.warpPerspective(ImgOri, H, (1000, 1000))
    WarpedImg = Image.fromarray(cv2.cvtColor(WarpedImg, cv2.COLOR_BGR2RGB))
    InputTensor = ImgTransform(WarpedImg)
    InputTensor = np.expand_dims(InputTensor, 0)
    InputTensor = torch.from_numpy(InputTensor)
    InputImg = InputTensor.float().to(Device)
    OutputImg = Unet(InputImg)
    OutputImg = OutputImg.cpu().detach().numpy()[0, 0]
    OutputImg = (OutputImg * 255).astype(np.uint8)
    # Input = InputTensor.numpy()[0][0]
    # Input = (Normalization(Input) * 255).astype(np.uint8)
    # ResultImg = cv2.cvtColor(Input, cv2.COLOR_GRAY2RGB)
    OutputImg[OutputImg < 40] = 0
    # 取testposition行检测车道线位置
    testposition = 35
    LinePosition = np.where(OutputImg[testposition, :]>0)
    isNaN = np.size(LinePosition)#判断是否为nan
    LinePosition = np.sum(LinePosition)/np.size(LinePosition)
    # ResultImg[..., 2] = OutputImg * 3
    # cv2.imshow('Video', ResultImg)
    # cv2.waitKey(30)

    # 返回前瞻处偏差
    return isNaN , LinePosition
