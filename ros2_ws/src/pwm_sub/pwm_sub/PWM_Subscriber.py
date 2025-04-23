import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

import numpy as np
from adafruit_servokit import ServoKit

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            # String,
            Float32MultiArray,
            'driver_commands',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning

        self.ctlr = pwm_controller()

    def listener_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        self.get_logger().info(f'I heard: {msg.data}')

        # if msg.data[0] < 0 :
        #     self.ctlr.set_servo_angle_rel(0, -15)
        # elif msg.data[0] > 0 :
        #     self.ctlr.set_servo_angle_rel(0, 15)
        
        if msg.data[0] != 0 :
            self.ctlr.set_servo_angle_rel(0, 15*msg.data[0])
        else:
            self.ctlr.decay_to_neutral(0)

        # if msg.data[1] < 0 :
        #     self.ctlr.set_servo_angle_rel(1, -15)
        # elif msg.data[1] > 0 :
        #     self.ctlr.set_servo_angle_rel(1, 15)
        
        if msg.data[1] != 0 :
            self.ctlr.set_servo_angle_rel(1, 15*msg.data[1])
        else:
            self.ctlr.decay_to_neutral(1)

class pwm_controller():
    def __init__(self):
        n_servos = 16

        self.ctlr = ServoKit(channels=n_servos, address=0x41)

        self.set_servo_rng(0, 300, 2500)
        self.set_servo_rng(1, 300, 2500)

        self.s_angles = n_servos * [90]
    
    def set_servo_rng(self, s_idx, s_min, s_max):
        self.ctlr.servo[s_idx].set_pulse_width_range(s_min, s_max)
    
    def set_servo_angle_abs(self, s_idx, s_angle):
        if s_angle < 0 :
            s_angle = 0
        elif s_angle > 180 :
            s_angle = 180
        
        self.ctlr.servo[s_idx].angle = s_angle

        self.s_angles[s_idx] = s_angle
    
    def set_servo_angle_rel(self, s_idx, s_angle):
        new_angle = s_angle + self.s_angles[s_idx]

        self.set_servo_angle_abs(s_idx, new_angle)
    
    def decay_to_neutral(self, s_idx):
        decay_rate = 5
        curr_angle = self.s_angles[s_idx]

        if np.abs(90-curr_angle) <= 1.1*decay_rate :
            return

        dir = 1 if self.s_angles[s_idx]<90 else -1

        self.set_servo_angle_rel(s_idx, dir*decay_rate)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


