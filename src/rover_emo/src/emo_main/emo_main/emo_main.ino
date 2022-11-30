/*
 * John Ludeke
 * rosserial publisher for sensor data
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino_HTS221.h>
#include <Arduino_LSM9DS1.h>
#define GREEN 23
#define RED 22
#define BLUE 24

// Declare 
float acelX, acelY, acelZ; 
// Declare alpha for each sensor as necessary
double alphaTemp = 0.5;


std::string errorCodes[] = {"FF", "FF", "FF", "FF", "FF", "FF", "FF"};
int errorCodesLength = 0;

ros::NodeHandle nh;
std_msgs::String str_data;
ros::Publisher sensordata("sensordata", &str_data);
String err = "FF";


// method that updates the errorCodes array
//void updateErrorCode(std::string newError);



void setup() {
  // setup
  digitalWrite(RED, HIGH);
  digitalWrite(BLUE, LOW);
  digitalWrite(GREEN, HIGH);
  
}

void loop() {
  //std::string sensorData = gyroscopeData() + boxTemperatureData() + ultrasonicData() + busMonitorData() + batteryTempData() + voltageConverterTempData() + GPSData();
  String temp = boxTemperatureData();
   if (temp != "3B") {
    digitalWrite(RED, HIGH);
    digitalWrite(BLUE, HIGH);
    digitalWrite(GREEN, LOW);
  }
  else {
    digitalWrite(RED, LOW);
    digitalWrite(BLUE, HIGH);
    digitalWrite(GREEN, HIGH);
  }
  
}




String gyroscopeData() {
  if (!IMU.begin()) {
    return "2C";//Could not initialize
  }
  if (IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(acelX, acelY, acelZ); //Provides positional information for X, Y, and Z on a scale of -1 to 1
  }
  String acelXmap = (String)map(acelX*100, -100, 100, 0, 360);
  String acelYmap = (String)map(acelY*100, -100, 100, 0, 360);
  return acelXmap + "," + acelYmap;
}


String boxTemperatureData() {
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

String startTemperatureSensor() {
  // Tests if the temperature sensor is able to be initialized
  if (!HTS.begin()) {
    // Temperature sensor was unable to begin
    return "3B";
  }
  return "FF";
}
/*
std::string ultrasonicData() {

}

std::string busMonitorData() {

}

std::string batteryTempData() {

}

std::string voltageConverterTempData() {

}

std::string GPSData() {

}

std::string getErrorCode() {

}
*/

void updateErrorCode(std::string newError) {
  // This makes sure the errorCodesLength never exceeds 8 before the for loop
  if (errorCodesLength = 8) {
    errorCodesLength--;
  }

  // Moves the existing errors to the right in the errorCodes array and removes the last error code
  for (int i = errorCodesLength - 1; i > 0; --i) {
    errorCodes[i] = errorCodes[i - 1];
  }

  // sets the first error in the errorCodes array as the new error
  errorCodes[0] = newError;
}


// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

