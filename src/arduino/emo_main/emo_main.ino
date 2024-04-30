#include <Arduino.h>
#include <ros.h>
#include <avr/dtostrf.h>
#include <std_msgs/Float32MultiArray.h> // Ultra
#include <sensor_msgs/Imu.h>
//#include "C:\Users\Paul\MarsRoverWork\Precision1.x\ros_lib\sensor_msgs\BatteryState.h"
#include <sensor_msgs/BatteryState.h> // Does not work, see voltage_sensor.ino
#include <sensor_msgs/Temperature.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <diagnostic_msgs/KeyValue.h>

#include <NewPing.h> // Ultrasonic
#include <Arduino_HTS221.h> // On-board temperature
<<<<<<< HEAD
#include "attitude.h" // IMU
#include <TinyGPSPlus.h> // GPS
#include <float.h> // GPS
#include <ros/time.h> // GPS
#include <sensor_msgs/NavSatFix.h> // GPS
#include <sensor_msgs/NavSatStatus.h> // GPS
=======
//#include <Arduino_LSM9DS1.h> // IMU
#include "attitude.h" // GPS

//GPS Include
#include <TinyGPSPlus.h>
#include <float.h>
#include <ros/time.h>
#include <sensor_msgs/NavSatFix.h>
#include <sensor_msgs/NavSatStatus.h>
>>>>>>> 1e9eebddc610a90a4152cf7b5be587e46e4a3d77

// Debug settings for serial printing.
#define DEBUG 0
#if DEBUG == 1
#define debug(x) Serial.print(x)
#define debugln(x) Serial.println(x)
#else
#define debug(x)
#define debugln(x)
#endif

//////////////////////////////////////////////////////////////////////////////////////
//Object variables for ultrasonic, IMU, thermistors, boxTemp, voltageSense, and GPS
//////////////////////////////////////////////////////////////////////////////////////

//Ultrasonic sensor variables

#define NW 0
#define TRIG1 2 // Northwest
#define ECHO1 3

#define NE 1
#define TRIG2 4 // Northeast
#define ECHO2 5

#define SW 2
#define TRIG3 6 // Southwest
#define ECHO3 7

#define SE 3
#define TRIG4 8 // Southeast
#define ECHO4 9

#define MAX_DISTANCE 100 // maximum distance for sensors in cm
#define NUM_SONAR 4 // number of ultrasonic sensors

NewPing sonar[NUM_SONAR] = { // array of ultrasonic pings
  NewPing(TRIG1, ECHO1, MAX_DISTANCE),
  NewPing(TRIG2, ECHO2, MAX_DISTANCE),
  NewPing(TRIG3, ECHO3, MAX_DISTANCE),
  NewPing(TRIG4, ECHO4, MAX_DISTANCE)
};

double curDuration[NUM_SONAR]; // array for pings in microseconds
double prevDistance[NUM_SONAR]; // arrays for pings
double curDistance[NUM_SONAR];// in cm

// arrays to store distance output as string
String curDistanceCM[NUM_SONAR];
String curDistanceOutput[NUM_SONAR];
float ultraArray[4]; // initialize array to assign to msg

//IMU variables
Attitude attitude;
float* qrt;           // [w, qx, qy, qz]         Quarternion data for w, x, y, and z
float* ypr;           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector
float* acc;           // [ax, ay, az]         Accelerometer data for x, y, and z
float* gyr;           // [gx, gy, gz]         Gyroscope data for x, y, and z
Quaternion* quat;         // [w, x, y, z]         quaternion container

// Timing variables for Loop
uint32_t LoopTimer;
int LastLoop;

//Thermistor variables
// which analog pin to connect
#define VOLTAGETHERMISTORPIN A2  
#define BATTERYTHERMISTORPIN A1      
// resistance at 25 degrees C
#define VOLTAGETHERMISTORNOMINAL 100000
#define BATTERYTHERMISTORNOMINAL 2000      
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define VOLTAGE_BCOEFFICIENT 4615
#define BATTERY_BCOEFFICIENT 3965
// the value of the 'other' resistor
#define VOLTAGESERIESRESISTOR 100100
#define BATTERYSERIESRESISTOR 2010 //1980 when mulitmeter directly on resistor, 2010 when measured relative to ground

//Box temperature variables
float currTemp;

