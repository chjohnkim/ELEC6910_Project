/* Author: Yetao,Lyu */
#include <iostream>
#include <vector>
#include <string>

// include OpenCV header file
#include <opencv2/opencv.hpp>
#include "opencv2/objdetect.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

// include Eigen header file
#include <Eigen/Dense>
#include <Eigen/Geometry>

// ROS image handling
#include <ros/ros.h>
#include <ros/console.h>
#include <std_msgs/Int8.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <cv_bridge/cv_bridge.h>

using namespace std;
using namespace cv;
using namespace Eigen;

#define  PI 3.1415926
#define  color_width 512
#define  color_height 512
#define  angle 0.785398
#define  faceSize 128
#define  TRAINNO 5
#define  deleteEigenNo 0
#define  coefNo 4 //TRAINNO - 1 - deleteEigenNo
#define  deleteEigenOrder true

//Global variables
String face_cascade_name = "/home/john/catkin_ws/src/face_detector/data/haarcascade_face.xml";
String eyes_cascade_name = "/home/john/catkin_ws/src/face_detector/data/haarcascade_eye.xml";
CascadeClassifier face_cascade;
CascadeClassifier eyes_cascade;
String window_name = "Capture - Face detection";
MatrixXf eigenValue(TRAINNO - 1, 1);
MatrixXf eigenVector(faceSize*faceSize, TRAINNO - 1);
MatrixXf trainingset(faceSize*faceSize, TRAINNO);
MatrixXf testingset(faceSize*faceSize, 1);
MatrixXf trainCoef = MatrixXf(coefNo, TRAINNO);
MatrixXf testCoef = MatrixXf(coefNo, 1);
float meanFace[faceSize*faceSize];
ros::Publisher recognize_pub;

bool detectAndDisplay(Mat frame, Mat & faceROI){
    bool detect = false;
    resize(frame, frame, Size(512, 512));
    std::vector<Rect> faces;
    Mat frame_gray;
    cvtColor( frame, frame_gray, COLOR_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );
    //-- Detect faces
    //cout << "Start detecting faces!" << endl;
    imwrite("testing.jpg", frame_gray);
    face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|CASCADE_SCALE_IMAGE, Size(10, 10), Size(500, 500) );
    //cout << faces.size() << " faces are detected" << endl;

    if(faces.size() > 0){
      detect = true;
      //only show the first detected face
      Point center( faces[0].x + faces[0].width/2, faces[0].y + faces[0].height/2 );
      //ellipse( frame, center, Size( faces[0].width/2, faces[0].height/2 ), 0, 0, 360, Scalar( 255, 0, 255 ), 4, 8, 0 );
      rectangle(frame, faces[0], CV_RGB(255, 255, 0), 2, CV_AA);
      faceROI = frame_gray( faces[0] );

      // //-- In each face, detect eyes
      // std::vector<Rect> eyes;
      // eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |CASCADE_SCALE_IMAGE, Size(30, 30) );
      // for ( size_t j = 0; j < eyes.size(); j++ )
      // {
      //     Point eye_center( faces[0].x + eyes[j].x + eyes[j].width/2, faces[0].y + eyes[j].y + eyes[j].height/2 );
      //     int radius = cvRound( (eyes[j].width + eyes[j].height)*0.25 );
      //     circle( frame, eye_center, radius, Scalar( 255, 0, 0 ), 4, 8, 0 );
      // }
    }

    //-- Show what you got
    if(detect){
      //imshow( window_name, frame );
      resize(faceROI, faceROI, Size(faceSize, faceSize));
      imshow( window_name, faceROI );
      waitKey(50) ;
    }
    return detect;
}

VectorXf normalizeFace(Mat testFace){
  VectorXf face(faceSize * faceSize);
  for (int j = 0; j < faceSize * faceSize; j++){
    face(j) = (float)testFace.data[j];
  }
  float sum = 0;
	float mean;
	float variance = 0;
	for (int i = 0; i < faceSize*faceSize; i++){
		sum += face(i);
	}
	mean = sum / faceSize*faceSize;
	for (int i = 0; i < faceSize*faceSize; i++){
		face(i) -= mean;
		variance += face(i) * face(i);
	}
	variance /= faceSize*faceSize;
	for (int i = 0; i < faceSize*faceSize; i++){
		face(i) /= sqrt(variance);
	}
  return face;
}

int recognize(Mat frame){
  //Apply the face detector to the frame
  int matchedFace = 0;
  Mat testFace;
  bool detect = detectAndDisplay(frame, testFace);
  if(detect){
      //cout << "Faces is detected!" << endl;
      imwrite("detected_face.jpg", testFace);
      //VectorXf normalizedTestFace = normalizeFace(testFace);
      for (int j = 0; j < faceSize * faceSize; j++){
        testingset(j) = (testFace.data[j] - meanFace[j]);
      }

      if (deleteEigenOrder){		//if delete several eigenvectors of large eigenvalue
        testCoef = (eigenVector.transpose() * testingset).block(0, 0, TRAINNO - 1 - deleteEigenNo, 1);
      }
      else{						//if delete the first several eigenvectors of small eigenvalue
        testCoef = (eigenVector.transpose() * testingset).block(deleteEigenNo, 0, TRAINNO - 1 - deleteEigenNo, 1);
      }
     // cout << "trainCoef: " << endl << trainCoef << endl;
     // cout << "testCoef: " << endl << testCoef << endl;
      float euclideanDistance_min = 1000000000;
      for (int j = 0; j < TRAINNO; j++){
        VectorXf distance(coefNo);
        distance = testCoef.col(0) - trainCoef.col(j);
        //cout << "train No. " << j << "\tdistance: " << distance << endl;
        float euclideanDistance = 0;
        for (int k = 0; k < coefNo; k++){
          euclideanDistance += (distance(k) * distance(k));
        }
        euclideanDistance = sqrt(euclideanDistance);
        if (euclideanDistance < euclideanDistance_min){
          matchedFace = j+1;
          euclideanDistance_min = euclideanDistance;
        }
      }
     // cout << "min distance: " << euclideanDistance_min << endl;
     // cout << "matched face: " << matchedFace << endl;
  }
  return matchedFace;
}

