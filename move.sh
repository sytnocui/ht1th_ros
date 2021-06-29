#!/bin/bash
roslaunch yocs_velocity_smoother standalone.launch &
echo "smooth starting success!"
sleep 6
roslaunch qingzhou_nav qingzhou_bringup.launch &
echo "bringup starting success!"
sleep 7

roslaunch qingzhou_nav qingzhou_move_base.launch &
echo "movebase starting success!"
sleep 7

roslaunch ht1th_pkg ht1th.launch
echo "ht1th starting success!"

wait 

exit 0
