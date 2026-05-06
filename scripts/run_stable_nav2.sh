#!/bin/bash

cd ~/projects/warehouse_ws || exit

source /opt/ros/humble/setup.bash
source install/setup.bash

export TURTLEBOT3_MODEL=burger

ros2 launch warehouse_bringup warehouse_full_system_STABLE_NAV2_SUCCESS.launch.py
