#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该例程设置/读取海龟例程中的参数

import sys
import rospy
from std_srvs.srv import Empty

if __name__=="__main__":

    rospy.init_node("viewpara",anonymous=True)

    viewpara = []

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