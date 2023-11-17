#include <ros.h>
#include <std_msgs/Float64.h>
#include <std_msgs/String.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/BatteryState.h>
#include <Arduino_HTS221.h>
#include <Arduino_LSM9DS1.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <diagnostic_msgs/KeyValue.h>

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
float plusThreshold = 30, minusThreshold = -30;
int voltagePin = A0;
int sensorValue;
// Declare alpha for each sensor as necessary
double alphaTemp = 0.5;
double alphaUltra = 0.7;
double alphaGyro = 0.3;

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;


ros::NodeHandle nh;

std_msgs::Float64 boxTemp_data;
ros::Publisher boxTempPub("boxTemp_pub", &boxTemp_data);

geometry_msgs::Vector3 angular_velocity;
ros::Publisher imuPub("imu_pub",&angular_velocity);

sensor_msgs::BatteryState voltage_msg;
ros::Publisher voltagePub("voltage_pub", &voltage_msg);

diagnostic_msgs::DiagnosticStatus dia_imu;
ros::Publisher diaImuPub("diaImu_pub", &dia_imu);

//diagnostic_msgs::DiagnosticArray dia_array;
//ros::Publisher diagnosticPub("diagnostic_pub", &dia_array);

diagnostic_msgs::KeyValue box_key;
diagnostic_msgs::KeyValue imu_key;


//diagnostic_msgs::KeyValue battery_key;
//ros::Publisher batteryStatusPub("batteryStatus_pub", &batteryKey);


char errorCode;

// method that updates the errorCodes array
//void updateErrorCode(std::string newError);



void setup() {
  // setup
  //Serial.begin(9600);
  delay(10);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinN, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinE, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinS, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinW, INPUT); // Sets the echoPin as an INPUT
  pinMode(voltagePin, INPUT); 
  
  nh.initNode();
  nh.advertise(boxTempPub);
  nh.advertise(imuPub);
  nh.advertise(voltagePub);

  nh.advertise(diaImuPub);

  dia_imu.name = "Gyroscope";
  dia_imu.values_length = 2;
 // dia_array.status_length = 10;

}

void loop() {
  delay(50);
  boxTemp_data.data = boxTemperatureData();
  boxTempPub.publish(&boxTemp_data);  
  gyroscopeData();
  imuPub.publish(&angular_velocity);
  voltageSensorData();
  voltagePub.publish(&voltage_msg);

  // diagnostic update
  dia_imu.values[0] = imu_key;
  //dia_array.st_status = dia_imu;
  
  // diagnostic publish
  diaImuPub.publish(&dia_imu);
  diagnosticPub.publish(&dia_array);


  /*
  dia_array.status[0] = diagnostic_msg;
  diagnostic_msg.level = WARN;
  dia_array[1].st_status = diagnostic_msg;
  diagnosticPub.publish(&dia_array);
  */
  nh.spinOnce(); 
  
  //Serial.println(sensorData);
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


void gyroscopeData() {
  
  if (!IMU.begin()) {
    //errorCode = 'E';
    imu_key.key = "Disconnect";
    imu_key.value = "E";
    dia_imu.level = STALE;
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
  angular_velocity.x = curAcelXmap;
  angular_velocity.y = curAcelYmap;
  
  if(curAcelYmap < minusThreshold*2 || plusThreshold*2 < curAcelYmap || curAcelXmap < minusThreshold*2 || plusThreshold*2 < curAcelXmap)
  {
    //error = '0';
    dia_imu.message = "Roll over emergency";
    dia_imu.level = ERROR;
    //roll over emergency
    
  }
  else if(curAcelYmap < minusThreshold || plusThreshold < curAcelYmap || curAcelXmap < minusThreshold || plusThreshold < curAcelXmap)
  {
    //error = '1';
    dia_imu.message = "Roll over warning";
    dia_imu.level = WARN;
    //roll over warning
  }
  else{
    dia_imu.message = "All Good";
    dia_imu.level = OK;
    //All good
  }
  imu_key.key = ("angular velocity x: ");
  imu_key.value = "temp";
  delay(50);
}


float boxTemperatureData() {
  if (HTS.begin()){
    float currTemp = HTS.readTemperature();
    // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
    //String temp_reading = (String)(currTemp);
    //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);
    box_key.key = "All Good";
    box_key.value = "F";
    if (currTemp < 0) {
      //errorHexBits[3] = '2';
      box_key.key = "Underheat emergency";
      box_key.value = "2";
    }
    else if (currTemp < 10) {
      //errorHexBits[3] = '3';
      box_key.key = "Underheat warning";
      box_key.key = "3";
    }
    if (currTemp > 60) {
      //errorHexBits[3] = '1';
      box_key.key = "Overheat warning";
      box_key.value = "1";
    }
    else if (currTemp > 70) {
      //errorHexBits[3] = '0';
      box_key.key = "Overheat emergency";
      box_key.value = "0";
    }
    // Returns the temperature
    //return temp_reading.substring(0, 3);
    return(currTemp);

  }
  //errorHexBits[3] = 'E';
  box_key.key = "Disconnect";
  box_key.value = "E";

  
}


void voltageSensorData() {
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = map(sensorValue, 0, 1023, 0, 3.3);
  float batteryVoltage = map(voltage, 0, 3.3, 0, 53);
  
  voltage_msg.voltage = batteryVoltage;

}


// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){ 
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

