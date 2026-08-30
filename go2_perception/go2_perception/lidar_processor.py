import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2


class LidarProcessor(Node):

    def __init__(self):
        super().__init__('lidar_processor')

        self.declare_parameter('input_topic', '/unitree_lidar/points')
        self.declare_parameter('output_topic', '/unitree_lidar/scan')

        self.declare_parameter('angle_min', -math.pi)
        self.declare_parameter('angle_max', math.pi)
        self.declare_parameter('angle_increment', math.radians(1.0))

        self.declare_parameter('range_min', 0.1)
        self.declare_parameter('range_max', 30.0)

        self.declare_parameter('z_min', -0.5)
        self.declare_parameter('z_max', 1.0)

        input_topic = self.get_parameter(
            'input_topic'
        ).get_parameter_value().string_value

        output_topic = self.get_parameter(
            'output_topic'
        ).get_parameter_value().string_value

        self.angle_min = self.get_parameter(
            'angle_min'
        ).get_parameter_value().double_value

        self.angle_max = self.get_parameter(
            'angle_max'
        ).get_parameter_value().double_value

        self.angle_increment = self.get_parameter(
            'angle_increment'
        ).get_parameter_value().double_value

        self.range_min = self.get_parameter(
            'range_min'
        ).get_parameter_value().double_value

        self.range_max = self.get_parameter(
            'range_max'
        ).get_parameter_value().double_value

        self.z_min = self.get_parameter(
            'z_min'
        ).get_parameter_value().double_value

        self.z_max = self.get_parameter(
            'z_max'
        ).get_parameter_value().double_value

        self.num_bins = int(
            math.ceil(
                (self.angle_max - self.angle_min)
                / self.angle_increment
            )
        )

        self.subscription = self.create_subscription(
            PointCloud2,
            input_topic,
            self.pointcloud_callback,
            10
        )

        self.publisher = self.create_publisher(
            LaserScan,
            output_topic,
            10
        )

        self.get_logger().info(
            'LiDAR processor started.'
        )

        self.get_logger().info(
            f'Subscribing: {input_topic}'
        )

        self.get_logger().info(
            f'Publishing: {output_topic}'
        )

    def pointcloud_callback(self, msg):

        ranges = [float('inf')] * self.num_bins

        total_points = 0
        valid_points = 0
        rejected_z = 0
        rejected_range = 0
        rejected_angle = 0

        for point in point_cloud2.read_points(
            msg,
            field_names=['x', 'y', 'z'],
            skip_nans=False
        ):

            total_points += 1

            x = float(point[0])
            y = float(point[1])
            z = float(point[2])

            # Reject NaN / Inf.
            if not (
                math.isfinite(x)
                and math.isfinite(y)
                and math.isfinite(z)
            ):
                continue

            # Vertical filtering.
            if not (self.z_min <= z <= self.z_max):
                rejected_z += 1
                continue

            # Horizontal range.
            distance = math.hypot(x, y)

            if not (
                self.range_min
                <= distance
                <= self.range_max
            ):
                rejected_range += 1
                continue

            # Horizontal angle.
            angle = math.atan2(y, x)

            if not (
                self.angle_min
                <= angle
                < self.angle_max
            ):
                rejected_angle += 1
                continue

            index = int(
                (angle - self.angle_min)
                / self.angle_increment
            )

            if 0 <= index < self.num_bins:

                if distance < ranges[index]:
                    ranges[index] = distance

                valid_points += 1

        scan = LaserScan()

        scan.header = msg.header

        scan.angle_min = self.angle_min
        scan.angle_max = self.angle_max
        scan.angle_increment = self.angle_increment

        scan.time_increment = 0.0
        scan.scan_time = 0.0

        scan.range_min = self.range_min
        scan.range_max = self.range_max

        scan.ranges = ranges

        self.publisher.publish(scan)

        self.get_logger().debug(
            f'Total={total_points}, '
            f'valid={valid_points}, '
            f'z_rejected={rejected_z}, '
            f'range_rejected={rejected_range}, '
            f'angle_rejected={rejected_angle}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = LidarProcessor()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()