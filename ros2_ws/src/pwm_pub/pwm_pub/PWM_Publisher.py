#! /usr/bin/env python3

import numpy as np

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

class PWM_Publisher(Node):
    def __init__(self):
        super().__init__("PWM_Publisher")

        # self.action = np.array([0.0, 0.0])
        self.action = [0.0, 0.0]

        self.publisher_ = self.create_publisher(Float32MultiArray, 'driver_commands', 1,)

        self.get_logger().info("PWM_Publisher running")

        update_interval = 1./25
        self.create_timer(update_interval, self.timer_callback)

        with open('output.txt', 'w') as f :
            f.write( "" )

    def timer_callback(self):
        msg = Float32MultiArray()
        msg.data = self.action
        self.publisher_.publish(msg)

    def publish_action(self):
        msg = Float32MultiArray()
        msg.data = self.action
        self.publisher_.publish(msg)

        self.get_logger().info( f"msg = {msg.data}" )




def main(args=None):
    rclpy.init(args=args)

    node = PWM_Publisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
    main()

