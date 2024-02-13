/*
 * John Ludeke
 * 10/06/22
 * 
 * The purpose of this code is to upload temperature data
 * to the ROS to be able to be used
 */
 //Edited by Paul on 11/15 and 11/17

#include <Arduino_HTS221.h>
#define GREEN 23
#define RED 22
#define BLUE 24

//String list[] = {"FF", "FF", "FF", "FF"};

//double prevTemp = 0;
//double currTemp = 0;
float t = 0;

//String temperatureSensor();
//void startTemperatureSensor();

void setup() {
  Serial.begin(9600);
  pinMode(BLUE, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(RED, OUTPUT);

  digitalWrite(BLUE, LOW);

  while(!Serial);
  //delay(1000);

  Serial.println("Starting");
  Serial.println(startTemperatureSensor());
  //delay(2000);
}

void loop() {
  /*
  Serial.print("Temperature: ");
  String temp = temperatureSensor();
  
  Serial.println(temp);
  delay(1000);
*/
  digitalWrite(GREEN, LOW);
  digitalWrite(RED, HIGH);
  digitalWrite(BLUE, HIGH);
  //t = HTS.readTemperature();
  Serial.print("temp: ");
  Serial.println(temperatureSensor());
  digitalWrite(RED, LOW);
  digitalWrite(BLUE, HIGH);
  digitalWrite(GREEN, HIGH);
  delay(500);
}

String startTemperatureSensor() {
  // Tests if the temperature sensor is able to be initialized
  if (!HTS.begin()) {
    // Temperature sensor was unable to begin
    Serial.println("Could not initialize temperature sensor.");
    return "3B";
  }
  return "FF";
}


String temperatureSensor() {
  // Takes the temperature reading, and converts it to a 3 character string without the decimal

  if (HTS.begin()){
    float currTemp = HTS.readTemperature();
    // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
    String temp_reading = (String)(currTemp * 10);
    //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);

    // Returns the temperature
    return temp_reading.substring(0, 3);
  }
  return "3B";//could not init
}
