from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    warehouse_gazebo_pkg = get_package_share_directory('warehouse_gazebo')
    turtlebot3_description_pkg = get_package_share_directory('turtlebot3_description')

    world_file = os.path.join(
        warehouse_gazebo_pkg,
        'worlds',
        'small_warehouse.world'
    )

    robot_sdf = '/opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf'

    robot_urdf = os.path.join(
        turtlebot3_description_pkg,
        'urdf',
        'turtlebot3_burger.urdf'
    )

    gazebo_models = (
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

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command([
                'xacro ',
                robot_urdf,
                ' namespace:=""'
            ]),
            'use_sim_time': True
        }],
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
                    '-file', robot_sdf,
                    '-x', '0',
                    '-y', '0',
                    '-z', '0.05'
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', gazebo_models),

        gazebo,
        robot_state_publisher,
        spawn_robot
    ])
