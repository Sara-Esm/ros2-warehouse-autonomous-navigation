from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='warehouse_mission',
            executable='warehouse_mission_manager',
            output='screen'
        )

    ])