//Voltage sensor variables
int voltagePin = A0;
float sensorValue;
float prevSensorValue;
const float Vmax = 683.934; //This is real reading of voltage sensor at V = 57.500 V. Based on equation, reading would be 689.4547242 at 57.5V
const float Vmin = 630.2345; //This is real reading of voltage sensor at V = 45.505 V. Based on equation, reading would be 629.7072093 at 45.5V
//Above values were adjusted for accuracy between 45.5-50V, reading >50V results in an output about 0.5-1.0V less than actual
float diff = Vmax - Vmin;
float volt;

//GPS variables
// IMPORTANT: This code is written specifically for a GPS unit that receives signal at a frequency of 1Hz.
// If a GPS with a higher refresh rate is used in the future, this code will need to be reworked. -Kaiden
TinyGPSPlus gps; //Boolean that keeps track of whether the previous reading was zero (prevents duplicate error messages)
bool gpsError = false;
int lastSecond = -1;

// Declare alpha for each sensor as necessary
double alphaTemp = 0.5;
double alphaUltra = 0.5;
double alphaVoltSense = 0.1;

//Counter variables
float timer;
float sensorTimer;

int queue_size;

//////////////////////////////////////////////////////////////////////////////
//Define ROS nodes, publishers, and subscribers
//////////////////////////////////////////////////////////////////////////////

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;

#define DIAGNOSTIC_STATUS_LENGTH 1

#define red 22
#define green 23
#define blue 24

/* Example for red light

  digitalWrite(red,LOW);
  digitalWrite(green,HIGH);
  digitalWrite(blue,HIGH);

*/

ros::NodeHandle nh;

// data messages setup

std_msgs::Float32MultiArray ultraMsg;
ros::Publisher ultraPub("emo/ultra", &ultraMsg);

sensor_msgs::Imu imuMsg;
ros::Publisher imuPub("emo/imu", &imuMsg);

//geometry_msgs::Vector3 angular_velocity;
//ros::Publisher imuPubGyro("emo/imu/gyro", &angular_velocity);

//geometry_msgs::Vector3 linear_acceleration;
//ros::Publisher imuPubAccel("emo/imu/accel", &linear_acceleration);

sensor_msgs::Temperature boxTemp;
ros::Publisher boxTempPub("emo/temp/box", &boxTemp);

sensor_msgs::BatteryState voltageSensorMsg;
ros::Publisher voltageSensorPub("emo/voltage", &voltageSensorMsg);

sensor_msgs::Temperature voltageConverterTempMsg;
ros::Publisher voltageConverterTempPub("emo/temp/voltage", &voltageConverterTempMsg);

sensor_msgs::Temperature batteryTempMsg;
ros::Publisher batteryTempPub("emo/temp/battery", &batteryTempMsg);

sensor_msgs::NavSatFix gpsMsg;
ros::Publisher gpsPub("emo/gps", &gpsMsg);

// diagnostic messages setup

// For the diagnostic message, 
//  level will be the priority of the error, OK, WARN, or ERROR (ERROR can be marked a critical error by the Pi and shutoff)
//  name will be the component name
//  message will be the numerical value of error if we want to report it(eg. Underheat warning), 
//  and the key:
//     key will be used to return the error code as we denote
//     value will be the meaning of that error code (eg. key = 15, value = all good)

diagnostic_msgs::DiagnosticStatus dia_ultraNW;
ros::Publisher diaUltraPubNW("emo/status/ultraNW", &dia_ultraNW);
diagnostic_msgs::DiagnosticStatus dia_ultraNE;
ros::Publisher diaUltraPubNE("emo/status/ultraNE", &dia_ultraNE);
diagnostic_msgs::DiagnosticStatus dia_ultraSW;
ros::Publisher diaUltraPubSW("emo/status/ultraSW", &dia_ultraSW);
diagnostic_msgs::DiagnosticStatus dia_ultraSE;
ros::Publisher diaUltraPubSE("emo/status/ultraSE", &dia_ultraSE);

diagnostic_msgs::DiagnosticStatus dia_imu;
ros::Publisher diaImuPub("emo/status/imu", &dia_imu);

diagnostic_msgs::DiagnosticStatus dia_boxTemp;
ros::Publisher diaBoxTempPub("emo/status/temp/box", &dia_boxTemp);

