import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class GPSPublisherNode(Node):
    """ROS2 Node to publish GPS location."""

    def __init__(self):
        super().__init__('gps_publisher_node')
        self.publisher = self.create_publisher(NavSatFix, '/gps/location', 10)
        self.timer = self.create_timer(1.0, self.publish_gps_location)  # Publish every second
        self.get_logger().info("GPS Publisher Node Initialized.")

    def publish_gps_location(self):
        """Publish a dummy GPS location."""
        msg = NavSatFix()
        msg.latitude = 37.7749  # Example latitude (San Francisco)
        msg.longitude = -122.4194  # Example longitude (San Francisco)
        msg.altitude = 30.0  # Example altitude in meters
        msg.position_covariance = [0.0] * 9  # Placeholder covariance matrix
        msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN
        msg.status.status = NavSatFix.STATUS_FIX  # Assume a valid GPS fix
        msg.status.service = NavSatFix.SERVICE_GPS

        self.publisher.publish(msg)
        self.get_logger().info(f"Published GPS Location: lat={msg.latitude}, lon={msg.longitude}, alt={msg.altitude}")

def main(args=None):
    rclpy.init(args=args)
    node = GPSPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down GPS Publisher Node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
