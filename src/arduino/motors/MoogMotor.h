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

#define ACCMAX 1000
#define RPMMAX 4423680
#define TRQMAX 32767
#define POSMAX 32768
#define REVSPERROTATION 4000



class MoogMotor
 {
  public:
    MoogMotor();
    MoogMotor(int id, HardwareSerial* associatedSerial);
    boolean setVelocity(float rpm, float acceleration);
    boolean setTorque(float torque);
    boolean setPosition(float value,float velocity, float acceleration);
    
    
    void ESHUTDOWN();
    void stop();
    void enable();
    void off();
    void holdON();
    void holdOFF();

    void statusCheck();
    bool isConnected();
    unsigned int getStatusCode();
    bool resetStatusCodes();
    int getData(char[]);
    bool sendCommand(String command);
    int id;
    
  private:
    unsigned int statusCode:17;
    unsigned int statusCode1:17;
    unsigned int statusCode2:17;
    unsigned int statusCode3:17;
    unsigned int statusCode4:17;
    unsigned int statusCode5:17;
    unsigned int statusCode6:17;
    unsigned int statusCode7:17;
    HardwareSerial *serial = NULL;
    bool connected;
    
  
 };
#endif