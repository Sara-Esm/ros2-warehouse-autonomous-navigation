#!/usr/bin/env python3

import math
import time
import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus


def yaw_to_quaternion(yaw_deg):
    yaw_rad = math.radians(yaw_deg)
    qz = math.sin(yaw_rad / 2.0)
    qw = math.cos(yaw_rad / 2.0)
    return qz, qw


class WarehouseAutonomy(Node):

    def __init__(self):
        super().__init__('warehouse_autonomy')

        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.waypoints = [
            {
                'name': 'Charging Station',
                'x': -7.131,
                'y': -6.491,
                'yaw': 9.481,
            },
            {
                'name': 'Loading Zone',
                'x': 9.785,
                'y': -2.849,
                'yaw': 0.493,
            },
            {
                'name': 'Shelf A Inspection',
                'x': 0.493,
                'y': -0.944,
                'yaw': -67.400,
            },
            {
                'name': 'Shelf B Inspection',
                'x': 2.997,
                'y': -6.240,
                'yaw': -11.774,
            },
            {
                'name': 'Central Warehouse Aisle',
                'x': 2.359,
                'y': -2.495,
                'yaw': 10.807,
            },
            {
                'name': 'Return to Charging Station',
                'x': -7.131,
                'y': -6.491,
                'yaw': 9.481,
            },
        ]

        self.current_waypoint = 0

        self.get_logger().info('Warehouse autonomy node started.')
        self.get_logger().info('Waiting for Nav2 action server...')

        self.client.wait_for_server()

        self.get_logger().info('Nav2 is ready. Starting mission in 3 seconds...')
        time.sleep(3)

        self.send_next_goal()

    def send_next_goal(self):

        if self.current_waypoint >= len(self.waypoints):
            self.get_logger().info('MISSION COMPLETE: Robot finished all warehouse destinations.')
            return

        waypoint = self.waypoints[self.current_waypoint]

        name = waypoint['name']
        x = waypoint['x']
        y = waypoint['y']
        yaw = waypoint['yaw']

        qz, qw = yaw_to_quaternion(yaw)

        goal_msg = NavigateToPose.Goal()
        pose = PoseStamped()

        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0

        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw

        goal_msg.pose = pose

        self.get_logger().info(
            f'Sending robot to {name} '
            f'({self.current_waypoint + 1}/{len(self.waypoints)}): '
            f'x={x}, y={y}, yaw={yaw} deg'
        )

        future = self.client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by Nav2.')
            self.current_waypoint += 1
            time.sleep(2)
            self.send_next_goal()
            return

        self.get_logger().info('Goal accepted by Nav2.')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):

        result = future.result()
        status = result.status

        waypoint = self.waypoints[self.current_waypoint]
        name = waypoint['name']

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'ARRIVED: {name}')
        else:
            self.get_logger().error(f'FAILED: {name}, status={status}')

        self.current_waypoint += 1
        time.sleep(2)
        self.send_next_goal()


def main(args=None):
    rclpy.init(args=args)
    node = WarehouseAutonomy()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()