

#include <ros.h>

#include <Arduino.h>
#include "src/udmrt_gps/udmrt_gps.h"
#include "src/udmrt_imu/udmrt_imu.h"


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





void setup(){
  
  node.initNode();
  imu.init(&imuData,&imuDiag);
  gps.init(&gpsData,&gpsDiag);
  

  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);

  rgbControl(1,0,0);
  delay(500);
  rgbControl(0,1,0);
  delay(500);
  rgbControl(0,0,1);
  delay(500);
  
  // setup
  rgbControl(1,0,0);
}

void loop(){
  rgbControl(0,1,0);
  node.spinOnce();
  delay(500);
  gps.spin();
  imu.spin();
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