

#include <ros.h>

#include <Arduino.h>
#include "src/udmrt_gps/udmrt_gps.h"
#include "src/udmrt_imu/udmrt_imu.h"
#include "src/udmrt_thermistor/udmrt_thermistor.h"
#include "src/udmrt_temperature/udmrt_temperature.h"
#include "src/udmrt_voltage_sensor/udmrt_voltage_sensor.h"
#include "src/udmrt_ultrasonic/udmrt_ultrasonic.h"


ros::NodeHandle node;

/**
 * @brief GPS Definitions
 * 
 */
UDMRT_GPS gps("gps",&node);
ros::Publisher gpsData("/emo/gps", &(gps.data_msg));
ros::Publisher gpsDiag("/emo/status/gps", &(gps.diag_msg));

/**
 * @brief IMU Definitions
 * 
 */
UDMRT_IMU imu("IMU",&node,30,60,30,60);
ros::Publisher imuData("/emo/imu",&(imu.data_msg));
ros::Publisher imuDiag("/emo/status/imu",&(imu.diag_msg));

/**
 * @brief Battery Temperature Defitions
 * 
 */
UDMRT_Thermistor batteryTemp("batteryTemperature",&node,A1,2000,2010,3965,80,0,60,30);
ros::Publisher batTempData("/emo/batteryTemperature",&(batteryTemp.data_msg));
ros::Publisher batTempDiag("/emo/status/batteryTemperature",&(batteryTemp.diag_msg));

/**
 * @brief Box Temperature Defitions
 * 
 */
UDMRT_Temperature boxTemp("boxTemperature",&node);
ros::Publisher boxTempData("/emo/boxTemperature",&(boxTemp.data_msg));
ros::Publisher botTempDiag("/emo/status/boxTemperature",&(boxTemp.diag_msg));

/**
 * @brief Voltage Converter Temperature Defitions
 * 
 */
UDMRT_Thermistor voltageConverterTemp("batteryTemperature",&node,A2,100000,100100,4615,80,0,60,30);
ros::Publisher voltTempData("/emo/voltageConverterTemperature",&(voltageConverterTemp.data_msg));
ros::Publisher voltTempDiag("/emo/status/voltageConverterTemperature",&(voltageConverterTemp.diag_msg));

/**
 * @brief Voltage Sensor Definitions
 * 
 */
UDMRT_Voltage_Sensor batteryVoltage("voltageVensor",&node,A0,45.5,47.5);
ros::Publisher voltData("/emo/batteryVoltage",&(batteryVoltage.data_msg));
ros::Publisher voltDiag("/emo/status/batteryVoltage",&(batteryVoltage.diag_msg));

/**
 * @brief Ultrasonic Definitions
 * 
 */
#define NE_TRIG 4
#define NE_ECHO 5
UDMRT_Ultrasonic ultraNE("ultraNE",&node,NE_TRIG,NE_ECHO);
ros::Publisher ultraNEData("/emo/ultraNE",&(ultraNE.data_msg));
ros::Publisher ultraNEDiag("/emo/status/ultraNE",&(ultraNE.diag_msg));
#define NW_TRIG 2
#define NW_ECHO 3
UDMRT_Ultrasonic ultraNW("ultraNW",&node,NW_TRIG,NW_ECHO);
ros::Publisher ultraNWData("/emo/ultraNW",&(ultraNW.data_msg));
ros::Publisher ultraNWDiag("/emo/status/ultraNW",&(ultraNW.diag_msg));
#define SE_TRIG 8
#define SE_ECHO 9
UDMRT_Ultrasonic ultraSE("ultraSE",&node,SE_TRIG,SE_ECHO);
ros::Publisher ultraSEData("/emo/ultraSE",&(ultraSE.data_msg));
ros::Publisher ultraSEDiag("/emo/status/ultraSE",&(ultraSE.diag_msg));
#define SW_TRIG 6
#define SW_ECHO 7
UDMRT_Ultrasonic ultraSW("ultraSW",&node,SW_TRIG,SW_ECHO);
ros::Publisher ultraSWData("/emo/ultraSW",&(ultraSW.data_msg));
ros::Publisher ultraSWDiag("/emo/status/ultraSW",&(ultraSW.diag_msg));



void setup(){

  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);

  rgbControl(1,0,0);
  delay(500);
  rgbControl(0,1,0);
  delay(500);
  rgbControl(0,0,1);
  delay(500);
  
  node.initNode();
  imu.init(&imuData,&imuDiag);
  gps.init(&gpsData,&gpsDiag);
  batteryTemp.init(&batTempData,&batTempDiag);
  boxTemp.init(&boxTempData,&botTempDiag);
  voltageConverterTemp.init(&voltTempData,&voltTempDiag);
  batteryVoltage.init(&voltData,&voltDiag);
  ultraNE.init(&ultraNEData,&ultraNEDiag);
  ultraNW.init(&ultraNWData,&ultraNWDiag);
  ultraSE.init(&ultraSEData,&ultraSEDiag);
  ultraSW.init(&ultraSWData,&ultraSWDiag);
  

  rgbControl(1,0,0);
}

void loop(){
  rgbControl(0,1,0);
  node.spinOnce();
  delay(500);
  gps.spin();
  imu.spin();
  batteryTemp.spin();
  boxTemp.spin();
  voltageConverterTemp.spin();
  batteryVoltage.spin();
  ultraNE.spin();
  ultraNW.spin();
  ultraSE.spin();
  ultraSW.spin();
  rgbControl(1,0,1);
  delay(500);

}

void rgbControl(float red, float green, float blue){
  /** @brief This function controls the onboard LEDs
    This function control the onboard LED of the adruino and allows for analog control

    @param red: 1-0 value for red intencity
    @param green: 1-0 value for green intencity
    @param blue: 1-0 value for blue intencity

    @return None
  */
  analogWrite(22,(1023 - (1023 * red)));
  analogWrite(23,(1023 - (1023 * green)));
  analogWrite(24,(1023 - (1023 * blue)));

}