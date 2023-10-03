/*
 * John Ludeke
 * rosserial publisher for sensor data
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino_HTS221.h>
#include <Arduino_LSM9DS1.h>

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
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinN, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinE, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinS, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinW, INPUT); // Sets the echoPin as an INPUT
  
}

void loop() {
  String sensorData = gyroscopeData() + "," + boxTemperatureData();

}


float thermistorData(int pin){
  int ThermistorPin = 0;
  int Vo;
  float R1 = 10000;
  float logR2, R2, T;
  float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;
  Vo = analogRead(pin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;
  T = (T * 9.0)/ 5.0 + 32.0; 

  //Serial.print("Temperature: "); 
  //Serial.print(T);
  //Serial.println(" C");
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
    errorHexBits[4] = '0';
  }
  else if(curAcelYmap < minusThreshold || plusThreshold < curAcelYmap || curAcelXmap < minusThreshold || plusThreshold < curAcelXmap)
  {
    errorHexBits[4] = '1';
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


// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}
