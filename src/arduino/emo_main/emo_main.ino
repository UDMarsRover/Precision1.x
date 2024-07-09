

#include <ros.h>

#include <Arduino.h>
#include "src/udmrt_sensor.cpp"
#include <sensor_msgs/NavSatFix.h>

ros::NodeHandle node;
sensor_msgs::NavSatFix test;
UDMRT_Sensor <sensor_msgs::NavSatFix> hi("gps","emo/gps","emo/status/gps");

void setup(){
  node.initNode();
  hi.init(&node);

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
  rgbControl(0,0,1);
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