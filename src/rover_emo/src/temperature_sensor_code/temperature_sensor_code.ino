/*
 * John Ludeke
 * 10/06/22
 * 
 * The purpose of this code is to upload temperature data
 * to the ROS to be able to be used
 */

#include <Arduino_HTS221.h>
#define GREEN 23

//String list[] = {"FF", "FF", "FF", "FF"};

//double prevTemp = 0;
//double currTemp = 0;
float t = 0;

//String temperatureSensor();
//void startTemperatureSensor();

void setup() {
  Serial.begin(9600);
  pinMode(GREEN, OUTPUT);

  //delay(1000);

  Serial.println("Starting");
  startTemperatureSensor();
  delay(2000);
}

void loop() {
  /*
  Serial.print("Temperature: ");
  String temp = temperatureSensor();
  
  Serial.println(temp);
  delay(1000);
*/
  digitalWrite(GREEN, LOW);
  t = HTS.readTemperature();
  Serial.print("temp: ");
  Serial.println(temperatureSensor());
  digitalWrite(GREEN, HIGH);
  //delay(500);
}

bool startTemperatureSensor() {
  // Tests if the temperature sensor is able to be initialized
  if (!HTS.begin()) {
    // Temperature sensor was unable to begin
    Serial.println("Could not initialize temperature sensor.");
    return false;
    //list[0] = "3B";
  }

  return true;
}


String temperatureSensor() {
  // Takes the temperature reading, and converts it to a 3 character string without the decimal

  if (!HTS.begin()){
    float currTemp = HTS.readTemperature();
    // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
    String temp_reading = (String)(currTemp * 10);
    //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);

    // Returns the temperature
    return temp_reading;
  }
  return "3B";//could not init
}
