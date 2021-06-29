#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <geometry_msgs/Twist.h>

//接收到订阅的消息后，会进入消息回调函数
void poseCallback(const move_base_msgs::MoveBaseActionFeedback &feedback)
{
	ros::param::set("/ht1th/viewpara/pose_x",feedback.feedback.base_position.pose.position.x);
	ros::param::set("/ht1th/viewpara/pose_y",feedback.feedback.base_position.pose.position.y);
	printf("[pose:%f,%f]",feedback.feedback.base_position.pose.position.x,feedback.feedback.base_position.pose.position.y);
}

int main(int argc, char **argv)
{
	// 初始化ROS节点
	ros::init(argc, argv, "pose_subscriber");
	// 创建节点句柄
	ros::NodeHandle n;
	// 创建一个Publisher，订阅名为/turtle1/pose的topic，注册回调函数poseCallback
	ros::Subscriber pose_sub = n.subscribe("/move_base/feedback",1,poseCallback);
	// 循环等待回调函数
	ros::spin();

	return 0;
}
//move_base_msgs/MoveBaseActionFeedback