diagnostic_msgs::DiagnosticStatus dia_voltageSensor;
ros::Publisher diaVoltageSensorPub("emo/status/voltage", &dia_voltageSensor);

diagnostic_msgs::DiagnosticStatus dia_voltageConverterTemp;
ros::Publisher diaVoltageConverterTempPub("emo/status/temp/voltage",&dia_voltageConverterTemp);

diagnostic_msgs::DiagnosticStatus dia_batteryTemp;
ros::Publisher diaBatteryTempPub("emo/status/temp/battery",&dia_batteryTemp);

diagnostic_msgs::DiagnosticStatus dia_gps;
ros::Publisher diaGpsPub("emo/status/gps", &dia_gps);

diagnostic_msgs::KeyValue ultra_key;
diagnostic_msgs::KeyValue imu_key;
diagnostic_msgs::KeyValue box_key;
diagnostic_msgs::KeyValue sensor_key;
diagnostic_msgs::KeyValue converter_key;
diagnostic_msgs::KeyValue battery_key;
diagnostic_msgs::KeyValue gps_key;

//diagnostic_msgs::KeyValue battery_key;
//ros::Publisher batteryStatusPub("batteryStatus_pub", &batteryKey);

////////////////////////////////////////////////////////////////////////////////////////////
//Main setup, loop, and methods
////////////////////////////////////////////////////////////////////////////////////////////

void setup() {
  // setup
  Serial1.begin(9600);


  //Ros setup
  nh.initNode();
  nh.advertise(ultraPub); 
  //nh.advertise(imuPub);
  //nh.advertise(imuPubGyro);
  //nh.advertise(imuPubAccel);
  nh.advertise(boxTempPub);
  nh.advertise(voltageSensorPub); 
  nh.advertise(voltageConverterTempPub);
  nh.advertise(batteryTempPub);
  nh.advertise(gpsPub);
  
  nh.advertise(diaUltraPubNW);
  nh.advertise(diaUltraPubNE);
  nh.advertise(diaUltraPubSW);
  nh.advertise(diaUltraPubSE);
  nh.advertise(diaImuPub);
  nh.advertise(diaBoxTempPub);
  nh.advertise(diaVoltageSensorPub);
  nh.advertise(diaVoltageConverterTempPub);
  nh.advertise(diaBatteryTempPub);

  dia_ultraNW.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_ultraNE.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_ultraSW.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_ultraSE.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_imu.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_boxTemp.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_voltageSensor.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_voltageConverterTemp.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_batteryTemp.values_length = DIAGNOSTIC_STATUS_LENGTH;

  dia_ultraNW.name = "NW Ultrasonic";
  dia_ultraNE.name = "NE Ultrasonic";
  dia_ultraSW.name = "SW Ultrasonic";
  dia_ultraSE.name = "SE Ultrasonic";
  dia_imu.name = "Gyroscope";
  dia_boxTemp.name = "Box Temperature";
  dia_voltageSensor.name = "Voltage Sensor";
  dia_voltageConverterTemp.name = "Voltage Converter Sensor";
  dia_batteryTemp.name = "Battery Temperature Sensor";
  dia_gps.name = "GPS";

  //Method setup
  ultraMsg.data_length = 4; // initialize length of ultrasonic msg array

  LoopTimer = 0; //Going to have to find a way to integrate loop into method, not high-level loop

  attitude.initialize();

  if (!HTS.begin()) {
    dia_boxTemp.message = "Failed to intialize box temperature sensor";
    //dia_boxTemp.message = STALE;
    nh.spinOnce();

    debugln("Failed to initialize temperature sensor!");
    while (1);
  }

  pinMode(voltagePin, INPUT); // Voltage sensor setup
  //pinMode(voltageConverterTemp, INPUT); // Voltage converter temp setup
  //pinMode(batteryTemp, INPUT); // Battery temp setup
  //digitalWrite(red,LOW);
  //digitalWrite(green,HIGH);
  //digitalWrite(blue,HIGH);
}

