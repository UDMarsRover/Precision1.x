#include <ros.h>
#include <std_msgs/Float64.h>
#include <std_msgs/String.h>
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/BatteryState.h>
#include <Arduino_HTS221.h>
#include <Arduino_LSM9DS1.h>
#include <sensor_msgs/Temperature.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
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

#define DIAGNOSTIC_STATUS_LENGTH 1

ros::NodeHandle nh;

// data messages setup
std_msgs::Float64 boxTemp_data;
ros::Publisher boxTempPub("boxTemp_pub", &boxTemp_data);

sensor_msgs::Temperature batteryTemp_msg;
ros::Publisher batteryTempPub("batteryTemp_pub", &batteryTemp_msg);

sensor_msgs::Temperature voltConverterTemp_msg;
ros::Publisher voltConverterTempPub("voltConverterTemp_pub", &voltConverterTemp_msg);

geometry_msgs::Vector3 angular_velocity;
ros::Publisher imuPub("imu_pub",&angular_velocity);

//geometry_msgs::Vector3 linear_acceleration;
//ros::Publisher imuPub("imu_pub", &linear_acceleration);

sensor_msgs::BatteryState voltConverter_msg;
ros::Publisher voltConverterPub("voltConverter_pub", &voltConverter_msg);

// diagnostic messages setup
diagnostic_msgs::DiagnosticStatus dia_imu;
ros::Publisher diaImuPub("diaImu_pub", &dia_imu);

diagnostic_msgs::DiagnosticStatus dia_boxTemp;
ros::Publisher diaBoxTempPub("diaBoxTemp_pub", &dia_boxTemp);

diagnostic_msgs::DiagnosticStatus dia_voltConverterTemp;
ros::Publisher diaVoltConverterTempPub("diaVoltConverterTemp_pub",&dia_voltConverterTemp);

diagnostic_msgs::DiagnosticStatus dia_batteryTemp;
ros::Publisher diaBatteryTempPub("diaBatteryTemp_pub",&dia_batteryTemp);

diagnostic_msgs::KeyValue box_key[DIAGNOSTIC_STATUS_LENGTH];
diagnostic_msgs::KeyValue imu_key[DIAGNOSTIC_STATUS_LENGTH];


//diagnostic_msgs::KeyValue battery_key;
//ros::Publisher batteryStatusPub("batteryStatus_pub", &batteryKey);


char errorCode;

// method that updates the errorCodes array
//void updateErrorCode(std::string newError);
//change
void setup() {
  // setup
  //Serial.begin(9600);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinN, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinE, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinS, INPUT); // Sets the echoPin as an INPUT
  pinMode(echoPinW, INPUT); // Sets the echoPin as an INPUT
  pinMode(voltagePin, INPUT); 
  
  nh.initNode();
  nh.advertise(boxTempPub);
  nh.advertise(imuPub);
  nh.advertise(voltConverterPub);
  nh.advertise(voltConverterTempPub);
  nh.advertise(batteryTempPub);

  nh.advertise(diaImuPub);
  nh.advertise(diaBoxTempPub);
  nh.advertise(diaVoltConverterTempPub);
  nh.advertise(diaBatteryTempPub);

  dia_imu.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_boxTemp.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_imu.name = "Gyroscope";
  dia_boxTemp.name = "Box Temp";
  dia_voltConverterTemp.name = "Voltage Converter Temp";
  dia_batteryTemp.name = "Battery Temp";
}

void loop() {
  delay(10);

  // raw data update and publish
  boxTemp_data.data = boxTemperatureData();
  boxTempPub.publish(&boxTemp_data);  
  gyroscopeData();
  imuPub.publish(&angular_velocity);
  voltageSensorData();
  voltConverterPub.publish(&voltConverter_msg);
  voltageConverterTempData();
  voltConverterTempPub.publish(&voltConverterTemp_msg);
  batteryTempData();
  batteryTempPub.publish(&batteryTemp_msg);
  

  // diagnostic update
  dia_imu.values = imu_key;
  dia_boxTemp.values = box_key;
  
  // diagnostic publish
  diaImuPub.publish(&dia_imu);
  diaBoxTempPub.publish(&dia_boxTemp);
  diaVoltConverterTempPub.publish(&dia_voltConverterTemp);
  diaBatteryTempPub.publish(&dia_batteryTemp);

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
    dia_imu.message = "Disconnect";
    dia_imu.level = STALE;
  }
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(curAcelX, curAcelY, curAcelZ); //Provides positional information for X, Y, and Z on a scale of -1 to 1
  }
  curAcelX = expFilter(alphaGyro, acelX, curAcelX);
  curAcelY = expFilter(alphaGyro, acelY, curAcelY);
  //curAcelXmap = map(curAcelX*100, -100, 100, 0, 360) - 180;//Subtract 180 from this value to measure gyro on a scale of -180 to 180 degrees
  //curAcelYmap = map(curAcelY*100, -100, 100, 0, 360) - 180;//Subtract 180 from this value to measure gyro on a scale of -180 to 180 degrees
  
  acelX = curAcelX;
  acelY = curAcelY;
  angular_velocity.x = curAcelX;
  angular_velocity.y = curAcelY;
  //linear_acceleration.x = curAcelX;
  //linear_acceleration.y = curAcelY;
  
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
  imu_key[0].key = "";
  //imu_key[0].value = "temp";
}


