#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node

from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import PoseWithCovarianceStamped


class AutoInitialPose(Node):

    def __init__(self):
        super().__init__('auto_initial_pose_from_gazebo')

        self.pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        self.sub = self.create_subscription(
            ModelStates,
            '/gazebo/model_states',
            self.model_states_callback,
            10
        )

        self.sent = False

        self.get_logger().info(
            'Waiting for Gazebo robot pose...'
        )

    def model_states_callback(self, msg):

        if self.sent:
            return

        robot_index = None

        for i, name in enumerate(msg.name):
            if (
                'turtlebot3' in name.lower()
                or 'burger' in name.lower()
                or 'waffle' in name.lower()
            ):
                robot_index = i
                break

        if robot_index is None:
            self.get_logger().warn(
                f'Robot model not found. Available models: {msg.name}'
            )
            return

        robot_pose = msg.pose[robot_index]

        initial_pose = PoseWithCovarianceStamped()

        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.get_clock().now().to_msg()

        initial_pose.pose.pose.position.x = robot_pose.position.x
        initial_pose.pose.pose.position.y = robot_pose.position.y
        initial_pose.pose.pose.position.z = 0.0

        initial_pose.pose.pose.orientation = robot_pose.orientation

        initial_pose.pose.covariance[0] = 0.05
        initial_pose.pose.covariance[7] = 0.05
        initial_pose.pose.covariance[35] = 0.05

        time.sleep(1.0)

        for _ in range(5):
            self.pose_pub.publish(initial_pose)
            time.sleep(0.3)

        self.get_logger().info(
            f'Initial pose published from Gazebo: '
            f'x={robot_pose.position.x:.3f}, '
            f'y={robot_pose.position.y:.3f}'
        )

        self.sent = True


def main(args=None):
    rclpy.init(args=args)

    node = AutoInitialPose()

    try:
        while rclpy.ok() and not node.sent:
            rclpy.spin_once(node, timeout_sec=0.2)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
