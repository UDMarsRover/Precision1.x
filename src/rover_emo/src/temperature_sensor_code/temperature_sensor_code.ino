/*
 * John Ludeke
 * 10/06/22
 * 
 * The purpose of this code is to upload temperature data
 * to the ROS to be able to be used
 */

#include <Arduino_HTS221.h>

String list[] = {"FF", "FF", "FF", "FF"};

double prevTemp = 0;
double currTemp = 0;

//String temperatureSensor();
//void startTemperatureSensor();

void setup() {
  Serial.begin(9600);
  
  delay(1000);

  Serial.println("Starting");
  startTemperatureSensor();
}

void loop() {

  Serial.print("Temperature: ");
  String temp = temperatureSensor();
  
  Serial.println(temp);
}

void startTemperatureSensor() {
  // Tests if the temperature sensor is able to be initialized
  if (!HTS.begin()) {
    // Temperature sensor was unable to begin
    Serial.println("Could not initialize temperature sensor.");
    list[0] = "3B";
  }

}

String temperatureSensor() {
  // Takes the temperature reading, and converts it to a 3 character string without the decimal

  currTemp = HTS.readTemperature();
   
  // double tempOut = filterFunction(alpha, currTemp, prevTemp);
  
  prevTemp = currTemp;

  // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
  String temp_reading = (String)(currTemp * 10);
  //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);

  // Returns the temperature
  return temp_reading;
}
