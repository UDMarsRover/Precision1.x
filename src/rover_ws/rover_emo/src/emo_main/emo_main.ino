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
//Ultrasonic sensor
#define trigPin 2 //attach pin D3 Arduino to pin Trig of HC-SR04
#define echoPinN 3 // attach pin D2 Arduino to pin Echo of HC-SR04_North
#define echoPinE 4 // attach pin D2 Arduino to pin Echo of HC-SR04_East
#define echoPinS 5 // attach pin D2 Arduino to pin Echo of HC-SR04_South
#define echoPinW 6 // attach pin D2 Arduino to pin Echo of HC-SR04_West
long duration; // variable for the duration of sound wave travel
long curDuration;
String distance; // variable for the distance measurement
String longD;

// Declare 
float acelX, acelY, acelZ; 
float curAcelX, curAcelY, curAcelZ;
float curAcelXmap, curAcelYmap;
float plusThreshold = 60, minusThreshold = -60;
// Declare alpha for each sensor as necessary
double alphaTemp = 0.5;
double alphaUltra = 0.7;
double alphaGyro = 0.3;
/*
int errorCode = 0xFF; //This variable will be used in every method when an error occurs. When there is an error, that error will attempt to overwrite this variable. 
//If the error passed has higher priority than the current error in this variable, it replaces it. 
//This way, this variable can be concatenated to the string at the end of the loop to return the highest priority error on every loop.
*/
char errorHexBits[] = {'F', 'F', 'F', 'F', 'F', 'F', 'F'};
//index 0 = 48V Monitor
//index 1 = Battery Temp
//index 2 = Voltage Converter Temp
//index 3 = Box Temp
//index 4 = Gyroscope
//index 5 = GPS
//index 6 = Ultrasonics
String errorString;

ros::NodeHandle nh;
std_msgs::String str_data;
ros::Publisher sensordata("sensordata", &str_data);



// method that updates the errorCodes array
//void updateErrorCode(std::string newError);



void setup() {
  // setup
  Serial.begin(9600);
  delay(10);
  digitalWrite(RED, HIGH);
  digitalWrite(BLUE, LOW);
  digitalWrite(GREEN, HIGH);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinN, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinE, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinS, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinW, INPUT); // Sets the echoPin as an INPUT
  
}

void loop() {
  for (int i = 0; i < 7; i++) {
    errorString += errorHexBits[i];
  }
  //String sensorData = gyroscopeData() + boxTemperatureData() + ultrasonicData() + busMonitorData() + batteryTempData() + voltageConverterTempData() + GPSData();
  String sensorData = errorString + ", " + gyroscopeData() + "," + boxTemperatureData() + "," + ultrasonicData();
  Serial.println(sensorData);
  for (int i = 0; i < 7; i++) {
    errorHexBits[i] = 'F';
  } //FIX THIS, THIS SUCKS
  /*
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
  */
}




String gyroscopeData() {
  if (!IMU.begin()) {
    errorHexBits[4] = 'E';
  }
  if (IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(curAcelX, curAcelY, curAcelZ); //Provides positional information for X, Y, and Z on a scale of -1 to 1
  }
  curAcelX = expFilter(alphaGyro, acelX, curAcelX);
  curAcelY = expFilter(alphaGyro, acelY, curAcelY);
  curAcelXmap = map(curAcelX*100, -100, 100, 0, 360) - 180;//Subtract 180 from this value to measure gyro on a scale of -180 to 180 degrees
  curAcelYmap = map(curAcelY*100, -100, 100, 0, 360) - 180;//Subtract 180 from this value to measure gyro on a scale of -180 to 180 degrees

  acelX = curAcelX;
  acelY = curAcelY;

  String xString = stringPadding(3, String(map(curAcelX*100, -100, 100, 0, 360)));
  String yString = stringPadding(3, String(map(curAcelY*100, -100, 100, 0, 360)));

  if(curAcelYmap < minusThreshold*2 || plusThreshold*2 < curAcelYmap || curAcelXmap < minusThreshold*2 || plusThreshold*2 < curAcelXmap)
  {
    errorHexBits[4] = '1';
  }
  else if(curAcelYmap < minusThreshold || plusThreshold < curAcelYmap || curAcelXmap < minusThreshold || plusThreshold < curAcelXmap)
  {
    errorHexBits[4] = '0';
  }
  
  delay(50);

  return xString + "," + yString;
}


