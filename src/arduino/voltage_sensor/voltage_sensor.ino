#include <ros.h>
#include <std_msgs/Float32.h>

int voltagePin = A0;
ros::NodeHandle voltage;
float sensorValue;
float prevSensorValue;
//const float Vmax = 2.2;
//const float Vmin = 1.975;
const float Vmax = 683.934; //V = 57.500 V
// Based on equation, reading would be 685.401 at 57.5V
const float Vmin = 630.2345; //V = 45.505 V
// Based on equation, reading would be 632.027 at 45.5V
//This means the voltage is not correctly calculated at ends -> voltage will be overestimated on high end, and underestimated on low end (sensor reads voltage of 45.4 V at input of 631.55)
float diff = Vmax - Vmin;
float volt;
std_msgs::Float32 voltage_msg;
//ros::Publisher voltage_node("Voltage", &voltage_msg);
float alpha = 0.1;
int i = 0;
float sum;
float avg;

//At 57 volts, converter reads 2.2 V
//At 43 volts, converter reads 1.975

void setup() {
  //volt.initNode();
  //volt.advertise(voltage_node);
  pinMode(voltagePin, INPUT);
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(voltagePin);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  sensorValue = expFilter(alpha, prevSensorValue, sensorValue);
  prevSensorValue = sensorValue;
  Serial.print(sensorValue);
  volt = ( sensorValue * 0.2008451735 ) - 80.97365371; //Linear regression line-of-best-fit

  float voltPercent = ( sensorValue - Vmin ) / diff;
  Serial.print(", ");
  Serial.print(volt, 8);
  Serial.print(", ");
  Serial.println(voltPercent, 8);
  delay(50);

  i += 1;
  sum += volt;
  if (i > 200) {
    avg = sum / i;
    i = 0;
    sum = 0;
    Serial.println(avg,10);
  }
  //voltage_msg.data = batteryVoltage;
  //voltage_node.publish(&voltage_msg);
  //volt.spinOnce();
}

double expFilter(double alpha, double prevReading, double curReading){ 
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