void loop() {
  
  delay(10);
  timer = millis();

  ultrasonicData();
  imuData();
  digitalWrite(red,HIGH);
  digitalWrite(green,HIGH);
  digitalWrite(blue,LOW);
  //accelerometerData();
  //if ( (timer - sensorTimer) > 20000 ) { // If using timer, ensure no filter is being used. This will decrease resolution SIGNIFICANTLY. (20 sec/update lol)
    boxTemperatureData();
    digitalWrite(red,HIGH);
    digitalWrite(green,LOW);
    digitalWrite(blue,HIGH);
    voltageConverterTempData();
    batteryTempData();
    
   //sensorTimer = timer;
//}
  voltageSensorData();
  gpsData();

  nh.spinOnce(); 
  
  digitalWrite(red,LOW);
  digitalWrite(green,HIGH);
  digitalWrite(blue,HIGH);
}

void ultrasonicData() {
  for (int i = 0; i < NUM_SONAR; i++) {
    curDuration[i] = sonar[i].ping(); // ping distance in microseconds
    // sonar sensors return 0 if no obstacle is detected

    curDistance[i] = (curDuration[i] * 0.034) / 2; // convert microseconds to cm

    // if no object is detected, set current distance to previous 
    if (curDistance[i] == 0){
      curDistance[i] = prevDistance[i];
    }
    else{
      curDistance[i] = expFilter(alphaUltra, prevDistance[i], curDistance[i]); // filter distance values
    }

    ultraArray[i] = curDistance[i]; 
    prevDistance[i] = curDistance[i]; // set previous distance to current 
  }
  
  ultraMsg.data = ultraArray; // update msg with curent array of values
  ultraPub.publish(&ultraMsg);

  ultrasonicDiagnostic(&dia_ultraNW, &diaUltraPubNW, &ultra_key, ultraArray[NW]);
  ultrasonicDiagnostic(&dia_ultraNE, &diaUltraPubNE, &ultra_key, ultraArray[NE]);
  ultrasonicDiagnostic(&dia_ultraSW, &diaUltraPubSW, &ultra_key, ultraArray[SW]);
  ultrasonicDiagnostic(&dia_ultraSE, &diaUltraPubSE, &ultra_key, ultraArray[SE]);

}

void ultrasonicDiagnostic(diagnostic_msgs::DiagnosticStatus* sensor, ros::Publisher* publisher, diagnostic_msgs::KeyValue* key, float distance) {
  //diagnostic_msgs::KeyValue ultra_key
  char dis[10];
  dtostrf(distance, 5, 1, dis);

  if ((distance <= 50) && (distance > 30)) {
    key->key = "1";
    key->value = "Within 50 CM";
    sensor->message = dis;
    sensor->level = WARN;
    sensor->values = key;
  }
  else if ((distance <= 30) && (distance > 0)) {
    key->key = "0";
    key->value = "Within 30 CM";
    sensor->message = dis;
    sensor->level = ERROR;
    sensor->values = key;
  }
  else {
    key->key = "2";
    key->value = "OK";
    sensor->message = dis;
    sensor->level = OK;
    sensor->values = key;
  }

  publisher->publish(sensor);
}

void imuData() {

  digitalWrite(red,LOW);
  digitalWrite(green,LOW);
  digitalWrite(blue,LOW);
  delay(1000);

  quat = attitude.getQrt();
  ypr = attitude.getYpr();
  acc = attitude.getAcc();
  gyr = attitude.getGyr();

  digitalWrite(red,LOW);
  digitalWrite(green,HIGH);
  digitalWrite(blue,LOW);
  delay(1000);

  imuMsg.orientation.w = quat->w;
  imuMsg.orientation.x = quat->x;
  imuMsg.orientation.y = quat->y;
  imuMsg.orientation.z = quat->z;

  digitalWrite(red,LOW);
  digitalWrite(green,LOW);
  digitalWrite(blue,HIGH);
  delay(1000);

  imuMsg.angular_velocity.x = gyr[0];
  imuMsg.angular_velocity.y = gyr[1];
  imuMsg.angular_velocity.z = gyr[2];

  imuMsg.linear_acceleration.x = acc[0];
  imuMsg.linear_acceleration.y = acc[1];
  imuMsg.linear_acceleration.z = acc[2];

  //imuPub.publish(&imuMsg);
  gyroscopeDiagnostics(&dia_imu, &diaImuPub, &imu_key, ypr[1], ypr[2]); //ypr[1] is pitch, but we use it as roll because of the orientation of the chip (it is rotated 90 degrees), and the same is done for ypr[2]



}

