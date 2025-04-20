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
        # self.get_logger().info(f'I heard: {msg.data}')

        # if msg.data[0] < 0 :
        #     self.ctlr.seServoKitt_servo_angle_rel(0, 15)

        #! Calibration
        # pin = 1
        # if msg.data[pin] < 0 :
        #     self.ctlr.set_servo_angle_abs(pin, 0)
        # elif msg.data[pin] > 0 :
        #     self.ctlr.set_servo_angle_abs(pin, 180)
        # else:
        #     self.ctlr.set_servo_angle_abs(pin, 90)

        step_size = 5
        
        if msg.data[0] != 0 :
            self.ctlr.set_servo_angle_rel(0, step_size*msg.data[0])
        else:
            self.ctlr.decay_to_neutral(0)

        
        if msg.data[1] != 0 :
            self.ctlr.set_servo_angle_rel(1, step_size*msg.data[1])
        else:
            self.ctlr.decay_to_neutral(1)

        # print()
        print( self.ctlr.s_angles[0:2] )
        # print( msg.data )

class pwm_controller():
    def __init__(self):
        n_servos = 16

        self.ctlr = ServoKit(channels=n_servos, address=0x41, frequency=100)

        self.set_servo_rng(0, 967, 1912)
        self.set_servo_rng(1, 1020, 1956)

        self.s_angles = n_servos * [155]

        self.set_servo_angle_abs(0, 90)
        self.set_servo_angle_abs(1, 90)
    
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
        center_angle = 110
        decay_rate = 10
        curr_angle = self.s_angles[s_idx]

        if np.abs(center_angle-curr_angle) <= 1.1*decay_rate :
            self.set_servo_angle_abs(s_idx, center_angle)
            return

        dir = 1 if self.s_angles[s_idx]<center_angle else -1

        self.set_servo_angle_rel(s_idx, dir*decay_rate)





# from adafruit_pca9685 import PCA9685
# import board

# i2c = board.I2C()

# pca = PCA9685(i2c)
# pca.frequency = 60
# pca.channels[0].duty_cycle = 0x7FFF
# pca.channels[1].duty_cycle = 0x7FFF





def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


