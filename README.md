# 🤖 ROS 2 Autonomous Warehouse Navigation System

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-11-orange)
![Nav2](https://img.shields.io/badge/Nav2-Autonomous_Navigation-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

> A fully autonomous warehouse inspection robot built with ROS 2 Humble, Nav2, and computer vision. The robot navigates to 4 warehouse stations, verifies each location using ArUco marker detection, and returns home — completing a full mission with zero human intervention.

---


## 📽️ Demo

<img width="1914" height="1030" alt="Desktop-screenshot-05-30-2026_05_02_PM" src="https://github.com/user-attachments/assets/dab35b3e-c798-4f6f-ab84-d8b0b9bfa21b" />


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
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │   Gazebo    │  │     Nav2     │  │  Autonomy Node    │   │
│  │ Simulation  │  │   Stack      │  │  (Mission Manager)│   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬──────────┘   │
│         │                │                    │             │
│  ┌──────▼──────┐  ┌──────▼───────┐  ┌────────▼──────────┐   │
│  │ TurtleBot3  │  │ AMCL + Map   │  │  NavigateToPose   │   │
│  │  burger_cam │  │    Server    │  │   Action Client   │   │
│  └──────┬──────┘  └──────────────┘  └───────────────────┘   │
│         │                                                   │
│  ┌──────▼──────────────────┐                                │
│  │   warehouse_perception  │                                │
│  │  ArUco Station Detector │                                │
│  │  /camera/image_raw  →   │                                │
│  │  /warehouse/marker_id   │                                │
│  └─────────────────────────┘                                │
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
git clone https://github.com/Sara-Esm/ros2-warehouse-autonomous-navigation.git .

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
- [ ] Autonomous recovery and marker search behaviour
- [ ] ROS 2 lifecycle node management
- [ ] Unit and integration tests

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.