void gyroscopeDiagnostics(diagnostic_msgs::DiagnosticStatus* sensor, ros::Publisher* publisher, diagnostic_msgs::KeyValue* key, float roll, float pitch) {
  char ro[10], pit[10];
  dtostrf(roll, 5, 1, ro);
  dtostrf(pitch, 5, 1, pit);
  if (abs(roll) >= 60) {
    key->key = "0";
    key->value = "Roll Emergency";
    sensor->message = ro;
    sensor->level = ERROR;
    sensor->values = key;
  }
  else if (abs(pitch) >= 60) {
    key->key = "1";
    key->value = "Pitch Emergency";
    sensor->message = pit;
    sensor->level = ERROR;
    sensor->values = key;
  }
  else if (abs(roll) >= 30) {
    key->key = "2";
    key->value = "Roll Warning";
    sensor->message = ro;
    sensor->level = WARN;
    sensor->values = key;
  }
  else if (abs(pitch) >= 30) {
    key->key = "3";
    key->value = "Pitch Warning";
    sensor->message = pit;
    sensor->level = WARN;
    sensor->values = key;
  }
  else {
    key->key = "4";
    key->value = "LEVEL";
    sensor->message = "";
    sensor->level = OK;
    sensor->values = key;
  }

  publisher->publish(sensor);
}

/*void accelerometerData() {

  acc = attitude.getAcc();
  
  linear_acceleration.x = acc[0];
  linear_acceleration.y = acc[1];
  linear_acceleration.z = acc[2];

  imuPubAccel.publish(&linear_acceleration);

}*/

float boxTemperatureData() {
    currTemp = HTS.readTemperature() - 3.0; // -3 because of constant on-board temperature increase

    delay(100);  // Only works with delay greater than or equal to 40 ms

    boxTemp.temperature = currTemp;

    boxTempPub.publish(&boxTemp);  

    temperatureDiagnostics(&dia_boxTemp, &diaBoxTempPub, &box_key, currTemp, 65, 55, 15, 5);
}

void voltageSensorData() {
  sensorValue = analogRead(voltagePin);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  sensorValue = expFilter(alphaVoltSense, prevSensorValue, sensorValue);
  prevSensorValue = sensorValue;
  volt = ( sensorValue * 0.2008451735 ) - 80.97365371; //Linear regression line-of-best-fit

  float voltPercent = ( sensorValue - Vmin ) / diff;
  
  voltageSensorMsg.voltage = volt;
  voltageSensorMsg.percentage = voltPercent;

  voltageSensorPub.publish(&voltageSensorMsg);

  voltageDiagnostics(&dia_voltageSensor, &diaVoltageSensorPub, &sensor_key, volt);
}

void voltageDiagnostics(diagnostic_msgs::DiagnosticStatus* sensor, ros::Publisher* publisher, diagnostic_msgs::KeyValue* key, float volt) {
  char v[10];
  dtostrf(volt, 5, 1, v);
  /*  CAN USE TO CONVERT STRING TO CHAR ARRAY FOR KEY
  char valWarn[20]; 
  String(degree + " Warning").toCharArray(valWarn, 20);
  char valErr[20];
  String(degree + " Emergency").toCharArray(valErr, 20); */
  
  if (volt <= 45.5) {
    key->key = "2";
    key->value = "Undervolt Emergency";
    sensor->message = v;
    sensor->level = ERROR;
    sensor->values = key;
  }
  else if (volt <= 47.5) {
    key->key = "1";
    key->value = "Undervolt Warning";
    sensor->message = v;
    sensor->level = WARN;
    sensor->values = key;
  }
  else {
    key->key = "0";
    key->value = "Voltage OK";
    sensor->message = "";
    sensor->level = OK;
    sensor->values = key;
  }

  publisher->publish(sensor);
}

void voltageConverterTempData() {
  uint8_t i;
  double average = 0;

  float samples[NUMSAMPLES];

  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(VOLTAGETHERMISTORPIN);
   average += samples[i];
  }
  
  average /= NUMSAMPLES;
  
  // convert the value to resistance
  //average = 1023 / average - 1;
  average = ((1023 * VOLTAGESERIESRESISTOR) / average) - VOLTAGESERIESRESISTOR;
  
  double steinhart;
  
  steinhart = ( 1 / ( ( ( log(average / VOLTAGETHERMISTORNOMINAL) ) / VOLTAGE_BCOEFFICIENT ) + ( 1.0 / (TEMPERATURENOMINAL + 273.15) ) ) ) - 273.15; //  1 / ( (ln(R/Ro)/B) + (1/To) ) - 273.15  

  voltageConverterTempMsg.temperature = steinhart;

  voltageConverterTempPub.publish(&voltageConverterTempMsg);

  temperatureDiagnostics(&dia_voltageConverterTemp, &diaVoltageConverterTempPub, &converter_key, steinhart, 70, 65, 5, 0);
}

