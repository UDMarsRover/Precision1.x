//ROS data-type libraries
#include <ros.h>
//#include <std_msgs/Float64.h>
//#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h> // Ultra
#include <sensor_msgs/Imu.h>
#include <sensor_msgs/BatteryState.h>
#include <sensor_msgs/Temperature.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <diagnostic_msgs/KeyValue.h>

#include <NewPing.h> // Ultrasonic
#include <Arduino_HTS221.h> // On-board temperature
#include <Arduino_LSM9DS1.h> // IMU

//GPS Include
//#include <Arduino.h> //Causes errors, "__FlashStringHelper already declared"
#include <TinyGPSPlus.h>
//#include <SoftwareSerial.h>    ASK KAIDEN
#include <float.h>
#include <ros/time.h>
#include <sensor_msgs/NavSatFix.h>
#include <sensor_msgs/NavSatStatus.h>

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

#define TRIG1 2
#define ECHO1 3

#define TRIG2 4
#define ECHO2 5

#define TRIG3 6
#define ECHO3 7

#define TRIG4 8
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
float RateRoll, RatePitch, RateYaw = 1; //If set to null, divide by zero in first iteration -> NaN output
float RateCalibrationRoll, RateCalibrationPitch, RateCalibrationYaw;
int RateCalibrationNumber;
float AccX, AccY, AccZ = 1; //If set to null, divide by zero in first iteration -> NaN output
float AccX_offset, Accy_offset, AccZ_offset;
float AngleRoll, AnglePitch;
uint32_t last_power_down;
float KalmanAngleRoll = 0, KalmanUncertaintyAngleRoll = 2 * 2;
float KalmanAnglePitch = 0, KalmanUncertaintyAnglePitch = 2 * 2;
float Kalman1DOutput[] = { 0, 0 };
// Timing variables for Loop
uint32_t LoopTimer;
int LastLoop;

//Thermistor variables
int voltageConverterTemp = A1;
int batteryTemp = A2;
int Vo_v, Vo_b;
float R1_v, R1_b = 10000;
float logR2_v, R2_v, T_v, logR2_b, R2_b, T_b; 
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

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
double alphaUltra = 0.1;
double alphaGyro = 0.3;
double alphaVoltSense = 0.1;

//////////////////////////////////////////////////////////////////////////////
//Define ROS nodes, publishers, and subscribers
//////////////////////////////////////////////////////////////////////////////

#define OK diagnostic_msgs::DiagnosticStatus::OK;
#define WARN diagnostic_msgs::DiagnosticStatus::WARN;
#define ERROR diagnostic_msgs::DiagnosticStatus::ERROR;
#define STALE diagnostic_msgs::DiagnosticStatus::STALE;

#define DIAGNOSTIC_STATUS_LENGTH 1

ros::NodeHandle nh;

// data messages setup

std_msgs::Float32MultiArray ultraMsg;
ros::Publisher ultraPub("ultrasonic_pub", &ultraMsg);

//sensor_msgs::Imu imuMsg;
geometry_msgs::Vector3 angular_velocity;
ros::Publisher imuPub("imu_pub",&angular_velocity);

sensor_msgs::Temperature boxTemp_data;
ros::Publisher boxTempPub("boxTemp_pub", &boxTemp_data);

sensor_msgs::BatteryState voltConverterMsg;
ros::Publisher voltConverterPub("voltageConverter_pub", &voltConverterMsg);

sensor_msgs::Temperature voltConverterTemp_msg;
ros::Publisher voltConverterTempPub("voltConverterTemp_pub", &voltConverterTemp_msg);

sensor_msgs::Temperature batteryTemp_msg;
ros::Publisher batteryTempPub("batteryTemp_pub", &batteryTemp_msg);

sensor_msgs::NavSatFix gpsMsg;
ros::Publisher gpsPub("GPS", &gpsMsg);

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

////////////////////////////////////////////////////////////////////////////////////////////
//Main setup, loop, and methods
////////////////////////////////////////////////////////////////////////////////////////////

void setup() {
  // setup
  //Serial.begin(9600);

  //Ros setup
  nh.initNode();
  //nh.advertise(ultraPub);
  //nh.advertise(imuPub);
  //nh.advertise(boxTempPub);
  //nh.advertise(voltConverterPub);
  nh.advertise(voltConverterTempPub);
  nh.advertise(batteryTempPub);
  //nh.advertise(gpsPub);
  
  //nh.advertise(diaImuPub);
  //nh.advertise(diaBoxTempPub);
  //nh.advertise(diaVoltConverterTempPub);
  //nh.advertise(diaBatteryTempPub);

  dia_imu.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_boxTemp.values_length = DIAGNOSTIC_STATUS_LENGTH;
  dia_imu.name = "Gyroscope";
  dia_boxTemp.name = "Box Temp";
  dia_voltConverterTemp.name = "Voltage Converter Temp";
  dia_batteryTemp.name = "Battery Temp";

  //Method setup
  ultraMsg.data_length = 4; // initialize length of ultrasonic msg array

  LoopTimer = 0; //Going to have to find a way to integrate loop into method, not high-level loop
  if (!IMU.begin()) {
    debugln("Failed to initialize IMU!");
    while (1);
  }

  pinMode(voltagePin, INPUT); // Voltage sensor setup
  pinMode(voltageConverterTemp, INPUT); // Voltage converter temp setup
  pinMode(batteryTemp, INPUT); // Battery temp setup

}

