/*
 * MoogMotor.cpp - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Moldkow Mar 27, 2021
 */

#include "Arduino.h"
#include "HardwareSerial.h"
#include "MoogMotor.h"


MoogMotor::MoogMotor(int id, HardwareSerial* serial)
{
  serial = serial;
  serial->setTimeout(50); // In Milliseconds
  id = id;
}

MoogMotor::MoogMotor(){}

void MoogMotor::enable(){
  sendCommand("MDT");
  sendCommand("MDB");
  sendCommand("BRKSRV");   // Engage Break When not Moving
  sendCommand("G");        // Go Command to turn on coils
  sendCommand("X");        // Send Stop Request'
}

bool MoogMotor::sendCommand( String command){
  char sendAddr = ((uint8_t) MoogMotor::id | 0b10000000);
  serial->print(sendAddr);
  serial->print(command);
  serial->print(" ");
}

void MoogMotor::statusCheck(){
  statusCode = getData("RW(0) ");
  statusCode1 = getData("RW(1) ");
  statusCode2 = getData("RW(2) ");
  statusCode3 = getData("RW(3) ");
  statusCode4 = getData("RW(4) ");
  statusCode5 = getData("RW(5) ");
  statusCode6 = getData("RW(6) ");
  statusCode7 = getData("RW(7) ");
}

int MoogMotor::getData(char command[]){
  sendCommand(command);
  if (serial->available()) connected = true;
  else connected = false;
  return int(serial->parseInt());
}

unsigned int MoogMotor::getStatusCode(){
  return MoogMotor::statusCode;
}

bool MoogMotor::isConnected(){
  return MoogMotor::connected;
}

bool MoogMotor::resetStatusCodes(){
  sendCommand("ZS ");       // Clear All Warning Tags
  //park();
  return statusCode == DRIVEREADY;
}

void MoogMotor::stop()
{
  sendCommand("X"); //Standard stop command
}

/* ESHUTDOWN
 * This command will imediatly kill power to the motor coils AND throw an overcurrent and positon
 * error to prevent further use. Use this function in case of an ESTOP button press only. This 
 * command WILL NOT ENGAGE BREAKING. To do a hard stop with breaking, call the stop() function.
 */
void MoogMotor::ESHUTDOWN(){
  sendCommand("S");    // Hard Stop
  sendCommand("OFF");  // Turn Coils Off
  sendCommand("B(0,0)=0");
}

boolean MoogMotor::setVelocity(float rpm, float acceleration){
  // RPM Can only be from -1 to 1
    
  if(abs(rpm) <= 1 && 0 <= acceleration <= 1){
    //rpm = rpm * RPMMAX;
    acceleration = acceleration * ACCMAX;

    sendCommand("MV");     //Set to motor velocity mode
    sendCommand("VT="+String(rpm));       //Set the rpm
    sendCommand("ADT="+String(acceleration));      //Set the acceration/deceleration
    sendCommand("G");      //Go Command
    return true;
  }
  return false;
}

boolean MoogMotor::setTorque(float torque){
  if(abs(torque) <= 1){
    torque = torque * TRQMAX;
    
    sendCommand("MT");     //Set motor to torque mode
    sendCommand("T=" + String(torque));        //Set the torque value
    sendCommand("G");     //Go command
    
    return true;
  }
  return false;
}

boolean MoogMotor::setPosition(float position, float velocity, float acceleration){
  
  if(abs(position) <= 1 && 0 <= acceleration <=1){
    position = position * POSMAX;         
    acceleration = acceleration * ACCMAX; 
    
    
    sendCommand("MP");                          //Set to motor position mode
    sendCommand("VT=" + String(velocity));      //Set the rpm
    sendCommand("ADT=" + String(acceleration)); //Set the acceration/deceleration
    sendCommand("PT=" + String(position));      //Set the position
    sendCommand("G");                           //Go Command
    return true;                                //Retrun a true to confirm operation complete
  }
  return false;
}

void MoogMotor::holdOFF(){
  sendCommand("BRKRLS");   // Disengage breaking system
  sendCommand("OFF");       // Turn Coils Off
}

void MoogMotor::holdON(){
  sendCommand("BRKSRV");   // Engage Break When not Moving
  sendCommand("G");        // Go Command to turn on coils
  sendCommand("X");        // Send Stop Request
}

