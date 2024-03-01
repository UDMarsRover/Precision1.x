#include <ros.h>
#include <std_msgs/Float32.h>

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
