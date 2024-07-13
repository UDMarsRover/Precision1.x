
#ifndef UDMRT_GPS_H
#define UDMRT_GPS_H

#include "src/udmrt_sensor.cpp"
#include <TinyGPSPlus.h>
#include <float.h>
#include <sensor_msgs/NavSatFix.h>


class UDMRT_GPS: public UDMRT_Sensor<sensor_msgs::NavSatFix>{
  /** IMPORTANT: This code is written specifically for a GPS unit that receives signal at a frequency of 1Hz. 
    If a GPS with a higher refresh rate is used in the future, this code will need to be reworked. -Kaiden
  */

  public:
    UDMRT_GPS(char* name, ros::NodeHandle* node);

    void updateData() override;

    bool init(ros::Publisher* dataPublisher, ros::Publisher* diagnosticPublisher);

    void spin();

  private:
    TinyGPSPlus gps; //Boolean that keeps track of whether the previous reading was zero (prevents duplicate error messages)
    bool gpsConnected;
    bool gpsError;
    int lastTimeStamp = millis();

    void errorState();
    void warningState();



};

#endif