#include <Arduino.h>
//ROS data-type libraries
#include <ros.h>
//#include <std_msgs/Float64.h>
//#include <std_msgs/String.h>
//#include <std_msgs/Float32MultiArray.h> // Ultra
//#include <sensor_msgs/Imu.h>
//#include "C:\Users\Paul\MarsRoverWork\Precision1.x\ros_lib\sensor_msgs\BatteryState.h"
//#include <sensor_msgs/BatteryState.h> // Does not work, see voltage_sensor.ino
#include <sensor_msgs/Temperature.h>
//#include <diagnostic_msgs/DiagnosticStatus.h>
//#include <diagnostic_msgs/KeyValue.h>

//#include <NewPing.h> // Ultrasonic
#include <Arduino_HTS221.h> // On-board temperature
//#include <Arduino_LSM9DS1.h> // IMU

//GPS Include
//#include <TinyGPSPlus.h>
//#include <float.h>
//#include <ros/time.h>
//#include <sensor_msgs/NavSatFix.h>
//#include <sensor_msgs/NavSatStatus.h>



/*
#include <Arduino.h>
#include <ros.h>
#include <sensor_msgs/Temperature.h>
#include <Arduino_HTS221.h>
*/
float currTemp;

ros::NodeHandle nh;

sensor_msgs::Temperature boxTemp;
ros::Publisher boxTempPub("boxTemp_Pub", &boxTemp);


void setup() {
  nh.initNode();
  nh.advertise(boxTempPub);


  if (!HTS.begin()) {
    //Serial.println("Failed to initialize humidity temperature sensor!");
    while (1);
  }
}

void loop() {
  //delay(20);
  
  //if (HTS.begin()) {
    currTemp = HTS.readTemperature();
 // }
  //t_v = 5;
  delay(40);

  boxTemp.temperature = currTemp;

  //delay(20);

  boxTempPub.publish(&boxTemp);

  //delay(10);

  nh.spinOnce();

}