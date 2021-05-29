#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该例程设置/读取海龟例程中的参数

import sys
import rospy
from std_srvs.srv import Empty

import struct
import socket
import time

if __name__=="__main__":
    rospy.init_node("viewpara",anonymous=True)

    #client 发送端
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 8888)  # 接收方 服务器的ip地址和端口号

    viewpara = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

    while True:
        #读取参数服务器
        viewpara[0] = rospy.get_param("/ht1th/viewpara/robot_state")
        viewpara[1] = rospy.get_param("/ht1th/viewpara/visual_nav")
        viewpara[2] = rospy.get_param("/ht1th/viewpara/pose_x")
        viewpara[3] = rospy.get_param("/ht1th/viewpara/pose_y")
        viewpara[4] = rospy.get_param("/ht1th/viewpara/pose_yaw")
        viewpara[5] = rospy.get_param("/ht1th/viewpara/vel_left")
        viewpara[6] = rospy.get_param("/ht1th/viewpara/vel_right")
        viewpara[7] = rospy.get_param("/ht1th/viewpara/vel_angle")
        rospy.loginfo(viewpara)
        msg = struct.pack("<8f",viewpara[0],viewpara[1],viewpara[2],viewpara[3],viewpara[4],viewpara[5],viewpara[6],viewpara[7])
        client_socket.sendto(msg, server_address) #将msg内容发送给指定接收方
        time.sleep(1)



    