void img_callback(const sensor_msgs::ImageConstPtr &img_msg){
  Mat frame;
  try
  {
    cv_bridge::CvImagePtr bridge_ptr = cv_bridge::toCvCopy(img_msg, sensor_msgs::image_encodings::BGR8);
    frame = bridge_ptr->image;
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to '8UC3'.", img_msg->encoding.c_str());
  }
  imwrite("frame.jpg", frame);
  flip(frame,frame,1);
  std_msgs::Int8 msg;
  msg.data = recognize(frame);
  recognize_pub.publish(msg);
}

int main(int argc, char **argv){
  ros::init(argc, argv, "face_detector");
  ros::NodeHandle n;

  //get the Eigenfaces for classification
  std::vector<Mat> trainFace;
  std::vector<VectorXf> normalizedTrainFace;

  for(int i=0; i<TRAINNO; i++){
    stringstream filename;
  	filename << "/home/john/catkin_ws/src/face_detector/training/" << i+1 << ".jpg";
    Mat face;
    try {   // Surround the OpenCV call by a try/catch block so we can give a useful error message!
      face = imread(filename.str(), CV_LOAD_IMAGE_GRAYSCALE);   // Read the file
    }
    catch (cv::Exception &e) {}
    if (!face.data){                              // Check for invalid input
      cout << "Could not open or find the image" << endl;
      exit(1);
    }
    trainFace.push_back(face);
    //normalizedTrainFace.push_back(normalizeFace(face));
  }
  for (int i = 0; i < faceSize*faceSize; i++){
    meanFace[i] = 0;
  }
  for (int i = 0; i < TRAINNO; i++){
    for (int j = 0; j < faceSize*faceSize; j++){
      meanFace[j] += trainFace[i].data[j];
    }
  }
  for (int i = 0; i < faceSize*faceSize; i++){
    meanFace[i] /= TRAINNO;
  }

  //Save the training face matrix into the format used in Eigen library
	for (int i = 0; i < TRAINNO; i++){
		for (int j = 0; j < faceSize * faceSize; j++){
			trainingset(j, i) = (trainFace[i].data[j] - meanFace[j]);
		}
	}
  MatrixXf covFace(TRAINNO, TRAINNO);
	covFace = trainingset.transpose()*trainingset;
	//cout << "Here is the matrix m:\n" << covFace << std::endl;
	//cout << "The matrix m is of size " << covFace.rows() << "x" << covFace.cols() << std::endl;
	//Get the eigen value and eigen vector of the covFace
	SelfAdjointEigenSolver<MatrixXf> eigensolver(covFace);
	if (eigensolver.info() != Success) abort();
	//cout << "The eigenvalues of covFace are:\n" << eigensolver.eigenvalues() << endl;
  for (int i = 0; i < TRAINNO - 1; i++){
    eigenValue(i) = eigensolver.eigenvalues()(i + 1);
  }

  for (int i = 0; i < TRAINNO - 1; i++){
    eigenVector.col(i) = trainingset * eigensolver.eigenvectors().col(i + 1);
    eigenVector.col(i) /= sqrt(eigenValue(i));
  }

  // Get the low-dimensional coefficients of train faces

  if (deleteEigenOrder){		//if delete several eigenvectors of large eigenvalue
		trainCoef = (eigenVector.transpose() * trainingset).block(0, 0, TRAINNO - 1 - deleteEigenNo, TRAINNO);
	}
	else{						//if delete the first several eigenvectors of small eigenvalue
		trainCoef = (eigenVector.transpose() * trainingset).block(deleteEigenNo, 0, TRAINNO - 1 - deleteEigenNo, TRAINNO);
	}

  //Load the cascades
  if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading face cascade\n"); return -1; };
  if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading eyes cascade\n"); return -1; };


// //For testing face recognition
//   //Open an image and load it to the Mat inputFace
//   Mat frame;
//   string filename = "/home/john/catkin_ws/src/face_detector/picture/pic001.jpg";
//   //string filename = "/home/john/catkin_ws/src/frame.jpg";
// 	try {   // Surround the OpenCV call by a try/catch block so we can give a useful error message!
// 		frame = imread(filename, CV_LOAD_IMAGE_COLOR);   // Read the file
// 	}
// 	catch (cv::Exception &e) {}
// 	if (!frame.data){                              // Check for invalid input
// 		cout << "Could not open or find the image" << endl;
// 		exit(1);
// 	}
//   int result = recognize(frame);

  ros::Subscriber sub_img = n.subscribe("/vrep/image", 100, img_callback);
  recognize_pub = n.advertise<std_msgs::Int8>("face_detector", 1);
  //ROS_INFO("Start detecting faces...");

  ros::spin();
}