void batteryTempData() {
  uint8_t i;
  double average = 0;

  float samples[NUMSAMPLES];

  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(BATTERYTHERMISTORPIN);
   average += samples[i];
  }
  
  average /= NUMSAMPLES;
  
  // convert the value to resistance
  //average = 1023 / average - 1;
  average = ((1023 * BATTERYSERIESRESISTOR) / average ) - BATTERYSERIESRESISTOR;
  
  double steinhart;
  
  steinhart = ( 1 / ( ( ( log(average / BATTERYTHERMISTORNOMINAL) ) / BATTERY_BCOEFFICIENT ) + ( 1.0 / (TEMPERATURENOMINAL + 273.15) ) ) ) - 273.15; //  1 / ( (ln(R/Ro)/B) + (1/To) ) - 273.15  

  batteryTempMsg.temperature = steinhart;

  batteryTempPub.publish(&batteryTempMsg);

  temperatureDiagnostics(&dia_batteryTemp, &diaBatteryTempPub, &battery_key, steinhart, 80, 60, 30, 0);
}

void temperatureDiagnostics(diagnostic_msgs::DiagnosticStatus* sensor, ros::Publisher* publisher, diagnostic_msgs::KeyValue* key, float temp, float upperEmer, float upperWarn, float lowEmer, float lowWarn) {
  char t[10];
  dtostrf(temp, 5, 1, t);
  
  if (temp >= upperEmer) {
    key->key = "0";
    key->value = "Overheat Emergency";
    sensor->message = t;
    sensor->level = ERROR;
    sensor->values = key;
  }
  else if ((temp < upperEmer) && (temp >= upperWarn)) {
    key->key = "1";
    key->value = "Overheat Warning";
    sensor->message = t;
    sensor->level = WARN;
    sensor->values = key;
  }
  else if ((temp < upperWarn) && (temp >= lowWarn)) {
    key->key = "2";
    key->value = "OK";
    sensor->message = t;
    sensor->level = OK;
    sensor->values = key;
  }
  else if ((temp < lowWarn) && (temp >= lowEmer)) {
    key->key = "3";
    key->value = "Underheat Warning";
    sensor->message = t;
    sensor->level = WARN;
    sensor->values = key;
  }
  else { // This is also a good indicator of connection. If device is connected, it will probably never get this cold.
    key->key = "4";
    key->value = "Underheat Emergency";
    sensor->message = t;
    sensor->level = ERROR;
    sensor->values = key;
  }

  publisher->publish(sensor);
}

void gpsData() {

  while (Serial1.available() > 0)
  {
    if (gps.encode(Serial1.read()) && gps.time.second() != lastSecond)
    {
      lastSecond = gps.time.second();
      if(gps.location.lat() == 0 && gps.location.lng() == 0)
      {
        if (!gpsError)
        {
          gpsMsg.status.status = 14;
        }
        gpsError = true;
      }
      else if (gps.location.age() > 500)
      {
        if (!gpsError)
        {
          gpsMsg.status.status = 14;
        }
        gpsError = true;
      }
      else
      {
        gpsMsg.header.stamp.sec = gps.time.second();
        gpsMsg.header.stamp.nsec = gps.time.centisecond() * 10000000;
        gpsMsg.latitude = gps.location.lat();
        gpsMsg.longitude = gps.location.lng();
        gpsMsg.altitude = gps.altitude.meters();
        gpsMsg.status.status = 15;
        gpsError = false;
      }
    }
  }

  if (millis() > 1000 && gps.charsProcessed() < 10)
  {
    
    gpsMsg.status.status = 14;
    gpsMsg.latitude = 0;
    gpsMsg.longitude = 0;
    //while(true);
  }

  gpsPub.publish(&gpsMsg);
}

double expFilter(double alpha, double prevReading, double curReading){ 
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

