#!/usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/vrep/cmd_vel', Twist, queue_size=10)

##Global Variables
x_linear = 0;
y_linear = 0;
z_linear = 0;
x_angular = 0;
y_angular = 0;
z_angular = 0;

## Publish user input from teleop_keyboard to vrep robot ##
def callback(msg):
    global x_linear
    global y_linear
    global z_linear
    global x_angular
    global y_angular
    global z_angular
    x_linear = msg.linear.x
#    y_linear = msg.linear.y
#    z_linear = msg.linear.z
#    x_angular = msg.angular.x
#    y_angular = msg.angular.y
    z_angular = msg.angular.z
    rospy.loginfo('x: {}, y: {}, z: {}, ax: {}, ay: {}, az: {}'.format(x_linear, y_linear, z_linear,  x_angular, y_angular, z_angular))

    vel_msg = Twist()
    
    #Retrieve values from keyboard input
    vel_msg.linear.x = x_linear
    vel_msg.angular.z = z_angular
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    
    pub.publish(vel_msg)
    
## Subscribe to teleop_keyboard to retrieve user input ##
def keyboard_control():
    rospy.init_node('keyboard_control', anonymous=True)
    rospy.Subscriber('/cmd_vel', Twist, callback)
    rospy.spin()

## MAIN ##
if __name__ == '__main__':
    try:
        keyboard_control()
    except rospy.ROSInterruptException: pass
