


#ifndef UDMRTDrivetrain_h
#define UDMRTDrivetrain_h

#define PARK 0
#define DRIVE 1
#define NEUTRAL 2


#include "MoogMotor.h"
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Accel.h>

 class UDMRTDrivetrain{

  public:
    UDMRTDrivetrain(int numberOfMotors, HardwareSerial* serialPort, float roverWidth=1.2, float tireDiameter=0.254);
    void ESHUTDOWN();
    void stop();
    void off();
    void setup(int leftMotors[], int rightMotors[], int gearRatios[]);
    void setGear(int gear = PARK);
    bool drive(float kmPerHour, float degPerSecond, float acc);
    void rosTankDrive(float kmPerHour, float degPerSecond, float acc);
    void reset();
    int* getStatus();


  private:
    MoogMotor motor[7];
    int* leftMotors;
    int* rightMotors;
    bool sendCommand(String command, int id=0);
    bool rosSetup;
    HardwareSerial *serial = NULL;
    int numberOfMotors;
    float roverWidth;
    float tireDiameter;

};

#endif