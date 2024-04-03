// SPDX-FileCopyrightText: 2011 Limor Fried/ladyada for Adafruit Industries
//
// SPDX-License-Identifier: MIT

// Thermistor Example #3 from the Adafruit Learning System guide on Thermistors 
// https://learn.adafruit.com/thermistor/overview by Limor Fried, Adafruit Industries
// MIT License - please keep attribution and consider buying parts from Adafruit

// which analog pin to connect
#define THERMISTORPIN A1         
// resistance at 25 degrees C
#define THERMISTORNOMINAL 100000      
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 4615
// the value of the 'other' resistor
#define SERIESRESISTOR 100100    

int samples[NUMSAMPLES];

void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  uint8_t i;
  double average = 0;

  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   average += samples[i];
   delay(10);
  }
  
  average /= NUMSAMPLES;

  Serial.print("Average analog reading "); 
  Serial.println(average);
  
  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
  Serial.print("Thermistor resistance "); 
  Serial.println(average);
  
  double steinhart;
  /*
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert absolute temp to C
  */
  steinhart = ( 1 / ( ( ( log(average / THERMISTORNOMINAL) ) / BCOEFFICIENT ) + ( 1.0 / (TEMPERATURENOMINAL + 273.15) ) ) ) - 273.15; //  1 / ( (ln(R/Ro)/B) + (1/To) ) - 273.15  
  
  Serial.print("Temperature "); 
  Serial.print(steinhart);
  Serial.println(" *C");
  
  delay(1000);
}

/*
#include <ros.h>
#include <sensor_msgs/Temperature.h>
#include <std_msgs/Header.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>

int ThermistorPin = 0;
int Vo, E;
float R1 = 100000;
float logR2, R2, T; 
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
char Ts[20];
ros::NodeHandle tempNode; 

sensor_msgs::Temperature batteryTemperature_msg;
sensor_msgs::Temperature voltageConverterTemperature_msg;

ros::Publisher batteryTemperature_pub("Bat_temp", &batteryTemperature_msg);
ros::Publisher voltConverterT_pub("VC_temp", &voltageConverterTemperature_msg);

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
  tempNode.advertise(voltConverterT_pub);
  tempNode.advertise(batteryTemperature_pub);
  tempNode.advertise(diagnosticPub);
  dia_temp.name = "Thermistor";
}

void loop() {
  delay(50);
  //voltageConverterTempData();
  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  voltageConverterTemperature_msg.temperature = T;

  voltConverterT_pub.publish(&voltageConverterTemperature_msg);

  tempNode.spinOnce();
}
/*
void loop() {
  delay(50);
  //voltageConverterTempData();
  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;
  sprintf(Ts, "%f", T);

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

  temp_key.key = "temperature (°C)";
  temp_key.value = Ts;

  diagnosticPub.publish(&dia_temp);

  //batteryTemperature_msg.temperature = T; 

  //batteryTemperature_pub.publish(&temperature_msg);
  //tempNode.spinOnce();
  
}
/*
void voltageConverterTempData() {

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;
  sprintf(Ts, "%f", T);

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
  
  temp_key.key = "temperature (°C)";
  temp_key.value = Ts;

  diagnosticPub.publish(&dia_temp);

  //temperature_msg.temperature = T; 

  //temperature_pub.publish(&temperature_msg);
  //tempNode.spinOnce();
}
*/