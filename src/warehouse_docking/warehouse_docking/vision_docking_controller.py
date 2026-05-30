#!/usr/bin/env python3

import cv2
import rclpy
import numpy as np

from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image


class VisionDockingController(Node):

    def __init__(self):

        super().__init__('vision_docking_controller')

        self.bridge = CvBridge()

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_5X5_50
        )

        self.parameters = cv2.aruco.DetectorParameters()

        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters
        )

        self.target_marker_id = 0

        self.image_center_x = 320

        self.center_tolerance = 30

        self.forward_speed = 0.04
        self.rotation_speed = 0.15

        self.stop_area_threshold = 45000

        self.get_logger().info(
            'Vision Docking Controller Started'
        )

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        corners, ids, _ = self.detector.detectMarkers(frame)

        twist = Twist()

        if ids is not None:

            for i, marker_id in enumerate(ids):

                marker_id = int(marker_id[0])

                if marker_id == self.target_marker_id:

                    marker_corners = corners[i][0]

                    center_x = int(
                        np.mean(marker_corners[:, 0])
                    )

                    center_error = (
                        center_x - self.image_center_x
                    )

                    marker_area = cv2.contourArea(
                        marker_corners.astype(np.float32)
                    )

                    cv2.aruco.drawDetectedMarkers(
                        frame,
                        [marker_corners]
                    )

                    cv2.putText(
                        frame,
                        f'ID:{marker_id}',
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f'Area:{int(marker_area)}',
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    if marker_area > self.stop_area_threshold:

                        twist.linear.x = 0.0
                        twist.angular.z = 0.0

                        self.get_logger().info(
                            'Docking complete.',
                            throttle_duration_sec=2.0
                        )

                    else:

                        if abs(center_error) > self.center_tolerance:

                            twist.angular.z = (
                                -self.rotation_speed
                                if center_error > 0
                                else self.rotation_speed
                            )

                        else:

                            twist.linear.x = self.forward_speed

                    self.cmd_pub.publish(twist)

                    cv2.imshow(
                        'Vision Docking Controller',
                        frame
                    )

                    cv2.waitKey(1)

                    return

        twist.linear.x = 0.0
        twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

        cv2.imshow(
            'Vision Docking Controller',
            frame
        )

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = VisionDockingController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
