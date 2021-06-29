#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/Twist.h>
int main(int argc, char** argv)
{
    // 初始化ROS节点
	ros::init(argc, argv, "ht1th_tf_listener");

    // 创建节点句柄
	ros::NodeHandle node;

    //创建tf的监听器
    tf::TransformListener listener;

    ros::Rate rate(10.0);
    while (node.ok())
    {
        //获取turtle1与turtle2坐标系间的tf数据
        tf::StampedTransform transform;
        try
        {
            listener.lookupTransform("/base_link","/map",ros::Time(0),transform);
        }
        catch(tf::TransformException &ex)
        {
            ROS_INFO("%s",ex.what());
            ros::Duration(1.0).sleep();
            continue;
        }
        ros::param::set("/ht1th/viewpara/pose_x",-transform.getOrigin().y());
        ros::param::set("/ht1th/viewpara/pose_y",transform.getOrigin().x());
        // ros::param::set("/ht1th/viewpara/pose_yaw",transform.getOrigin().yaw());

		rate.sleep();
        
    }
    return 0;
}