void loop() {
  
  delay(10);

  //ultrasonicData();
  //gyroscopeData();
  //boxTemperatureData();
  //voltageSensorData();
  voltageConverterTempData();
  batteryTempData();
  //gps();

  /*
  // diagnostic update
  dia_imu.values = imu_key;
  dia_boxTemp.values = box_key;
  
  
  // diagnostic publish
  diaImuPub.publish(&dia_imu);
  diaBoxTempPub.publish(&dia_boxTemp);
  diaVoltConverterTempPub.publish(&dia_voltConverterTemp);
  diaBatteryTempPub.publish(&dia_batteryTemp);
  */

  nh.spinOnce(); 
}

void ultrasonicData() {
  for (int i = 0; i < NUM_SONAR; i++) {
    curDuration[i] = sonar[i].ping(); // ping distance in microseconds
    // sonar sensors return 0 if no obstacle is detected

    curDistance[i] = (curDuration[i] * 0.034) / 2; // convert microseconds to cm

    // if no object is detected set current distance to previous 
    if (curDistance[i] == 0){
      curDistanceOutput[i] = String(prevDistance[i]);
    }
    else{
      curDistance[i] = expFilter(alphaUltra, prevDistance[i], curDistance[i]); // filter distance values
      curDistanceCM[i] = String(curDistance[i]); // convert distance in cm to string
      curDistanceOutput[i] = curDistanceCM[i].substring(0,curDistanceCM[i].length()-1); // concatanate cm with decimal mm
    }  

    ultraArray[i] = curDistanceOutput[i].toFloat(); // convert output to float and assign to
    prevDistance[i] = curDistance[i]; // set previous distance to current 

  }
  
  ultraMsg.data = ultraArray; // update msg with curent array of values
  ultraPub.publish(&ultraMsg);
}

//-------------------------------------------------------------------------------------------------------------------------------------
//Get Gyroscope signals
//inputs: AccX, AccY => For integrating
//outputs: AngleRoll, AnglePitch => Integrated
//-------------------------------------------------------------------------------------------------------------------------------------
void gyroscopeData(void) {
  //if (startup) {delay(10); startup = false;} //Fixed by setting initial RateR,P,Y and AccX,Y,Z to 1 instead of 0. Ensure functionality with EMo
  if (micros() - LoopTimer > 4000) {
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(RateRoll, RatePitch, RateYaw); //Provides angular velocity in degrees/sec
      //RateRoll -> gyro x, RatePitch -> gyro y, RateYaw -> gyro z
    }

    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(AccX, AccY, AccZ); //Provides angular velocity in degrees/sec
    }

    AngleRoll = atan(AccY / sqrt(AccX * AccX + AccZ * AccZ)) * 1 / (3.142 / 180);
    AnglePitch = -atan(AccX / sqrt(AccY * AccY + AccZ * AccZ)) * 1 / (3.142 / 180);

    calculate_orientation();
  
    LoopTimer = micros();
  }
}

void calculate_orientation() {
  RateRoll -= RateCalibrationRoll;
  RatePitch -= RateCalibrationPitch;
  RateYaw -= RateCalibrationYaw;
  kalman_1d(KalmanAngleRoll, KalmanUncertaintyAngleRoll, RateRoll, AngleRoll);
  angular_velocity.x = KalmanAngleRoll = Kalman1DOutput[0];
  KalmanUncertaintyAngleRoll = Kalman1DOutput[1];
  kalman_1d(KalmanAnglePitch, KalmanUncertaintyAnglePitch, RatePitch, AnglePitch);
  angular_velocity.y = KalmanAnglePitch = Kalman1DOutput[0];
  KalmanUncertaintyAnglePitch = Kalman1DOutput[1];
  imuPub.publish(&angular_velocity);
}

