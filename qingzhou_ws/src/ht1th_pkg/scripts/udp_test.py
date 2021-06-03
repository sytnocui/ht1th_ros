#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该例程设置/读取海龟例程中的参数

import sys
import os
import threading
import struct
import socket

import rospy
from geometry_msgs.msg import Twist

####################################################################################UDP
def udp_thread():#udp传输子线程函数
    timer = threading.Thread(target=udp_send)
    timer.start()

def udp_send():
    udp_viewpara_send()
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
    pass
#####################################################################################VISUAL
def cam_get():
    pass

def lane_check():
    #初始化Twist类型的消息
    vel_msg = Twist()
    vel_msg.linear.x=0.5
    vel_msg.angular.z=0.2
    #发布消息
    visual_vel_pub.publish(vel_msg)
    rospy.loginfo("[%0.2f m/s,%0.2f rad/s]",vel_msg.linear.x,vel_msg.angular.z)

def light_check():
    pass

#####################################################################################

if __name__=="__main__":
    #client 发送端初始化
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 8888)  # 接收方 服务器的ip地址和端口号

    #初始化ros节点
    rospy.init_node("ht1th_visual",anonymous=True)

    #创建一个Publisher,发布cmd_vel的topic,消息类型为geometry_msgs::Twist,没有队列
    visual_vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=None)

    #设置循环的频率
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if 1:
            #拍照
            cam_get()
            if 0:
                #红绿灯检测
                light_check()
                pass
            else:
                #车道线检测
                lane_check()
                pass
        
        udp_thread()

        #按照循环频率延时
        rate.sleep()