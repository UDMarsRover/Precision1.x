
#include <ros.h>
#include "C:\Users\Paul\MarsRoverWork\Precision1.x\src\arduino\voltage_sensor\BatteryState.h"

//The following include statement throughs a Checksum does not match error. This means the file imported by this line does not match with the file ros.h is looking for.
//Why? I do not know. But, if you install the BatteryState file directly, it works.

//#include <sensor_msgs/BatteryState.h>

int voltagePin = A0;
ros::NodeHandle voltage;
float sensorValue;
float prevSensorValue;
//const float Vmax = 2.2;
//const float Vmin = 1.975;
const float Vmax = 683.934; //This is real reading of voltage sensor at V = 57.500 V. Based on equation, reading would be 689.4547242 at 57.5V
const float Vmin = 630.2345; //This is real reading of voltage sensor at V = 45.505 V. Based on equation, reading would be 629.7072093 at 45.5V
//Above values were adjusted for accuracy between 45.5-50V, reading >50V results in an output about 0.5-1.0V less than actual
float diff = Vmax - Vmin;
float volt;
//ros::Publisher voltage_node("Voltage", &voltage_msg);
float alpha = 0.1;
int i = 0;
float sum;
float avg;
double alphaVoltSense = 0.1;

//At 57 volts, converter reads 2.2 V
//At 43 volts, converter reads 1.975

ros::NodeHandle voltNode;

sensor_msgs::BatteryState voltConverterMsg;
ros::Publisher voltConverterPub("voltageConverter_pub", &voltConverterMsg);

void setup() {
  voltNode.initNode();
  voltNode.advertise(voltConverterPub);
  pinMode(voltagePin, INPUT);
}

void loop() {
  delay(10);
  
  voltageSensorData();

  voltNode.spinOnce();
}

double expFilter(double alpha, double prevReading, double curReading){ 
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

void voltageSensorData() {
  sensorValue = analogRead(voltagePin);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  sensorValue = expFilter(alphaVoltSense, prevSensorValue, sensorValue);
  prevSensorValue = sensorValue;
  volt = ( sensorValue * 0.2008451735 ) - 80.97365371; //Linear regression line-of-best-fit

  float voltPercent = ( sensorValue - Vmin ) / diff;
  
  voltConverterMsg.voltage = volt;
  voltConverterMsg.percentage = voltPercent;

  voltConverterPub.publish(&voltConverterMsg);
}