#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

# import roslib
# roslib.load_manifest('my_package')

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String, Bool, Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

pub1 = rospy.Publisher('/vrep/laser_switch', Bool, queue_size = 10)
#Global Variables
x_d = 255
radius_d = 180
K_p_x = 0.02
K_p_radius = 0.02
global room


def callback1(data):
    global room
    room = data.data

class image_converter:


    def __init__(self):
        self.image_pub = rospy.Publisher('image_topic_2', Image, queue_size=1)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('vrep/image', Image, self.callback)

    def callback(self, data):
        global room
        try:
            raw_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError, e:
            pass #print e
    # Flip image to correct orientation 
        corrected_image = raw_image.copy()
        corrected_image = cv2.flip(corrected_image, 1)
        #cv2.imshow('Corrected', corrected_image)

    #set boundaries for color detection    
        boundaries = [([0, 150, 150], [70, 255, 255])]
        for (lower, upper) in boundaries:  # Loop over the boundaries

    # create NumPy arrays from the boundaries

            lower = np.array(lower, dtype='uint8')
            upper = np.array(upper, dtype='uint8')

    # find the colors within the specified boundaries and apply the mask

            mask = cv2.inRange(corrected_image, lower, upper)
            output = cv2.bitwise_and(corrected_image, corrected_image, mask=mask)
            
            #find countours in the mask and initialize the current (x,y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            #global room
            rospy.Subscriber('/location_monitor', String, callback1)
        
            #print room
            #only proceed if at least one contour was found
            if  room == "Robot is in Room D!" and len(cnts) > 0: #
                
                pub = rospy.Publisher('/vrep/cmd_vel', Twist, queue_size = 10) 
                bool_msg = 0
                pub1.publish(bool_msg)
                #find the largest contour in the mask, then use it to compute the minimum enclosing circule and centroid
                c = max(cnts, key=cv2.contourArea)
                ((x,y,), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if M["m00"] == 0:
                    M["m00"] = 0.0001
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #print M #debug
                #only proceed if the radius meets a minimum size
                if radius > 10:
                    #draw circle and centroid on the frame, then update the list of tracked points 
                    cv2.circle(corrected_image, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(corrected_image, center, 5, (0, 0, 255), -1)
                    
                    #Implement Control to follow yellow ball
                    ang_err = x_d - x
                    cmd_vel_ang = K_p_x * ang_err
                    distance_err = radius_d - radius
                    cmd_vel_lin = K_p_radius * distance_err
                    if cmd_vel_ang > 1.5:
                        cmd_vel_ang = 1.5
                    if cmd_vel_lin > 2:
                        cmd_vel_lin = 2
                    #rospy.loginfo('x: {}, y: {}, radius: {}, cmd_vel_ang: {}, cmd_vel_lin: {}'.format(x, y, radius, cmd_vel_ang, cmd_vel_lin))

                    vel_msg = Twist()
                    vel_msg.linear.x = cmd_vel_lin
                    vel_msg.angular.z = cmd_vel_ang 
                    pub.publish(vel_msg)                   
            else: 
                bool_msg = 1 
                pub1.publish(bool_msg)


            cv2.imshow('Image', np.hstack([corrected_image, output]))
             



        cv2.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(raw_image,
                                   'bgr8'))
        except CvBridgeError, e:
            pass #print e


def main(args):
    
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass #print 'Shutting down'
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)

			
