from _02CalculatePositon import *
from _03TrafficLight import *

from cam_capture import *

np.set_printoptions(suppress=True, precision=4)

def LightDetect(ImgOri):
    CamPosition, MarkerROI = DealMarker(ImgOri)  # CamPosition：(x,y,z)
    # %% 实现交通灯颜色检测
    LightColors, LightImg = TrafficLight(MarkerROI, Img)  # LightColors：0-'Red', 1-'Yellow', 2-'Green'

    # LightImgName = 'TrafficLight'+str(Frame)+'.jpg'
    # cv2.imwrite(LightImgName, LightImg)
    print('Frame:', Frame)
    print(CamPosition, LightColors)     #
    # print(Img.shape)
    # 计算到红绿灯的距离
    Distance = 0
    for Position in CamPosition:
        Distance = Distance + Position**2

    if (0 or 1 in LightColors) and Distance>480000:
        #TODO Distance值待定
        return 0
    else:
        return 1

    # Img = cv2.resize(Img, (int(Img.shape[1] / 2), int(Img.shape[0] / 2)))
    # cv2.imshow('Video', Img)
    # key = cv2.waitKey(5)
    # if key != -1:
    #     exit()
    # if CamPosition is not None:
    # 	Point = ax.scatter(CamPosition[0], CamPosition[1], s=5)
    # 	plt.pause(0.01)
    # 	Point.remove()