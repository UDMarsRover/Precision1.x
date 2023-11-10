#include <ros.h>
#include <sensor_msgs/Temperature.h>
#include <std_msgs/Header.h>

int ThermistorPin = 0;
int Vo, E;
float R1 = 10000;
float logR2, R2, T; 
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
ros::NodeHandle tempNode; 

sensor_msgs::Temperature temperature_msg;
ros::Publisher temperature_pub("temperature", &temperature_msg);

void setup() {
  tempNode.initNode();
  tempNode.advertise(temperature_pub);
 Serial.begin(9600);
}

void loop() {

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  if (T <= 0) { 
    E = 3;
  }
  if ((0 < T) && (T <= 5)) {
    E = 4; 
  } 
  if ((5 < T) && (T < 65)) {
    E = 2;
  }
  if ((65 <= T) && (T < 70)) {
    E = 1;
  }
  if( T >= 70) {
    E = 0;
  }
  
  temperature_msg.temperature = T; 
  temperature_msg.variance = E;  

  temperature_pub.publish(&temperature_msg);
  tempNode.spinOnce();
  
  delay(500);
}