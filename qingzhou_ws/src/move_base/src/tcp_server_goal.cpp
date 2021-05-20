/*ROS*/
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
/*C*/
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cerrno>
#include <cstring>

#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>

void ros_setgoal(char buf[]);

int main() {
    std::cout << "This is server" << std::endl;
    // socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1) {
        std::cout << "Error: socket" << std::endl;
        return 0;
    }
    // bind
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(8888);
    addr.sin_addr.s_addr = INADDR_ANY;
    if (bind(listenfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        std::cout << "Error: bind" << std::endl;
        return 0;
    }
    // listen
    if(listen(listenfd, 5) == -1) {
        std::cout << "Error: listen" << std::endl;
        return 0;
    }
    // accept
    int conn;
    char clientIP[INET_ADDRSTRLEN] = "";
    struct sockaddr_in clientAddr;
    socklen_t clientAddrLen = sizeof(clientAddr);
    while (true) {
        std::cout << "...listening" << std::endl;
        conn = accept(listenfd, (struct sockaddr*)&clientAddr, &clientAddrLen);
        if (conn < 0) {
            std::cout << "Error: accept" << std::endl;
            continue;
        }
        inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);
        std::cout << "...connect " << clientIP << ":" << ntohs(clientAddr.sin_port) << std::endl;

        char buf[255];
        while (true) {
            memset(buf, 0, sizeof(buf));
            int len = recv(conn, buf, sizeof(buf), 0);
            buf[len] = '\0';
            

            //根据接收的信息执行命令
            switch (buf[0]){//改成传地址
            case 0x30:ros_setgoal(buf);break;
            case 0x40:ros_setgoal(buf);break;
            case 0x50:ros_setgoal(buf);break;
            default:break;
            }
        }
        close(conn);
    }
    close(listenfd);
    return 0;
}

void ros_setgoal(char buf[])
{
    float tcp_x,tcp_y = 0;
    char *tcp_x_b = NULL;
    char *tcp_y_b = NULL;
    tcp_x_b = &buf[1];
    tcp_y_b = &buf[5];
    memcpy(&tcp_x, tcp_x_b, sizeof(float));
    memcpy(&tcp_y, tcp_y_b, sizeof(float));

    std::cout << tcp_x << " " << tcp_y << std::endl;

    int argc = 0;
    char** argv = NULL;
    ros::init(argc, argv, "tcp_server_goal");
    //tell the action client that we want to spin a thread by default
    MoveBaseClient ac("move_base", true);
    //wait for the action server to come up
    while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
    }

    move_base_msgs::MoveBaseGoal goal;

    //we'll send a goal to the robot to move 1 meter forward
    goal.target_pose.header.frame_id = "map";
    goal.target_pose.header.stamp = ros::Time::now();
    goal.target_pose.pose.position.x = tcp_x;
    goal.target_pose.pose.position.y = tcp_y;
    goal.target_pose.pose.orientation.w = 1.0;

    ROS_INFO("Sending goal");
    ac.sendGoal(goal);
    ac.waitForResult();

    if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    ROS_INFO("Hooray, the base moved 1 meter forward");
    else
    ROS_INFO("The base failed to move forward 1 meter for some reason");

    return;
}