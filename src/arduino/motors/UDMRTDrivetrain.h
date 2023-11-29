


#ifndef UDMRTDrivetrain_h
#define UDMRTDrivetrain_h

#define PARK 0
#define DRIVE 1
#define NEUTRAL 2
#define ROVERWIDTH 1      // In Meters
#define WHEELRADIUS 0.032 // In Meters
#define GEARRATIO 40      // Number of input shaft roations for every output shaft roation

#include "MoogMotor.h"
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Accel.h>

 class UDMRTDrivetrain{

  public:
    UDMRTDrivetrain(int numberOfMotors, HardwareSerial* serialPort);
    void ESHUTDOWN();
    void stop();
    void off();
    void setup(int leftMotors[], int rightMotors[]);
    void setGear(int gear = PARK);
    bool drive(float kmPerHour, float degPerSecond, float acc);
    void rosTankDrive(float kmPerHour, float degPerSecond, float acc);
    void reset();
    int* getStatus();


  private:
    MoogMotor motor[13];
    int* leftMotors;
    int* rightMotors;
    bool sendCommand(String command, int id = 0);
    bool rosSetup;
    HardwareSerial *serial = NULL;
    int numberOfMotors = 0;

};

#endif