String boxTemperatureData() {
  if (HTS.begin()){
    float currTemp = HTS.readTemperature();
    // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
    String temp_reading = (String)(currTemp * 10);
    //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);
    if (currTemp < 0) {
      errorHexBits[3] = '2';
    }
    else if (currTemp < 10) {
      errorHexBits[3] = '3';
    }
    if (currTemp > 60) {
      errorHexBits[3] = '1';
    }
    else if (currTemp > 70) {
      errorHexBits[3] = '0';
    }
    // Returns the temperature
    return temp_reading.substring(0, 3);
  }
  errorHexBits[3] = 'E';
}

String ultrasonicData() {
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  longD = "";

  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  curDuration = pulseIn(echoPinN, HIGH);
  curDuration = ( curDuration * 0.034 ) / 2; // Speed of sound wave divided by 2 (go and back)
  curDuration = expFilter(alphaUltra, duration, curDuration);
  
  if (curDuration < 31) {
    errorHexBits[6] = '0';
  }
  else if ((curDuration > 31) && (curDuration < 62)) {
    errorHexBits[6] = '1';
  }
  distance = (String)curDuration;
  longD += stringPadding(4, distance);
  duration = curDuration;
  
  delay(50);// everthing below does not work unless all sensors are connected
/*

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  curDuration = pulseIn(echoPinE, HIGH);
  curDuration = ( curDuration * 0.034 ) / 2; // Speed of sound wave divided by 2 (go and back)
  curDuration = expFilter(0.3, duration, curDuration);
  if (curDuration < 31) {
    errorHexBits[6] = '0';
  }
  else if ((curDuration > 31) && (curDuration < 62)) {
    errorHexBits[6] = '1';
  }
  distance = (String)curDuration;
  longD += stringPadding(4, distance);
  duration = curDuration;
  
  delay(50);


  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  curDuration = pulseIn(echoPinS, HIGH);
  curDuration = ( curDuration * 0.034 ) / 2; // Speed of sound wave divided by 2 (go and back)
  curDuration = expFilter(0.3, duration, curDuration);
  if (curDuration < 31) {
    errorHexBits[6] = '0';
  }
  else if ((curDuration > 31) && (curDuration < 62)) {
    errorHexBits[6] = '1';
  }
  distance = (String)curDuration;
  longD += stringPadding(4, distance);
  duration = curDuration;
  
  delay(50);


  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  curDuration = pulseIn(echoPinW, HIGH);
  curDuration = ( curDuration * 0.034 ) / 2; // Speed of sound wave divided by 2 (go and back)
  curDuration = expFilter(0.3, duration, curDuration);
  if (curDuration < 31) {
    errorHexBits[6] = '0';
  }
  else if ((curDuration > 31) && (curDuration < 62)) {
    errorHexBits[6] = '1';
  }
  distance = (String)curDuration;
  longD += stringPadding(4, distance);
  duration = curDuration;
  
  delay(50);
*/

  return longD; //note to self: check whether it is necessary or not to have a 50 ms delay after each of the 4 readings. Also, this will not run without all 4 sensors connected.
}
/*
String busMonitorData() {

}

String batteryTempData() {

}

String voltageConverterTempData() {

}

String GPSData() {

}

String getErrorCode() {

}
*/

String stringPadding(int requiredDigits, String value) { //Fix to move negative sign to front of value
  int diff = requiredDigits - value.length();
  while (diff > 0) {
    value = "0" + value;
    diff = diff - 1;
  }
  return value;
}

// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){
  // Serial.println(alpha);
  /*
  if (curReading < 0) {
    return -( (alpha * curReading) + ((1 - alpha) * prevReading) );
  }
  */
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}
