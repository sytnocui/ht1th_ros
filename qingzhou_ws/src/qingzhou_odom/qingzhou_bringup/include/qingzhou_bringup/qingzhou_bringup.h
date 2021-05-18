#ifndef NODE_EXAMPLE_TALKER_H
#define NODE_EXAMPLE_TALKER_H

// ROS includes.
#include "ros/ros.h"
#include "ros/time.h"

#include <iostream>
#include <math.h>
#include <string.h>
#include <boost/asio.hpp>
#include <boost/bind.hpp>

#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/MagneticField.h>
#include <sensor_msgs/Range.h>

#include <geometry_msgs/Quaternion.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/PolygonStamped.h>
#include <geometry_msgs/Polygon.h>
#include <geometry_msgs/Point32.h>
#include <std_msgs/Float32.h>

//lib
#include <serial/serial.h>
#include <time.h>

#define CARL 0.31
#define CARW 0.325
#define PI 3.14159265
using namespace std;
using namespace boost::asio; 
using namespace boost;

typedef struct sMartcarControl{
  int TargetAngleDir;     //转向角度符号 0:直行；0x10:左转；0x20:右转  //not used
  int TargetAngle;        //角度
  int TargetSpeed;        //速度
  int TargetModeSelect;   //模式
  int TargetShiftPosition;
  bool control;
}sMartcarControl;        

 
class actuator
{
public:
  actuator(ros::NodeHandle nh);
  ~actuator();
  
  void run();

public:
     int m_baudrate;            
     std::string m_serialport;               //对应USB端口
     
     int encoderLeft;                        //左编码器
     int encoderRight;                       //右编码器
     int calibrate_lineSpeed;                //标定线速度
     int calibrate_angularSpeed;             //标定角速度
     float ticksPerMeter;                    //一米脉冲数
     float ticksPer2PI;                      //每圈脉冲数
     float linearSpeed;                      //线速度
     float angularSpeed;                     //角速度
     float batteryVoltage;                   //电池电压
       
     short tempaccelX,tempaccelY,tempaccelZ; //加速度缓存区
     short tempgyroX,tempgyroY,tempgyroZ;    //角速度缓存区
     short tempmagX,tempmagY,tempmagZ;       //磁力计缓存区
     double accelX,accelY,accelZ;            //加速度 
     double gyroX,gyroY,gyroZ;               //角速度 
     double magX,magY,magZ;                  //磁力计 

     double velDeltaTime;                    //时间，存放转换成秒的时间
     double detdistance,detth;               //计算距离和计算角度角度
     double detEncode;                           
     sMartcarControl carParasControl;           
  
     serial::Serial ser;                        
	 
     //msg
     sMartcarControl  moveBaseControl;          
     std_msgs::Float32  currentBattery;          

     //订阅话题
     ros::Subscriber sub_move_base;         
     
     //发布话题
     ros::Publisher pub_odom;              //发布odom topic
     ros::Publisher pub_imu;               //发布imu topic
     ros::Publisher pub_mag;               //发布磁力计 topic
     ros::Publisher pub_battery;           //发布电池 topic
     
     void pub_9250();                      //发布9250函数
     void recvCarInfoKernel();             //接收下位机发来数据函数
     void sendCarInfoKernel();             //发送小车数据到下位机函数

     void callback_move_base(const geometry_msgs::Twist::ConstPtr &msg);    //move_base回调函数
};

#endif 
