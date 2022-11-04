/*
 * John Ludeke
 * rosserial publisher for sensor data
 */

#include <ros.h>
#include <std_msgs/String.h>

// Declare 

// Declare alpha for each sensor as necessary
double alphaTemp = 0.5;

std::string errorCodes[] = {"FF", "FF", "FF", "FF", "FF", "FF", "FF"};
int errorCodesLength = 0;

ros::NodeHandle nh;
std_msgs::String str_data;
ros::Publisher sensordata("sensordata", &str_data);

// method that updates the errorCodes array
void updateErrorCode(std::string newError);



void setup() {
  // setup

}

void loop() {
  std::string sensorData = gyroscopeData() + boxTemperatureData() + ultrasonicData() + busMonitorData() + batteryTempData() + voltageConverterTempData() + GPSData();
  
}




std::string gyroscopeData() {

}

std::string boxTemperatureData() {

}

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
}

// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

