
#ifndef UDMRT_GPS_H
#define UDMRT_GPS_H

#include <TinyGPSPlus.h>
#include <float.h>
#include <sensor_msgs/NavSatFix.h>
#include <diagnostic_msgs/DiagnosticStatus.h>


class UDMRT_GPS{
  /** IMPORTANT: This code is written specifically for a GPS unit that receives signal at a frequency of 1Hz. 
    If a GPS with a higher refresh rate is used in the future, this code will need to be reworked. -Kaiden
  */

  public:

    UDMRT_GPS();
    bool spin();
    bool init();

  private:
    TinyGPSPlus gps; //Boolean that keeps track of whether the previous reading was zero (prevents duplicate error messages)
    bool gpsConnected;
    bool gpsError;
    int lastSecond = -1;
    sensor_msgs::NavSatFix output_msg;
    diagnostic_msgs::DiagnosticStatus diag_msg;
    void get_data();


};

#endif