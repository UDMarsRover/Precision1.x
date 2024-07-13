

#include <ros.h>

#include <Arduino.h>
#include "udmrt_gps.h"
#include <sensor_msgs/NavSatFix.h>

ros::NodeHandle node;
sensor_msgs::NavSatFix test;

diagnostic_msgs::DiagnosticStatus diag_msg;

UDMRT_GPS hi("gps",&node);
ros::Publisher dataPub("/emo/gps", &(hi.data_msg));
ros::Publisher diagPub("/emo/status/gps", &(hi.diag_msg));



void setup(){
  node.initNode();
  hi.init(&dataPub,&diagPub);

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
  //diag_msg_buf.message = "Unable to start serial connection with GPS sensor!!";
  //diag_msg_buf.level = ERROR;
  delay(500);
  hi.spin();
  rgbControl(1,0,1);
  delay(500);
  //hi.diag_msg.message = "Connected to onbard sensor over serial";
  //hi.diag_msg.level = OK;

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