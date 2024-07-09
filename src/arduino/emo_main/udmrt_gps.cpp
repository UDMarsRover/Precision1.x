
#include "udmrt_gps.h"

UDMRT_GPS::UDMRT_GPS(){
  UDMRT_GPS::gpsConnected = false;
  UDMRT_GPS::gpsError = false;
 
}

bool UDMRT_GPS::init(){
   Serial1.begin(9600);

  int count = 50;
  while (!Serial1 && (count > 0)){
    count ++;
    delay(100);
  }
  return Serial1;
}



void UDMRT_GPS::get_data(){

  while (Serial1.available() > 0)
  {
    if (UDMRT_GPS::gps.encode(Serial1.read()) && gps.time.second() != lastSecond)
    {
      lastSecond = UDMRT_GPS::gps.time.second();
      if(UDMRT_GPS::gps.location.lat() == 0 && gps.location.lng() == 0)
      {
        if (!gpsError)
        {
          UDMRT_GPS::output_msg.status.status = 14;
        }
        gpsError = true;
      }
      else if (UDMRT_GPS::gps.location.age() > 500)
      {
        if (!gpsError)
        {
          UDMRT_GPS::output_msg.status.status = 14;
        }
        gpsError = true;
      }
      else
      {
        UDMRT_GPS::output_msg.header.stamp.sec = gps.time.second();
        UDMRT_GPS::output_msg.header.stamp.nsec = gps.time.centisecond() * 10000000;
        UDMRT_GPS::output_msg.latitude = gps.location.lat();
        UDMRT_GPS::output_msg.longitude = gps.location.lng();
        UDMRT_GPS::output_msg.altitude = gps.altitude.meters();
        UDMRT_GPS::output_msg.status.status = 15;
        gpsError = false;
      }
    }
  }

  if (millis() > 1000 && UDMRT_GPS::gps.charsProcessed() < 10)
  {
    
    UDMRT_GPS::output_msg.status.status = 14;
    UDMRT_GPS::output_msg.latitude = 0;
    UDMRT_GPS::output_msg.longitude = 0;
    //while(true);
  }

  
}