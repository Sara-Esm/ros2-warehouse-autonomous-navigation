from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    nav2_pkg = get_package_share_directory('turtlebot3_navigation2')

    map_file = os.path.join(
        os.path.expanduser('~'),
        'projects',
        'warehouse_ws',
        'src',
        'aws-robomaker-small-warehouse-world',
        'maps',
        '002',
        'map.yaml'
    )

    nav2_launch = os.path.join(
        nav2_pkg,
        'launch',
        'navigation2.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true'
            }.items()
        )
    ])
