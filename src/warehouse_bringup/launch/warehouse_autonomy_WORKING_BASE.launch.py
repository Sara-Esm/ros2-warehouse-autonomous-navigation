from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    warehouse_gazebo_pkg = get_package_share_directory('warehouse_gazebo')

    world_file = os.path.join(
        warehouse_gazebo_pkg,
        'worlds',
        'small_warehouse.world'
    )

    if not os.path.exists(world_file):
        raise FileNotFoundError(f"World file not found: {world_file}")

    gazebo_model_path = (
        '/usr/share/gazebo-11/models:'
        + os.path.expanduser('~/projects/warehouse_ws/src/warehouse_gazebo/models:')
        + '/opt/ros/humble/share/turtlebot3_gazebo/models'
    )

    gazebo = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            world_file,
            '-s', 'libgazebo_ros_factory.so'
        ],
        output='screen'
    )

    spawn_robot = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=[
                    '-entity', 'turtlebot3',
                    '-file', '/opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf',
                    '-x', '0',
                    '-y', '0',
                    '-z', '0.05'
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_model_path),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),

        gazebo,
        spawn_robot
    ])