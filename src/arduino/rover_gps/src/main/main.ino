#include <Arduino.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <float.h>
#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/NavSatFix.h>
#include <sensor_msgs/NavSatStatus.h>

// IMPORTANT: This code is written specifically for a GPS unit that receives signal at a frequency of 1Hz.
// If a GPS with a higher refresh rate is used in the future, this code will need to be reworked. -Kaiden

TinyGPSPlus gps;
//Boolean that keeps track of whether the previous reading was zero (prevents duplicate error messages)
bool error = false;
int lastSecond = -1;

sensor_msgs::NavSatFix gpsMessage;
ros::NodeHandle gpsNode;

ros::Publisher pub("GPS", &gpsMessage);

void setup() {
  gpsNode.initNode();
  gpsNode.advertise(pub);
  //Serial.begin(9600);
  Serial2.begin(9600);
}

void loop() 
{
  gpsNode.spinOnce();

  while (Serial2.available() > 0)
  {
    if (gps.encode(Serial2.read()) && gps.time.second() != lastSecond)
    {
      lastSecond = gps.time.second();
      if(gps.location.lat() == 0 && gps.location.lng() == 0)
      {
        if (!error)
        {
          gpsMessage.status.status = 14;
        }
        error = true;
      }
      else if (gps.location.age() > 500)
      {
        if (!error)
        {
          gpsMessage.status.status = 14;
        }
        error = true;
      }
      else
      {
        gpsMessage.header.stamp.sec = gps.time.second();
        gpsMessage.header.stamp.nsec = gps.time.centisecond() * 10000000;
        gpsMessage.latitude = gps.location.lat();
        gpsMessage.longitude = gps.location.lng();
        gpsMessage.altitude = gps.altitude.meters();
        gpsMessage.status.status = 15;
        error = false;
      }
    }
  }

  if (millis() > 1000 && gps.charsProcessed() < 10)
  {
    
    gpsMessage.status.status = 14;
    gpsMessage.latitude = 0;
    gpsMessage.longitude = 0;
    //while(true);
  }

  pub.publish(&gpsMessage);
}

  