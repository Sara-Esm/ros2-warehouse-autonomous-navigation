# Warehouse Autonomous Robot (ROS2 + Nav2)

Simulation (Gazebo world)
        ↓
Robot Spawn (TurtleBot3)
        ↓
TF + Robot State (robot_state_publisher)
        ↓
Localization (AMCL)
        ↓
Navigation (Nav2)
        ↓
Autonomous movement

## 🚀 Overview
Autonomous mobile robot navigating a warehouse using ROS2 Nav2 stack.

## 🧠 System Architecture
(diagram)

## 🛠️ Tech Stack
- ROS2 Humble
- Nav2
- Gazebo
- TurtleBot3

## ▶️ How to Run
ros2 launch warehouse_bringup warehouse_system.launch.py

## 🎯 Features
- Autonomous navigation
- Map-based localization (AMCL)
- Path planning (Nav2)
- Obstacle avoidance

## 🎥 Demo
(video link)

## 🔮 Future Work
- Multi-robot coordination
- Object detection integration
