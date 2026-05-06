from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_warehouse = get_package_share_directory('warehouse_gazebo')
    pkg_tb3 = get_package_share_directory('turtlebot3_gazebo')

    world = os.path.join(pkg_warehouse, 'worlds', 'small_warehouse.world')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': world}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_tb3, 'launch', 'spawn_turtlebot3.launch.py')
            ),
        ),
    ])
