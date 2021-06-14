#! /usr/bin/python3
# -*- coding:utf-8 _*-

# 该例程设置/读取海龟例程中的参数

import sys
import os
import threading
import struct
import socket
import time

import rospy
#import tf

from geometry_msgs.msg import Twist

#视觉代码
from cam_capture import *
from lane_check_opencv import *
from light_check import *

####################################################################################UDP
def udp_thread():#udp传输子线程函数
    timer = threading.Thread(target=udp_send)
    timer.start()

def udp_send():
    udp_viewpara_send()
    time.sleep(0.1)
    udp_img_send()

def udp_viewpara_send():
    viewpara = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    #读取参数服务器
    viewpara[0] = rospy.get_param("/ht1th/viewpara/nav_state")
    viewpara[1] = rospy.get_param("/ht1th/viewpara/visual_state")
    viewpara[2] = rospy.get_param("/ht1th/viewpara/pose_x")
    viewpara[3] = rospy.get_param("/ht1th/viewpara/pose_y")
    viewpara[4] = rospy.get_param("/ht1th/viewpara/pose_yaw")
    viewpara[5] = rospy.get_param("/ht1th/viewpara/vel_left")
    viewpara[6] = rospy.get_param("/ht1th/viewpara/vel_right")
    viewpara[7] = rospy.get_param("/ht1th/viewpara/vel_angle")
    rospy.loginfo(viewpara)
    msg = struct.pack("<8f",*viewpara)
    client_socket.sendto(msg, server_address) #将msg内容发送给指定接收方

def udp_img_send():
    resizedImg = cv2.resize(ImgOri, (int(ImgOri.shape[1]/4), int(ImgOri.shape[0]/4)))
    client_socket.sendto(resizedImg, server_address)
#####################################################################################VISUAL
#0-close   1-light_en   2-light_dis   5-check_lane   6-lane

#TODO:测试参数服务器设置时间
def light_check(ImgOri):
    isWait = LightDetect(ImgOri)
    #TODO：加什么时候赋成pass_light
    # pass
    if isWait:
        rospy.set_param("/ht1th/viewpara/visual_state",1)#可通行1
    else:
        rospy.set_param("/ht1th/viewpara/visual_state",2)#不可通行2

def lane_check(ImgOri):
    isNaN , lane_position = TrafficLinePosition(ImgOri)
    if isNaN == 0:
        rospy.set_param("/ht1th/viewpara/visual_state",5)#结尾如果没检测到车道线就赋成5
    else:
        print('lane_position:', lane_position)
        if -400<lane_position<400:
            lane_angular = 0.001 * lane_position#TODO:计算角速度
        else:
            lane_angular = 0
        rospy.set_param("/ht1th/viewpara/visual_state",6)#检测到车道线赋为6
        #发布话题
        vel_msg = Twist()
        vel_msg.linear.x=0.3#TODO:更改速度
        vel_msg.angular.z= lane_angular
        visual_vel_pub.publish(vel_msg)
        rospy.loginfo("[%0.2f m/s,%0.2f rad/s]",vel_msg.linear.x,vel_msg.angular.z)

#####################################################################################

def robot_tf_update():
   pose_x = rospy.get_param('/ht1th/viewpara/pose_x')
   pose_x = rospy.get_param('/ht1th/viewpara/pose_y')


if __name__=="__main__":
    # Restart GStreamer
    # os.system('sudo systemctl restart nvargus-daemon')
    #client 发送端初始化
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("192.168.43.86", 8888)  # 接收方 服务器的ip地址和端口号

    #初始化ros节点
    rospy.init_node("ht1th_visual",anonymous=True)

    #创建一个Publisher,发布cmd_vel的topic,消息类型为geometry_msgs::Twist,没有队列
    visual_vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=1)
    
    #tf
    pose_x = 0.0
    pose_y = 0.0
    pose_yaw = 0.0

    #设置循环的频率
    rate = rospy.Rate(10)
    
    ImgOri = cam_capture()
    cv2.waitKey(10)
    print(ImgOri.shape)
    while not rospy.is_shutdown():
        #0-stop    1-towait     2-toload    3-tounload   4-reached    5-pass_light    6-wrong 
        nav_state = rospy.get_param("/ht1th/viewpara/nav_state")#获取机器人状态
        if (nav_state == 1) or (nav_state == 3):
            ImgOri = cam_capture()#拍照
            cv2.waitKey(10)
            # print(type(ImgOri))
            
            # print(ImgOri.shape)
            print('Camera Opened')
            if nav_state == 3:#前往卸货区
                if pose_x <= 1.3 and pose_y <= -7.5:
                   rospy.set_param('/ht1th/viewpara/nav_state', 5)
                light_check(ImgOri)#红绿灯检测
            elif nav_state == 1: #and pose_y >= -5:#前往等待区
                if pose_y >= -1:
                    rospy.set_param('/ht1th/viewpara/nav_state', 6)
                lane_check(ImgOri)#车道线检测
        
        robot_tf_update()

        udp_thread()

        #按照循环频率延时
        rate.sleep()
