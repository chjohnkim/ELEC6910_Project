#!/usr/bin/env python

import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import rospy
import math
from std_msgs.msg import Int8


###PORTRAIT 3##

#            marker.pose.position.x = 4.7317
#            marker.pose.position.y = -4.51


###PORTRAIT 4##
#      
#            marker.pose.position.x = 2.3205
#            marker.pose.position.y = -7.08034
#         
#     
###PORTRAIT 5##
#      
#            marker.pose.position.x = -0.227
#            marker.pose.position.y = -13.6657


scale = 0.5
topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, MarkerArray)

def callback(msg):
    
    markerArray = MarkerArray()

    count = 0
    MARKERS_MAX = 1
    face_detection = msg.data
##PORTRAIT ONE##
    if face_detection == 1:
        print face_detection
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = 4.739
        marker.pose.position.y = -0.15
        marker.pose.position.z = 0.3
    
            # We add the new marker to the MarkerArray, removing the oldest
            # marker from it when necessary
        if(count > MARKERS_MAX):
            markerArray.markers.pop(0)
    
        markerArray.markers.append(marker)
    
            # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1

   # Publish the MarkerArray
        publisher.publish(markerArray)
        count += 1

        rospy.sleep(0.01)
#PORTRAIT 2##
    if face_detection == 3:
        print face_detection
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = -3.156
        marker.pose.position.y = -5.9088
        marker.pose.position.z = 0.3 
# We add the new marker to the MarkerArray, removing the oldest
   # marker from it when necessary
        if(count > MARKERS_MAX):
            markerArray.markers.pop(0)
  
        markerArray.markers.append(marker)

   # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1
    
   # Publish the MarkerArray
        publisher.publish(markerArray)

        count += 1
    
        rospy.sleep(0.01)
##PORTRAIT 3##
    if face_detection == 2:
        print face_detection
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = 4.7317
        marker.pose.position.y = -4.51
        marker.pose.position.z = 0.3 
# We add the new marker to the MarkerArray, removing the oldest
   # marker from it when necessary
        if(count > MARKERS_MAX):
            markerArray.markers.pop(0)
  
        markerArray.markers.append(marker)

   # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1
    
   # Publish the MarkerArray
        publisher.publish(markerArray)

        count += 1
    
        rospy.sleep(0.01)



##PORTRAIT 4##
    if face_detection == 5:
        print face_detection
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = 2.3205
        marker.pose.position.y = -7.08034
        marker.pose.position.z = 0.3 
# We add the new marker to the MarkerArray, removing the oldest
   # marker from it when necessary
        if(count > MARKERS_MAX):
            markerArray.markers.pop(0)
  
        markerArray.markers.append(marker)

   # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1
    
   # Publish the MarkerArray
        publisher.publish(markerArray)

        count += 1
    
        rospy.sleep(0.01)

      
         
     
##PORTRAIT 5##
    if face_detection == 4:
        print face_detection
        marker = Marker()
        marker.header.frame_id = "/world"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = scale
        marker.scale.y = scale
        marker.scale.z = scale
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = -0.227
        marker.pose.position.y = -13.6657
        marker.pose.position.z = 0.3 
# We add the new marker to the MarkerArray, removing the oldest
   # marker from it when necessary
        if(count > MARKERS_MAX):
            markerArray.markers.pop(0)
  
        markerArray.markers.append(marker)

   # Renumber the marker IDs
        id = 0
        for m in markerArray.markers:
            m.id = id
            id += 1
    
   # Publish the MarkerArray
        publisher.publish(markerArray)

        count += 1
    
        rospy.sleep(0.01)
     
      
            

    print face_detection

    marker = Marker()
    marker.header.frame_id = "/world"
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.pose.orientation.w = 1.0
    marker.pose.position.x = 1000
    marker.pose.position.y = 1000
    marker.pose.position.z = 1000
    
            # We add the new marker to the MarkerArray, removing the oldest
            # marker from it when necessary
    if(count > MARKERS_MAX):
        markerArray.markers.pop(0)
    markerArray.markers.append(marker)
    
            # Renumber the marker IDs
    id = 0
    for m in markerArray.markers:
        m.id = id
        id += 1

   # Publish the MarkerArray
    publisher.publish(markerArray)
    count += 1
    rospy.sleep(0.01)


def portrait_marker():
    rospy.init_node('register')
    rospy.Subscriber('/face_detector', Int8, callback)
    rospy.spin()

if __name__ == '__main__':
    try: 
        portrait_marker()
    except rospy.ROSInterruptException: pass





