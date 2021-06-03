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
#0-close   1-check_light   2-red_light   3-green_light  4-yellow_light  5-check_lane   6-lane

#TODO:测试参数服务器设置时间
def cam_get():
    pass

def light_check():
    pass
    if 0:
        rospy.set_param("/ht1th/viewpara/visual_state",1)#结尾如果没检测到灯就赋成1
    elif 1:
        rospy.set_param("/ht1th/viewpara/visual_state",2)#检测到红灯赋为2
    elif 2:
        rospy.set_param("/ht1th/viewpara/visual_state",3)#检测到绿灯赋为3
    elif 3:
        rospy.set_param("/ht1th/viewpara/visual_state",4)#检测到黄灯赋为4

def lane_check():
    pass
    if 0:
        rospy.set_param("/ht1th/viewpara/visual_state",5)#结尾如果没检测到车道线就赋成5
    elif 1:
        rospy.set_param("/ht1th/viewpara/visual_state",6)#检测到车道线赋为6
        #发布话题
        vel_msg = Twist()
        vel_msg.linear.x=0.5
        vel_msg.angular.z=0.2
        visual_vel_pub.publish(vel_msg)
        rospy.loginfo("[%0.2f m/s,%0.2f rad/s]",vel_msg.linear.x,vel_msg.angular.z)

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
        #0-stop    1-towait     2-toload    3-tounload   4-reached   5-wrong
        nav_state = rospy.get_param("/ht1th/viewpara/nav_state")#获取机器人状态
        if nav_state == 1 or 3:
            cam_get()#拍照
            if nav_state == 3:#前往卸货区
                light_check()#红绿灯检测
            elif nav_state == 1:#前往等待区
                lane_check()#车道线检测
        
        udp_thread()

        #按照循环频率延时
        rate.sleep()