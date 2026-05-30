from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bringup_pkg = get_package_share_directory('warehouse_bringup')

    gazebo_robot_launch = os.path.join(
        bringup_pkg, 'launch', 'warehouse_simulation_camera.launch.py'
    )

    nav2_launch = os.path.join(
        bringup_pkg, 'launch', 'warehouse_navigation.launch.py'
    )

    gazebo_and_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_robot_launch)
    )

    nav2_delayed = TimerAction(
        period=40.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(nav2_launch)
            )
        ]
    )

    auto_initial_pose = TimerAction(
        period=50.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'topic', 'pub',
                    '--once',
                    '/initialpose',
                    'geometry_msgs/msg/PoseWithCovarianceStamped',
                    "{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.000076, y: -0.000005, z: 0.0}, orientation: {z: 0.0, w: 1.0}}, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0685]}}"
                ],
                output='screen'
            )
        ]
    )

    aruco_detector = TimerAction(
        period=55.0,
        actions=[
            Node(
                package='warehouse_perception',
                executable='aruco_station_detector',
                name='aruco_station_detector',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gazebo_and_robot,
        nav2_delayed,
        auto_initial_pose,
        aruco_detector
    ])