//-------------------------------------------------------------------------------------------------------------------------------------
//1D Kalman filter
//inputs: KalmanState, KalmanUncertainty, KalmanInput, KalmanMeasurement => Kalman filter inputs
//outputs: Kalman1DOutput => Gives Kalman filter outputs
//-------------------------------------------------------------------------------------------------------------------------------------
void kalman_1d(float KalmanState, float KalmanUncertainty, float KalmanInput, float KalmanMeasurement) {
  //Don't forget that 0.004 is the time separation (4 ms)
  KalmanState = KalmanState + 0.004 * KalmanInput;
  KalmanUncertainty = KalmanUncertainty + 0.004 * 0.004 * 4 * 4;
  float KalmanGain = KalmanUncertainty * 1 / (1 * KalmanUncertainty + 2); //Edited from original document as Kalman Gain factor was too high for sensitivty of BLE 33 sense's IMU
  KalmanState = KalmanState + KalmanGain * (KalmanMeasurement - KalmanState);
  KalmanUncertainty = (1 - KalmanGain) * KalmanUncertainty;
  Kalman1DOutput[0] = KalmanState;
  Kalman1DOutput[1] = KalmanUncertainty;
}

float boxTemperatureData() {
  //HTS.begin() is necessary to turn on temp sensor
  if (HTS.begin()){
    currTemp = HTS.readTemperature();
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
    

  }
  //errorHexBits[3] = 'E';
  // disconnect
  dia_boxTemp.message = "Disconnect";
  dia_boxTemp.level = STALE; 
  boxTemp_data.temperature = currTemp;
  boxTempPub.publish(&boxTemp_data);  
}

void voltageSensorData() {
  sensorValue = analogRead(voltagePin);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  sensorValue = expFilter(alphaVoltSense, prevSensorValue, sensorValue);
  prevSensorValue = sensorValue;
  volt = ( sensorValue * 0.2008451735 ) - 80.97365371; //Linear regression line-of-best-fit

  float voltPercent = ( sensorValue - Vmin ) / diff;
  
  voltConverterMsg.voltage = volt;
  voltConverterMsg.percentage = voltPercent;

  voltConverterPub.publish(&voltConverterMsg);
}

void voltageConverterTempData() {

  Vo_v = analogRead(voltageConverterTemp);
  R2_v = R1_v * (1023.0 / (float)Vo_v - 1.0);
  logR2_v = log(R2_v);
  T_v = (1.0 / (c1 + c2*logR2_v + c3*logR2_v*logR2_v*logR2_v));
  T_v = T_v - 273.15;

  voltConverterTemp_msg.temperature = T_v;

  voltConverterTempPub.publish(&voltConverterTemp_msg);

  if (T_v <= 0) { 
    dia_voltConverterTemp.message = "Underheat Emergency"; 
    dia_voltConverterTemp.level = ERROR;
  }
  else if ((0 < T_v) && (T_v <= 5)) {
    dia_voltConverterTemp.message = "Underheat Warning"; 
    dia_voltConverterTemp.level = WARN;
  } 
  else if ((5 < T_v) && (T_v < 65)) {
    dia_voltConverterTemp.message = "OK";
    dia_voltConverterTemp.level = OK;
  }
  else if ((65 <= T_v) && (T_v < 70)) {
    dia_voltConverterTemp.message = "Overheat Warning";
    dia_voltConverterTemp.level = WARN;
  }
  else if( T_v >= 70) {
    dia_voltConverterTemp.message = "Overheat Emergency";
    dia_voltConverterTemp.level = ERROR;
  }
}

void batteryTempData(){

  Vo_b = analogRead(batteryTemp);
  R2_b = R1_b * (1023.0 / (float)Vo_b - 1.0);
  logR2_b = log(R2_b);
  T_b = (1.0 / (c1 + c2*logR2_b + c3*logR2_b*logR2_b*logR2_b));
  T_b = T_b - 273.15;

  batteryTemp_msg.temperature = T_b;

  batteryTempPub.publish(&batteryTemp_msg);

  if (T_b <= 30) { 
    dia_batteryTemp.message = "Underheat Emergency"; 
    dia_batteryTemp.level = ERROR;
  }
  else if ((30 < T_b) && (T_b <= 35)) {
    dia_batteryTemp.message = "Underheat Warning"; 
    dia_batteryTemp.level = WARN;
  } 
  else if ((35 < T_b) && (T_b < 60)) {
    dia_batteryTemp.message = "OK";
    dia_batteryTemp.level = OK;
  }
  else if ((60 <= T_b) && (T_b < 80)) {
    dia_batteryTemp.message = "Overheat Warning";
    dia_batteryTemp.level = WARN;
  }
  else if( T_b >= 80) {
    dia_batteryTemp.message = "Overheat Emergency";
    dia_batteryTemp.level = ERROR;
  }
}
/* WAIT UNTIL MEETING TO ASK GREG IF SECOND SERIAL WILL BREAK BOARD
void gps(){

  while (Serial2.available() > 0)
  {
    if (gps.encode(Serial2.read()) && gps.time.second() != lastSecond)
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
*/
double expFilter(double alpha, double prevReading, double curReading){ 
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}

