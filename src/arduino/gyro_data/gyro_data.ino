
#include <Arduino_LSM9DS1.h>

//The gyroscope and accelerometer methods are switched in this library for some reason. The readGyroscope() method provides speed of angle change in degrees per second and the 
//readAccelerometer() method provides positional information for X, Y, and Z on a scale of -1 to 1. Therefore, we do not need to use readGyroscope(), even though these are the values
//we are looking for.
float acelX, acelY, acelZ; 
String errorCodes;
String gyroError;
/*
This is an array of error codes. They are inserted into the array as they come in, and we will pull from the start of the array. Once we pull a value, all following values will be shifted up
so that 
*/


void setup() {
  // put your setup code here, to run once: 
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Begun");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  
  gyroscope();

}

void gyroscope() { //returns 3 hex digits
  if (IMU.gyroscopeAvailable()) {
    //IMU.readGyroscope(gyroX, gyroY, gyroZ); //Provides speed of angle change in degrees per second
    IMU.readAcceleration(acelX, acelY, acelZ); //Provides positional information for X, Y, and Z on a scale of -1 to 1
  }
  /*
  if(gyroY < minusThreshold || plusThreshold < gyroY)
  {
    gyroError = "2F";
    Serial.println(gyroError);
    delay(500);
  }
  if(gyroX < minusThreshold || plusThreshold < gyroX)
  {
    gyroError = "2F";
    Serial.println(gyroError);
    delay(500);
  }

  if(gyroY < minusThreshold*2 || plusThreshold*2 < gyroY)
  {
    gyroError = "30";
    Serial.println(gyroError);
    delay(500);
  }
  if(gyroX < minusThreshold*2 || plusThreshold*2 < gyroX)
  {
    gyroError = "30";
    Serial.println(gyroError);
    delay(500);
  }
  */
  Serial.print(acelX);
  Serial.print(",");
  Serial.println(acelY);
  String X = (String)map(acelX*100, -100, 100, 0, 360);
  String Y = (String)map(acelY*100, -100, 100, 0, 360);
  Serial.print(X);
  Serial.print(",");
  Serial.println(Y);
  /*
  String gyro_reading_X = (String)(acelX);
  String gyro_reading_Y = (String)(acelY);

  Serial.println(gyro_reading_X.substring(0,4) + "," + gyro_reading_Y.substring(0,4));
  */
  delay(500);

}