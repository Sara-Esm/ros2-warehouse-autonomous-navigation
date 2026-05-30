#!/usr/bin/env python3

import cv2
import rclpy

from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32, Bool


class ArucoStationDetector(Node):

    def __init__(self):
        super().__init__('aruco_station_detector')

        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('debug_window', True)

        self.image_topic = self.get_parameter('image_topic').value
        self.debug_window = self.get_parameter('debug_window').value

        self.bridge = CvBridge()

        self.marker_pub = self.create_publisher(Int32, '/warehouse/marker_id', 10)
        self.detected_pub = self.create_publisher(Bool, '/warehouse/marker_detected', 10)

        self.image_sub = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10
        )

        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

        self.parameters = cv2.aruco.DetectorParameters()
        self.parameters.adaptiveThreshWinSizeMin = 3
        self.parameters.adaptiveThreshWinSizeMax = 53
        self.parameters.adaptiveThreshWinSizeStep = 10
        self.parameters.minMarkerPerimeterRate = 0.005
        self.parameters.maxMarkerPerimeterRate = 4.0
        self.parameters.polygonalApproxAccuracyRate = 0.05
        self.parameters.minCornerDistanceRate = 0.01
        self.parameters.minDistanceToBorder = 1
        self.parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters
        )

        self.get_logger().info('ArUco station detector started.')
        self.get_logger().info(f'Subscribing to image topic: {self.image_topic}')
        self.get_logger().info('Using dictionary: DICT_5X5_50')

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = self.detector.detectMarkers(gray)

        detected_msg = Bool()
        marker_msg = Int32()

        if ids is not None and len(ids) > 0:
            marker_id = int(ids[0][0])

            detected_msg.data = True
            marker_msg.data = marker_id

            self.marker_pub.publish(marker_msg)
            self.detected_pub.publish(detected_msg)

            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            self.get_logger().info(
                f'ArUco marker detected: ID={marker_id}',
                throttle_duration_sec=1.0
            )

        else:
            detected_msg.data = False
            self.detected_pub.publish(detected_msg)

            self.get_logger().info(
                f'No marker detected. Rejected candidates: {len(rejected)}',
                throttle_duration_sec=2.0
            )

        if self.debug_window:
            cv2.imshow('Warehouse ArUco Station Detector', frame)
            cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ArucoStationDetector()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
