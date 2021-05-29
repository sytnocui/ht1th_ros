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
void ros_ctrlpara_modify(char buf[]);

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
            /////////////////////////目标点指定///////////////////////////////////
            case 0x30:  ros_setgoal(buf);break;//前往等待区
            case 0x40:  ros_setgoal(buf);break;//前往装货区
            case 0x50:  ros_setgoal(buf);break;//前往卸货区
            /////////////////////////简单命令////////////////////////////////////
            case 0x01:  printf("wdnmd");break;//复位
            case 0x10:  printf("wdnmd");break;//运行
            case 0x20:  printf("wdnmd");break;//停车
            case 0x60:  printf("wdnmd");break;//打开视频
            case 0x70:  printf("wdnmd");break;//关闭视频
            /////////////////////////修改参数////////////////////////////////////
            case 0x77:  ros_ctrlpara_modify(buf);break;//修改参数
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

    switch (buf[0]){
    case 0x30:  goal.target_pose.pose.orientation.w = 1;
                break;//前往等待区
    case 0x40:  goal.target_pose.pose.orientation.w = 0.707;
                goal.target_pose.pose.orientation.z = -0.707;
                break;//前往装货区
    case 0x50:  goal.target_pose.pose.orientation.w = 0.707;
                goal.target_pose.pose.orientation.z = 0.707;
                break;//前往卸货区
    default:break;
    }

    ROS_INFO("Sending goal");
    ac.sendGoal(goal);
    ac.waitForResult();

    if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
    ROS_INFO("Hooray, the base moved 1 meter forward");
    else
    ROS_INFO("The base failed to move forward 1 meter for some reason");

    return;
}

#define CTRLPARA_NUM 6 //控制参数的个数

void ros_ctrlpara_modify(char buf[])
{
    //使用数组
    float ctrlpara[CTRLPARA_NUM] ={0};//存储传回来的值的数组
    char *pctrlpara = NULL;//指针
    //循环赋值
    for(int i=0;i<CTRLPARA_NUM;i++)
    {
        pctrlpara = &buf[i*4+1];
        memcpy(&ctrlpara[i], pctrlpara, sizeof(float));
    }
    
    //ROS节点初始化
    int argc = 0;
    char** argv = NULL;
    ros::init(argc,argv,"ctrlpara_modify");
    //创建节点句柄，到底是啥意思？？？？？？？？？？？？？
    ros::NodeHandle node;

    //设置背景颜色参数
    ros::param::set("/ht1th/ctrlpara/test0",ctrlpara[0]);
    ros::param::set("/ht1th/ctrlpara/test1",ctrlpara[1]);
    ros::param::set("/ht1th/ctrlpara/test2",ctrlpara[2]);
    ros::param::set("/ht1th/ctrlpara/test3",ctrlpara[3]);
    ros::param::set("/ht1th/ctrlpara/test4",ctrlpara[4]);
    ros::param::set("/ht1th/ctrlpara/test5",ctrlpara[5]);

    //读取背景颜色参数
    ros::param::get("/ht1th/ctrlpara/test0",ctrlpara[0]);
    ros::param::get("/ht1th/ctrlpara/test1",ctrlpara[1]);
    ros::param::get("/ht1th/ctrlpara/test2",ctrlpara[2]);
    ros::param::get("/ht1th/ctrlpara/test3",ctrlpara[3]);
    ros::param::get("/ht1th/ctrlpara/test4",ctrlpara[4]);
    ros::param::get("/ht1th/ctrlpara/test5",ctrlpara[5]);
    ROS_INFO("Get Backgroud Color[%.2f,%.2f,%.2f,%.2f,%.2f,%.2f]",
    ctrlpara[0], ctrlpara[1], ctrlpara[2],ctrlpara[3],ctrlpara[4],ctrlpara[5]);
}