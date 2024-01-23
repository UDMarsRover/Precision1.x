#include <ros.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <diagnostic_msgs/KeyValue.h>

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;

#define DIAGNOSTIC_STATUS_LENGTH 1

ros::NodeHandle nh;

diagnostic_msgs::KeyValue key;

diagnostic_msgs::DiagnosticStatus dia_status;
ros::Publisher diaPub("dia_pub", &dia_status);

diagnostic_msgs::DiagnosticArray dia_array;
ros::Publisher arrayPub("dia_array", &dia_status);



void setup() {
  
  nh.initNode();
  nh.advertise(diaPub);
  //dia_array.status = (diagnostic_msgs::DiagnosticStatus*)malloc(DIAGNOSTIC_STATUS_LENGTH * sizeof(diagnostic_msgs::DiagnosticStatus));
  dia_status.values = (diagnostic_msgs::KeyValue*)malloc(DIAGNOSTIC_STATUS_LENGTH * sizeof(diagnostic_msgs::KeyValue));
  dia_status.values_length = DIAGNOSTIC_STATUS_LENGTH;
  //dia_array.status_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_status.name = "Diag test";
}

void loop() {
  delay(10);

  dia_status.message = "All good";
  dia_status.level = OK;

 
  key.key = "key";
  //dia_status.values = key;
  //dia_array.status[0] = dia_status;
  diaPub.publish(&dia_status);
  //arrayPub.publish(&dia_array);

  nh.spinOnce(); 
  
}










