
#include <vector>
#include <string>   
#include "ros/ros.h"
#include "nav_msgs/Odometry.h"
#include "location_monitor/LandmarkDistance.h"

using std::vector;
using std::string;
using location_monitor::LandmarkDistance;

class Landmark {
 public:
  Landmark(string name, double x, double y)
	 : name(name), x(x), y(y) {}
  string name;
  double x;
  double y;
  double z;
  double ax;
  double ay;
  double az;
};

class LandmarkMonitor {
  public:
    LandmarkMonitor(const ros::Publisher& landmark_pub)
      : landmarks_(), landmark_pub_(landmark_pub) {
	InitLandmarks();
    }

    void OdomCallback(const geometry_msgs::Twist::ConstPtr& msg) {
	double x = msg->linear.x;
	double y = msg->linear.y;
	double z = msg->linear.z;
	double ax = msg->angular.x;
	double ay = msg->angular.y;
	double az = msg->angular.z;
	LandmarkDistance ld = FindClosest(x,y);
	landmark_pub_.publish(ld);
	//ROS_INFO("name: %s, d: %f", ld.name.c_str(), ld.distance);
	ROS_INFO("x: %f, y: %f, z: %f, ax: %f, ay: %f, az: %f", x, y, z, ax, ay, az);
    }
    
  private:
    vector<Landmark> landmarks_;
    ros::Publisher landmark_pub_;


    LandmarkDistance FindClosest(double x, double y) {
      LandmarkDistance result;
      result.distance = -1;

      for (size_t i = 0; i < landmarks_.size(); ++i) {
	const Landmark& landmark = landmarks_[i];
	double xd = landmark.x - x;
	double yd = landmark.y - y;
	double distance = sqrt(xd*xd + yd*yd);

	if (result.distance < 0 || distance < result.distance) {
	  result.name = landmark.name;
	  result.distance = distance;
	}


      }
      return result;
    

    }

    void InitLandmarks() {
	landmarks_.push_back(Landmark("Cube", 0.31, -0.99));
	landmarks_.push_back(Landmark("Dumpster", 0.11, -2.42));
	landmarks_.push_back(Landmark("Cylinder", -1.14, -2.88));
	landmarks_.push_back(Landmark("Barrier", -2.59, -0.83));
	landmarks_.push_back(Landmark("Bookshelf", -0.09, 0.53));
    }
};



int main(int argc, char** argv) {
	ros::init(argc, argv, "location_monitor");
	ros::NodeHandle nh;
	ros::Publisher landmark_pub = nh.advertise<LandmarkDistance>("closest_landmark", 10);
	LandmarkMonitor monitor(landmark_pub);

	vector<Landmark> landmarks;
	
	// topic "odom", size of queue is 10
	ros::Subscriber sub = nh.subscribe("/vrep/cmd_vel", 10, &LandmarkMonitor::OdomCallback, &monitor);
	ros::spin();
	return 0;
}
