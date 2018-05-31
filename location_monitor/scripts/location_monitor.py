#!/usr/bin/env python
import math
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

pub = rospy.Publisher('location_monitor', String, queue_size=10)
A = "Robot is in Room A!"
B = "Robot is in Room B!"
C = "Robot is in Room C!"
D = "Robot is in Room D!"
##Global Variables
x = 0;
y = 0;

## Publish user input from teleop_keyboard to vrep robot ##
def callback(msg):
    global x
    global y
    x = msg.pose.position.x
    y = msg.pose.position.y    
    ##rospy.loginfo('x: {}, y: {}'.format(x, y))
    if x > 5.0214:
    	pub.publish(D)
    elif y < -6.649:
	pub.publish(C)
    elif y < -3.587:
   	pub.publish(B)
    else:
   	pub.publish(A)

    

    
## Subscribe to /slam_out_pose and do callback##
def location_monitor():
    rospy.init_node('location_monitor', anonymous=True)
    rospy.Subscriber('/slam_out_pose', PoseStamped, callback)
    rate = rospy.Rate(10)
    rate.sleep()
    rospy.spin()

## MAIN ##
if __name__ == '__main__':
    try:
        location_monitor()
    except rospy.ROSInterruptException: pass
