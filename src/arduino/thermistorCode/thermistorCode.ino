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

sensor_msgs::Temperature batteryTemperature_msg;
sensor_msgs::Temperature voltageConverterTemperature_msg;

ros::Publisher batteryTemperature_pub("Battery Temperature", &batteryTemperature_msg);
ros::Publisher voltageConverterTemperature_pub("Voltage Converter Temperature", &voltageConverterTemperature_msg);

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;

diagnostic_msgs::DiagnosticStatus dia_temp;
diagnostic_msgs::DiagnosticArray dia_array;
diagnostic_msgs::KeyValue error;
diagnostic_msgs::KeyValue temp_key;

ros::Publisher diagnosticPub("diagnostic_pub", &dia_array);

void setup() {
  tempNode.initNode();
  tempNode.advertise(voltageConverterTemperature_pub);
  tempNode.advertise(batteryTemperature_pub);
  dia_temp.name = "Thermistor";
}

void loop() {
  delay(50);
  voltageConverterTempData();
  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  if (T <= 30) { 
    dia_temp.message = "Underheat Emergency"; 
    dia_temp.level = ERROR;
  }
  else if ((30 < T) && (T <= 35)) {
    dia_temp.message = "Underheat Warning"; 
    dia_temp.level = WARN;
  } 
  else if ((35 < T) && (T < 60)) {
    dia_temp.message = "OK";
    dia_temp.level = OK;
  }
  else if ((60 <= T) && (T < 80)) {
    dia_temp.message = "Overheat Warning";
    dia_temp.level = WARN;
  }
  else if( T >= 80) {
    dia_temp.message = "Overheat Emergency";
    dia_temp.level = ERROR;
  }

  temp_key.key = "temperature (°C)"
  temp_key.value = T.toString();

  diagnosticPub.publish(&dia_temp);

  //batteryTemperature_msg.temperature = T; 

  //batteryTemperature_pub.publish(&temperature_msg);
  //tempNode.spinOnce();
  
  delay(500);
}

void voltageConverterTempData() {

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  if (T <= 0) { 
    dia_temp.message = "Underheat Emergency"; 
    dia_temp.level = ERROR;
  }
  else if ((0 < T) && (T <= 5)) {
    dia_temp.message = "Underheat Warning"; 
    dia_temp.level = WARN;
  } 
  else if ((5 < T) && (T < 65)) {
    dia_temp.message = "OK";
    dia_temp.level = OK;
  }
  else if ((65 <= T) && (T < 70)) {
    dia_temp.message = "Overheat Warning";
    dia_temp.level = WARN;
  }
  else if( T >= 70) {
    dia_temp.message = "Overheat Emergency";
    dia_temp.level = ERROR;
  }
  
  temp_key.key = "temperature (°C)"
  temp_key.value = T.toString();

  diagnosticPub.publish(&dia_temp);

  //temperature_msg.temperature = T; 

  //temperature_pub.publish(&temperature_msg);
  //tempNode.spinOnce();
}