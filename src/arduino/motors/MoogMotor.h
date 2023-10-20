/*
 * MoogMotor.h - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Molskow on Mar 27, 2021
 */

#ifndef MoogMotor_h
#define MoogMotor_h

#include "Arduino.h"
#include "HardwareSerial.h"
#include "MoogMotorStatusWords.h"

class MoogMotor
 {
  public:
  
     MoogMotor(HardwareSerial* associatedSerial);
    //boolean driveMotor(MotorMode operationMode, float value);
     boolean setVelocity(float rpm, float acceleration);
     boolean setTorque(float torque);
     boolean setPosition(float value,float velocity, float acceleration);
     
     
     void ESHUTDOWN();
     void stop();
     void setUp();
     void off();
     void neutral();
     void park();
     

    void statusCheck();
    bool isConnected();
    unsigned int getStatusCode();
    bool resetStatusCodes();
    void drive();
    int getData(char[]);
    
    
  private:
    unsigned int statusCode:17;
    unsigned int statusCode1:17;
    unsigned int statusCode2:17;
    unsigned int statusCode3:17;
    unsigned int statusCode4:17;
    unsigned int statusCode5:17;
    unsigned int statusCode6:17;
    unsigned int statusCode7:17;
    bool connected;
    HardwareSerial *serial = NULL;
    bool sendCommand(String);
 };

#endif