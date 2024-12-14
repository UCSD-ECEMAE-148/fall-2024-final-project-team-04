import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from roboflowoak import RoboflowOak
import cv2
import json


# Nodes in this program
NODE_NAME = 'cane_detection_node'
CENTROID_TOPIC_NAME = '/centroid'

class CanDetection(Node):
    def __init__(self):
        super().__init__(NODE_NAME)
        self.centroid_error_publisher = self.create_publisher(Float32, CENTROID_TOPIC_NAME, 10)

        self.get_logger().info("Centroid Publisher Node Trying to Initialize with RoboflowOak ...")
        # Initialize RoboflowOak with required parameters
        self.rf = RoboflowOak(model="latinhas", confidence=0.6, overlap=0.5,
        version="1", api_key="api_key", rgb=True,
        depth=True, device=None, blocking=True)

        self.get_logger().info("Centroid Publisher Node Initialized with RoboflowOak")

    def calculate_x_centroids(self, predictions):
        """Calculate x centroids from predictions."""
        return [item.x + item.width / 2 for item in predictions]
    
    def process_and_publish(self):
        """Run detection, calculate x centroids, and publish."""
        try:
            # Run inference
            result, frame, _, _ = self.rf.detect()
            predictions = result["predictions"]

            # Calculate x centroids
            x_centroids = self.calculate_x_centroids(predictions)

            self.get_logger().info(f"Get x centroid: {json.dumps(x_centroids, indent=2)}")

            # Publish the x centroid of the first detected object, if any
            if x_centroids:
                msg = Float32()
                msg.data = float(x_centroids[0])  # Only publish the first x centroid
                self.centroid_error_publisher.publish(msg)
                self.get_logger().info(f"Published x centroid: {x_centroids[0]}")

            # Display frame with predictions
            # cv2.imshow("Roboflow Output", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) == ord('q'):
                raise KeyboardInterrupt

        except Exception as e:
            self.get_logger().error(f"Error in process_and_publish: {e}")


def main(args=None):
    rclpy.init(args=args)
    centroid_publisher = CanDetection()
    try:
        while rclpy.ok():
            centroid_publisher.process_and_publish()
    except KeyboardInterrupt:
        centroid_publisher.get_logger().info("Shutting down Centroid Publisher Node...")
    finally:
        centroid_publisher.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
