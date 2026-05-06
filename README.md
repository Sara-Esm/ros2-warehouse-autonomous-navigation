# Autonomous Warehouse Navigation with ROS 2 Nav2

## Overview

This project demonstrates an autonomous mobile robot navigating a realistic warehouse environment using ROS 2 Humble, Gazebo, TurtleBot3, and the Nav2 navigation stack.

The robot is capable of localizing itself on a map, planning safe paths, avoiding obstacles, and autonomously navigating between multiple warehouse destinations such as a charging station, loading zone, shelf inspection points, and central warehouse aisles.

---

# Demo Features

The system successfully demonstrates:

- TurtleBot3 autonomous navigation
- Warehouse simulation in Gazebo
- AMCL localization using RViz
- Nav2 path planning
- Obstacle avoidance
- Multi-goal autonomous missions
- Goal monitoring and logging
- Return-to-charging-station workflow

---

# Technologies Used

| Technology | Purpose |
|---|---|
| ROS 2 Humble | Robotics middleware |
| Nav2 | Autonomous navigation stack |
| Gazebo 11 | Robot simulation |
| TurtleBot3 | Mobile robot platform |
| RViz2 | Visualization and localization |
| Python | Autonomous mission scripting |
| AMCL | Localization |
| Git & GitHub | Version control and portfolio |

---

# System Architecture

```text
Warehouse Mission Node
        |
        v
Nav2 Action Server
        |
        v
Global Planner ---> Local Planner
        |
        v
AMCL Localization
        |
        v
Gazebo Warehouse Simulation
```

---

# Warehouse Mission Workflow

The robot autonomously performs the following mission:

1. Start from initial position
2. Navigate to charging station
3. Navigate to loading zone
4. Navigate to shelf inspection point A
5. Navigate to shelf inspection point B
6. Navigate to central warehouse aisle
7. Return to charging station
8. Complete mission

---

# Workspace Structure

```text
warehouse_ws/
├── README.md
├── scripts/
│   └── run_stable_nav2.sh
├── media/
├── docs/
└── src/
    ├── turtlebot3/
    ├── warehouse_bringup/
    ├── warehouse_gazebo/
    └── aws-robomaker-small-warehouse-world/
```

---

# Important Packages

## warehouse_bringup

Contains:

- Autonomous mission node
- Launch files
- Nav2 integration
- Multi-goal mission execution

Main node:

```text
warehouse_autonomy_node.py
```

---

## warehouse_gazebo

Contains:

- Warehouse Gazebo world
- Robot spawning launch files
- Warehouse simulation assets
- Custom environment configuration

---

# Autonomous Navigation Node

The custom Python node sends navigation goals to Nav2 using the ROS 2 action interface.

Main capabilities:

- Send sequential navigation goals
- Wait for robot arrival
- Monitor mission progress
- Log mission execution
- Return final status

Example output:

```text
Sending robot to Charging Station...
ARRIVED: Charging Station

Sending robot to Loading Zone...
ARRIVED: Loading Zone

MISSION COMPLETE
```

---

# Robot Destinations

| Destination | X | Y |
|---|---|---|
| Charging Station | -7.131 | -6.491 |
| Loading Zone | 9.785 | -2.849 |
| Shelf A Inspection | 0.493 | -0.944 |
| Shelf B Inspection | 2.997 | -6.240 |
| Central Warehouse Aisle | 2.359 | -2.495 |

---

# How to Build

## Clone Workspace

```bash
mkdir -p ~/projects/warehouse_ws/src
cd ~/projects/warehouse_ws/src
```

---

## Build Workspace

```bash
cd ~/projects/warehouse_ws

source /opt/ros/humble/setup.bash

colcon build
```

---

## Source Workspace

```bash
source install/setup.bash
```

---

# Run the Project

## Launch Full Navigation System

```bash
ros2 launch warehouse_bringup warehouse_full_system.launch.py
```

---

## Localize Robot in RViz

In RViz:

1. Click `2D Pose Estimate`
2. Click robot initial position
3. Drag orientation arrow

---

## Run Autonomous Mission

Open a new terminal:

```bash
cd ~/projects/warehouse_ws

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run warehouse_bringup warehouse_autonomy
```

---

# Navigation Debugging

Useful command for checking robot position:

```bash
ros2 topic echo /amcl_pose
```

Useful TF command:

```bash
ros2 run tf2_ros tf2_echo map base_link
```

---

# Challenges Solved During Development

This project involved solving several real robotics integration challenges:

- Nav2 action server connection issues
- Robot localization problems
- Goal rejection debugging
- Gazebo and RViz synchronization
- WSL2 graphical interface setup
- AMCL initialization workflow
- Workspace cleanup and package organization
- GitHub repository management

---

# Future Improvements

Potential future upgrades:

- Dynamic obstacle detection
- SLAM mapping
- Computer vision integration
- Autonomous docking
- Battery monitoring
- Task scheduling system
- Multi-robot coordination
- AI-based warehouse optimization

---

# Screenshots

Add screenshots inside:

```text
media/
```

Example screenshots:

- Gazebo warehouse environment
- RViz navigation
- Robot path planning
- Autonomous mission execution

---

# Learning Outcomes

This project provided hands-on experience with:

- ROS 2 architecture
- Nav2 stack integration
- Autonomous robotics systems
- Localization and navigation
- Simulation workflows
- Robotics software debugging
- Real-world robotics engineering workflow

---

# Author

Sara Esmaeili

Electrical and Control Engineer  
Robotics | ROS 2 | Autonomous Navigation | AI | Machine Learning

GitHub:
https://github.com/Sara-Esm

---

# License

This project is licensed under the MIT License.