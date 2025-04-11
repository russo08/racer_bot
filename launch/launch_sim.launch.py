import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

 

from launch_ros.actions import Node
def generate_launch_description():

    package1_name='racer_bot'
    package2_name='teleop_twist_joy'
    # lauching rsp
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package1_name), 'launch',
                    'rsp.launch.py')]),launch_arguments={'use_sim_time': 'true'}.items()
    )
    # launching gazebo
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'),
                    'launch', 'gazebo.launch.py')])
    )
    # running gazebo spawner
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                    '-entity', 'my_bot'], output='screen')
    
    
    teleop = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package2_name), 'launch',
                    'teleop-launch.py')]), launch_arguments={'joy_config':'xbox'}.items()
    )
    # Launch all of them
    return LaunchDescription([teleop,rsp,gazebo,spawn_entity])