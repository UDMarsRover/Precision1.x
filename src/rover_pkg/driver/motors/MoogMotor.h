/*
 * MoogMotor.h - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Molskow on Mar 27, 2021
 */

#ifndef MoogMotor_h
#define MoogMotor_h

#include "Arduino.h"
#include "HardwareSerial.h"


//=================================================//
//          Define Status Code Values              //
//=================================================//
#define ACTIVE        0b1000000000000000  //0x8000
#define FAULTSUM      0b0100000000000000  //0x4000
#define OVERHEAT      0b0010000000000000  //0x2000
#define UNDERVOLTAGE  0b0001000000000000  //0x1000
#define OVERCURRENT   0b0000100000000000  //0x0800
#define BUSVOLTAGE    0b0000010000000000  //0x0400
#define DRIVEENABLE   0b0000001000000000  //0x0200
#define BATTERY       0b0000000100000000  //0x0100
#define POSITION      0b0000000010000000  //0x0080
#define VELOCITY      0b0000000001000000  //0x0040
#define DEDT          0b0000000000100000  //0x0020
#define HISTPOSITIVE  0b0000000000010000  //0x0010
#define HISTNEGATIVE  0b0000000000001000  //0x0008
#define WATCHDOG      0b0000000000000100  //0x0004
#define ABDCHECKSUM   0b0000000000000010  //0x0002
#define FEEDBACK      0b0000000000000001  //0x0001
  

//1010010
//1000010



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
     

     struct statusBufferStruct {
      unsigned int error                    : 1;
      unsigned int active                   : 1;
      unsigned int underVoltageFault        : 1;
      unsigned int overCurrentFault         : 1;
      unsigned int overHeatFault            : 1;
      unsigned int positionErrorFault       : 1;
      unsigned int busVoltageFault          : 1;
      unsigned int velocityLimitFault       : 1;
      unsigned int dedtFault                : 1;
      unsigned int historicalPositiveFault  : 1;
      unsigned int historicalNegativeFault  : 1;
      unsigned int watchdogFault            : 1;
      unsigned int abdChecksumFault         : 1;
      unsigned int feedbackFault            : 1;
      unsigned int driveEnableFault         : 1;
      unsigned int absBatteryFault          : 1;
     };
    statusBufferStruct statusBuffer;
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
    void updateStatusCode(unsigned int , bool);
    bool sendCommand(String);
 };

#endif
