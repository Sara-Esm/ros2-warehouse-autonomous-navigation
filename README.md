# 🤖 ROS 2 Autonomous Warehouse Navigation System

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-11-orange)
![Nav2](https://img.shields.io/badge/Nav2-Autonomous_Navigation-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

> A fully autonomous warehouse inspection robot built with ROS 2 Humble, Nav2, and computer vision. The robot navigates to 4 warehouse stations, verifies each location using ArUco marker detection, and returns home — completing a full mission with zero human intervention.

---

## 📽️ Demo

> 

```
WAREHOUSE MISSION COMPLETE
Total mission steps: 5  |  Successful tasks: 5  |  Failed tasks: 0
```

---

## ✨ Features

- **Fully autonomous mission execution** — navigates 5 waypoints sequentially with no human input
- **Real-time ArUco marker detection** — OpenCV-based computer vision verifies each station visually
- **SLAM-built map** — warehouse map built using Google Cartographer
- **AMCL localization** — Monte Carlo particle filter for robust pose estimation
- **Nav2 navigation stack** — global path planning, local obstacle avoidance, and recovery behaviors
- **Automatic system initialization** — timed launch sequence brings up all nodes in correct order
- **Mission summary reporting** — logs successful/failed tasks with full traceability

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    warehouse_bringup                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │   Gazebo    │  │     Nav2     │  │  Autonomy Node    │  │
│  │ Simulation  │  │   Stack      │  │  (Mission Manager)│  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬──────────┘  │
│         │                │                    │             │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌────────▼──────────┐  │
│  │ TurtleBot3  │  │ AMCL + Map   │  │  NavigateToPose   │  │
│  │  burger_cam │  │    Server    │  │   Action Client   │  │
│  └──────┬──────┘  └──────────────┘  └───────────────────┘  │
│         │                                                   │
│  ┌──────▼──────────────────┐                               │
│  │   warehouse_perception   │                               │
│  │  ArUco Station Detector  │                               │
│  │  /camera/image_raw  →   │                               │
│  │  /warehouse/marker_id   │                               │
│  └─────────────────────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

### ROS 2 Topic Graph

| Topic | Type | Description |
|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | Robot camera feed |
| `/warehouse/marker_detected` | `std_msgs/Bool` | ArUco detection status |
| `/warehouse/marker_id` | `std_msgs/Int32` | Detected marker ID |
| `/navigate_to_pose` | `nav2_msgs/NavigateToPose` | Nav2 goal action |
| `/amcl_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Robot localization |
| `/map` | `nav_msgs/OccupancyGrid` | SLAM-built map |
| `/scan` | `sensor_msgs/LaserScan` | LiDAR for obstacle detection |

---

## 📦 Package Structure

```
warehouse_ws/
├── warehouse_bringup/          # Launch files, maps, mission autonomy node
│   ├── launch/
│   │   ├── warehouse_robot_system_camera.launch.py   # Full system launch
│   │   ├── warehouse_navigation.launch.py            # Nav2 only
│   │   └── warehouse_simulation_camera.launch.py     # Gazebo only
│   ├── maps/
│   │   ├── warehouse_map.pgm   # SLAM-built occupancy grid
│   │   └── warehouse_map.yaml  # Map metadata (origin, resolution)
│   └── warehouse_bringup/
│       └── warehouse_autonomy_node.py   # Mission orchestration node
│
├── warehouse_gazebo/           # Simulation environment
│   ├── worlds/
│   │   └── small_warehouse.world   # AWS warehouse environment
│   └── models/
│       ├── aruco_marker_0/     # Charging dock marker (DICT_5X5_50, ID 0)
│       ├── aruco_marker_1/     # Loading zone marker (ID 1)
│       ├── aruco_marker_2/     # Inventory station marker (ID 2)
│       └── aruco_marker_3/     # Dispatch zone marker (ID 3)
│
├── warehouse_perception/       # Computer vision
│   └── warehouse_perception/
│       └── aruco_station_detector.py   # Real-time ArUco detection node
│
├── warehouse_mission/          # Mission definitions
└── warehouse_docking/          # Docking behavior
```

---

## 🗺️ Warehouse Mission

The robot executes a 5-step autonomous inspection mission:

```
[START] Robot spawns at origin (0, 0)
    │
    ▼
[STEP 1] Navigate to Home Charging Dock      → Verify ArUco ID 0
    │
    ▼
[STEP 2] Navigate to Loading Zone            → Verify ArUco ID 1
    │
    ▼
[STEP 3] Navigate to Inventory Scan Station  → Verify ArUco ID 2
    │
    ▼
[STEP 4] Navigate to Dispatch Zone           → Verify ArUco ID 3
    │
    ▼
[STEP 5] Return to Home Charging Dock        → Verify ArUco ID 0
    │
    ▼
[COMPLETE] Mission summary logged
```

Each station is verified by detecting the expected ArUco marker ID within an 8-second window using the robot's onboard camera.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Robot OS | ROS 2 Humble Hawksbill |
| Navigation | Nav2 (NavFn planner, DWB controller, AMCL) |
| Simulation | Gazebo Classic 11 |
| SLAM | Google Cartographer |
| Computer Vision | OpenCV 4, ArUco (DICT_5X5_50) |
| Robot Model | TurtleBot3 Burger with camera |
| Language | Python 3 |
| Platform | Ubuntu 22.04 / WSL2 |

---

## 🚀 Getting Started

### Prerequisites

```bash
# ROS 2 Humble
sudo apt install ros-humble-desktop

# Nav2
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup

# TurtleBot3
sudo apt install ros-humble-turtlebot3*

# Gazebo
sudo apt install ros-humble-gazebo-ros-pkgs

# OpenCV / CV Bridge
sudo apt install python3-opencv ros-humble-cv-bridge
```

### Build

```bash
mkdir -p ~/warehouse_ws/src
cd ~/warehouse_ws/src
git clone https://github.com/zesmaeili/ros2-warehouse-autonomous-navigation.git .

cd ~/warehouse_ws
colcon build
source install/setup.bash
```

### Run

**Terminal 1 — Launch full system (Gazebo + Nav2 + RViz + ArUco detector):**
```bash
export TURTLEBOT3_MODEL=burger_cam
ros2 launch warehouse_bringup warehouse_robot_system_camera.launch.py
```

Wait ~60 seconds for all nodes to initialize.

**Terminal 2 — Start autonomous mission:**
```bash
source install/setup.bash
ros2 run warehouse_bringup warehouse_autonomy
```

The robot will autonomously complete all 5 mission steps.

### Build Map (Optional — map already included)

```bash
# Terminal 1
ros2 launch warehouse_bringup warehouse_simulation_camera.launch.py

# Terminal 2
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=true

# Terminal 3
ros2 launch turtlebot3_cartographer occupancy_grid.launch.py use_sim_time:=true

# Terminal 4 — Teleoperate to map the environment
ros2 run turtlebot3_teleop teleop_keyboard

# Save map
ros2 run nav2_map_server map_saver_cli -f ~/warehouse_ws/src/warehouse_bringup/maps/warehouse_map
```

---

## 📊 Results

| Metric | Value |
|---|---|
| Mission success rate | 5/5 tasks (100%) |
| Stations with ArUco verification | 4/4 |
| Navigation recoveries | 0 |
| Map resolution | 0.05 m/pixel |
| Map size | 318 × 439 pixels |
| Localization method | AMCL (Monte Carlo) |

---

## 🔑 Key Implementation Details

**Mission Orchestration** (`warehouse_autonomy_node.py`)
- Uses `NavigateToPose` action client for non-blocking navigation
- Callback-driven state machine advances through waypoints on goal completion
- 8-second vision verification window at each station with graceful timeout handling

**ArUco Detection** (`aruco_station_detector.py`)
- Subscribes to `/camera/image_raw`, publishes to `/warehouse/marker_detected` and `/warehouse/marker_id`
- Tuned `DetectorParameters` for reliable detection in Gazebo's simulated camera
- `CORNER_REFINE_SUBPIX` for sub-pixel corner accuracy
- Real-time debug visualization window

**Navigation Configuration**
- `xy_goal_tolerance: 0.05m`, `yaw_goal_tolerance: 0.05 rad` for precise station stopping
- `inflation_radius: 0.2m` tuned to allow close-wall navigation for marker inspection
- Timed launch sequence: Gazebo (0s) → Nav2 (40s) → Initial pose (50s) → ArUco detector (55s)

---

## 🔭 Future Work

- [ ] Dynamic task allocation based on inventory status
- [ ] Multi-robot coordination
- [ ] True docking controller with precision alignment
- [ ] Object detection beyond ArUco (YOLO-based inventory scanning)
- [ ] Autonomous recovery and marker search behavior
- [ ] ROS 2 lifecycle node management
- [ ] Unit and integration tests

---

## 👩‍💻 Author

**Sara Esmaeili** — Robotics Software Engineer  
Published research: Sliding Mode Control, Fuzzy Logic, FPGA Systems  
GitHub: [@zesmaeili](https://github.com/zesmaeili)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.


# Overview

This project demonstrates an autonomous mobile robot navigating a realistic warehouse environment using ROS 2 Humble, Gazebo, TurtleBot3, and the Nav2 navigation stack.

The robot is capable of localizing itself on a map, planning safe paths, avoiding obstacles, and autonomously navigating between multiple warehouse destinations such as a charging station, loading zone, shelf inspection points, and central warehouse aisles.

---

# Project Motivation

The goal of this project was to build a complete autonomous warehouse navigation system using ROS 2 and Nav2 while gaining hands-on experience with localization, path planning, autonomous mission execution, simulation, debugging, and robotics software integration.

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
| Git & GitHub | Version control |

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

# License

This project is licensed under the MIT License.
