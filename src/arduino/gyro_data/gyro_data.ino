
#include <Arduino_LSM9DS1.h>

float gyroX, gyroY, gyroZ;
float curGyroX, curGyroY, curGyroZ = 0;
float curRoll, curPitch, curYaw; 
float roll, pitch, yaw;


void setup() {
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
    IMU.readGyroscope(gyroX, gyroY, gyroZ); //Provides angular velocity in degrees/sec
  }
  
  Serial.print(gyroY);
  Serial.print(", ");
  Serial.print(gyroX);
  Serial.print(", ");
  Serial.print(curGyroX);

  bool negative = gyroX < 0;
  float tan = (gyroX - curGyroX);
  float integrand = 0.001 * ( pow( (tan), 2 ) / 2 );
  if (negative) { 
    pitch = pitch - integrand;
  }
  else {
    pitch = pitch + integrand;
  }
  curGyroX = gyroX;

  Serial.print(", ");
  Serial.println(pitch);

  delay(1);

}