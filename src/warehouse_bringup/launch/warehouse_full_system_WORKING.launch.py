from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bringup_pkg = get_package_share_directory('warehouse_bringup')

    gazebo_tb3_launch = os.path.join(
        bringup_pkg,
        'launch',
        'warehouse_autonomy_WORKING_GAZEBO_TB3.launch.py'
    )

    nav2_launch = os.path.join(
        bringup_pkg,
        'launch',
        'warehouse_nav2_WORKING_NAV2.launch.py'
    )

    gazebo_and_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_tb3_launch)
    )

    nav2_delayed = TimerAction(
        period=12.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(nav2_launch)
            )
        ]
    )

    return LaunchDescription([
        gazebo_and_robot,
        nav2_delayed
    ])