float boxTemperatureData() {
  if (HTS.begin()){
    float currTemp = HTS.readTemperature();
    // std::string temp_reading = (std::to_string(tempOut * 10)).substr(0, 3);
    //String temp_reading = (String)(currTemp);
    //std::string temp_reading = (std::to_string(HTS.readTemperature() * 10)).substr(0, 3);
    // all good
    dia_boxTemp.message = "All Good";
    dia_boxTemp.level = OK;
    if (currTemp < 0) {
      //errorHexBits[3] = '2';
      // underheat emergency
      dia_boxTemp.message = "Underheat Emergency";
      dia_boxTemp.level = ERROR;

    }
    else if (currTemp < 10) {
      //errorHexBits[3] = '3';
      // underheat warning
      dia_boxTemp.message = "Underheat Warning";
      dia_boxTemp.level = WARN;
    }
    if (currTemp > 60) {
      //errorHexBits[3] = '1';
      //over heat warning
      dia_boxTemp.message = "Overheat Warning";
      dia_boxTemp.level = WARN;

    }
    else if (currTemp > 70) {
      //errorHexBits[3] = '0';
      // overheat emergency
      dia_boxTemp.message = "Overheat Emergency";
      dia_boxTemp.level = ERROR;

    }
    // Returns the temperature
    //return temp_reading.substring(0, 3);
    box_key[0].key = "box temp";
    box_key[0].value = "temp";
    return(currTemp);

  }
  //errorHexBits[3] = 'E';
  // disconnect
  dia_boxTemp.message = "Disconnect";
  dia_boxTemp.level = STALE;
}

void voltageSensorData() {
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = map(sensorValue, 0, 1023, 0, 3.3);
  float batteryVoltage = map(voltage, 0, 3.3, 0, 53);
  
  voltConverter_msg.voltage = batteryVoltage;
}

void voltageConverterTempData() {
  int ThermistorPin = 0;
  int Vo, E;
  float R1 = 10000;
  float logR2, R2, T; 
  float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  voltConverterTemp_msg.temperature = T;

  if (T <= 0) { 
    dia_voltConverterTemp.message = "Underheat Emergency"; 
    dia_voltConverterTemp.level = ERROR;
  }
  else if ((0 < T) && (T <= 5)) {
    dia_voltConverterTemp.message = "Underheat Warning"; 
    dia_voltConverterTemp.level = WARN;
  } 
  else if ((5 < T) && (T < 65)) {
    dia_voltConverterTemp.message = "OK";
    dia_voltConverterTemp.level = OK;
  }
  else if ((65 <= T) && (T < 70)) {
    dia_voltConverterTemp.message = "Overheat Warning";
    dia_voltConverterTemp.level = WARN;
  }
  else if( T >= 70) {
    dia_voltConverterTemp.message = "Overheat Emergency";
    dia_voltConverterTemp.level = ERROR;
  }
}

void batteryTempData(){
  int ThermistorPin = 0;
  int Vo, E;
  float R1 = 10000;
  float logR2, R2, T; 
  float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

  Vo = analogRead(ThermistorPin);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  batteryTemp_msg.temperature = T;

  if (T <= 30) { 
    dia_batteryTemp.message = "Underheat Emergency"; 
    dia_batteryTemp.level = ERROR;
  }
  else if ((30 < T) && (T <= 35)) {
    dia_batteryTemp.message = "Underheat Warning"; 
    dia_batteryTemp.level = WARN;
  } 
  else if ((35 < T) && (T < 60)) {
    dia_batteryTemp.message = "OK";
    dia_batteryTemp.level = OK;
  }
  else if ((60 <= T) && (T < 80)) {
    dia_batteryTemp.message = "Overheat Warning";
    dia_batteryTemp.level = WARN;
  }
  else if( T >= 80) {
    dia_batteryTemp.message = "Overheat Emergency";
    dia_batteryTemp.level = ERROR;
  }

}

// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){ 
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

