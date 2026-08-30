#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2


class LidarProcessor(Node):

    def __init__(self):
        super().__init__('lidar_processor')

        self.subscription = self.create_subscription(
            PointCloud2,
            '/unitree_lidar/points',
            self.pointcloud_callback,
            10
        )

        self.get_logger().info(
            'LiDAR processor started. Waiting for PointCloud2...'
        )

    def pointcloud_callback(self, msg):

        self.get_logger().info(
            f'Received PointCloud2 | '
            f'frame={msg.header.frame_id} | '
            f'width={msg.width} | '
            f'height={msg.height}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = LidarProcessor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()