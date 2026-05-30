#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class WarehouseMissionManager(Node):

    def __init__(self):
        super().__init__('warehouse_mission_manager')

        self.navigator = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.waypoints = [
            {
                "name": "PICKUP_ZONE",
                "x": 0.5,
                "y": 0.0
            },
            {
                "name": "STORAGE_ZONE",
                "x": 1.5,
                "y": 0.5
            },
            {
                "name": "SHIPPING_ZONE",
                "x": 0.0,
                "y": 1.5
            },
            {
                "name": "HOME",
                "x": 0.0,
                "y": 0.0
            }
        ]

        self.current_waypoint = 0

        self.get_logger().info('Warehouse Mission Manager Started')

        self.navigator.wait_for_server()

        self.send_goal()

    def send_goal(self):

        if self.current_waypoint >= len(self.waypoints):
            self.get_logger().info('Mission completed!')
            return

        wp = self.waypoints[self.current_waypoint]

        goal_msg = NavigateToPose.Goal()

        pose = PoseStamped()

        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = wp["x"]
        pose.pose.position.y = wp["y"]

        pose.pose.orientation.w = 1.0

        goal_msg.pose = pose

        self.get_logger().info(
            f'Navigating to {wp["name"]}'
        )

        send_goal_future = self.navigator.send_goal_async(goal_msg)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected!')
            return

        self.get_logger().info('Goal accepted')

        result_future = goal_handle.get_result_async()

        result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):

        wp = self.waypoints[self.current_waypoint]

        self.get_logger().info(
            f'Arrived at {wp["name"]}'
        )

        self.get_logger().info(
            'Simulating warehouse task...'
        )

        time.sleep(5)

        self.current_waypoint += 1

        self.send_goal()


def main(args=None):

    rclpy.init(args=args)

    node = WarehouseMissionManager()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
