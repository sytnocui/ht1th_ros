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
def udp_viewpara_send():
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

####################################################################################VISUAL
def lane_detection_thread():#车道线线程开启或结束函数
    #TODO:加入开启或关闭进程参数
    timer = threading.Thread(target=lane_detection)
    timer.start()

def lane_detection():
    #TODO: 加入车道线检测代码,不能把循环写死要留跳出条件
    #初始化ros节点
    rospy.init_node("ht1th_visual_lane",anonymous=True)
    #创建一个Publisher,发布cmd_vel的topic,消息类型为geometry_msgs::Twist,没有队列
    visual_vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=None)
    #设置循环的频率
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #初始化Twist类型的消息
        vel_msg = Twist()
        vel_msg.linear.x=0.5
        vel_msg.angular.z=0.2
		#发布消息
        visual_vel_pub.publish(vel_msg)
        rospy.loginfo("[%0.2f m/s,%0.2f rad/s]",vel_msg.linear.x,vel_msg.angular.z)
        #按照循环频率延时
        rate.sleep()

def light_detection_thread():#红绿灯线程开启或结束函数
    #TODO:加入开启或关闭进程参数
    timer = threading.Thread(target=light_detection)
    timer.start()

def light_detection():
    #TODO: 加入红绿灯检测代码,不能把循环写死要留跳出条件
    #初始化ros节点
    rospy.init_node("ht1th_visual_light",anonymous=True)
    #设置循环的频率
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #按照循环频率延时
        rate.sleep()
#####################################################################################
viewpara = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

#client 发送端初始化
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 8888)  # 接收方 服务器的ip地址和端口号

#TODO:全局变量写在main下面行吗
if __name__=="__main__":

    while True:
        udp_viewpara_send()