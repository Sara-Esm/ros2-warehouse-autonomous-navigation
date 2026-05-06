from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get TurtleBot3 model from environment variable or default to 'burger'
    turtlebot3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')

    # Path to warehouse_gazebo package
    warehouse_pkg = get_package_share_directory('warehouse_gazebo')
    world_file = os.path.join(warehouse_pkg, 'worlds', 'small_warehouse.world')

    # Set Gazebo model path
    gazebo_models_path = os.path.join(warehouse_pkg, 'models')
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=gazebo_models_path
    )

    # Gazebo launch (server + client)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'world': world_file}.items()
    )

    # Robot state publisher (reads URDF)
    turtlebot3_urdf_file = os.path.join(
        get_package_share_directory('turtlebot3_description'),
        'urdf',
        f'turtlebot3_{turtlebot3_model}.urdf'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': open(turtlebot3_urdf_file).read()}]
    )

    # Spawn TurtleBot3 into Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'turtlebot3', '-topic', 'robot_description'],
        output='screen'
    )

    return LaunchDescription([
        set_gazebo_model_path,
        gazebo_launch,
        robot_state_publisher,
        spawn_robot
    ])
