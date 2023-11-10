#include <ros.h>
#include <sensor_msgs/Temperature.h>
#include <std_msgs/Header.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>

int ThermistorPin = 0;
int Vo, E;
float R1 = 10000;
float logR2, R2, T; 
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
ros::NodeHandle tempNode; 

sensor_msgs::Temperature temperature_msg;
ros::Publisher temperature_pub("temperature", &temperature_msg);

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;

diagnostic_msgs::DiagnosticStatus diagnostic_msg;
diagnostic_msgs::DiagnosticArray dia_array;
ros::Publisher diagnosticPub("diagnostic_pub", &dia_array);

void setup() {
  tempNode.initNode();
  tempNode.advertise(temperature_pub);
 dia_array status_length = 4;
}

void loop() {

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  if (T <= 30) { 
    E = 3;
  }
  if ((30 < T) && (T <= 35)) {
    E = 4; 
  } 
  if ((35 < T) && (T < 60)) {
    E = 2;
  }
  if ((60 <= T) && (T < 80)) {
    E = 1;
  }
  if( T >= 80) {
    E = 0;
  }
  
  diagnostic_msg.level = OK;
  dia_array.status[0] = diagnostic_msg
  diagnosticPub.publish(&dia_array);

  temperature_msg.temperature = T; 
  //temperature_msg.variance = E;  

  temperature_pub.publish(&temperature_msg);
  tempNode.spinOnce();
  
  delay(500);
}