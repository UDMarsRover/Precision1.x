/*
 * MoogMotor.cpp - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Moldkow Mar 27, 2021
 */


#include "MoogMotor.h"



MoogMotor::MoogMotor(int id, HardwareSerial* serial, int gearRatio, int resolution, int samplerate, int delayTime)
{  
  MoogMotor::delayTime = delayTime;
  MoogMotor::gearRatio = gearRatio;
  MoogMotor::resolution = resolution;
  MoogMotor::sampleRate = samplerate;
  MoogMotor::serial = serial;
  MoogMotor::id = id;
  
  MoogMotor::sendCommand("WAKE",true);
  MoogMotor::sendCommand("ECHO",true);

  //Remove Software Limits
  MoogMotor::sendCommand("EIGN(2)",true);
  MoogMotor::sendCommand("EIGN(3)",true);
  MoogMotor::sendCommand("SLD",true);
  MoogMotor::sendCommand("ZS",true);
  MoogMotor::enable();
  //Serial.println("Starting a motor");
}

MoogMotor::MoogMotor(){}

bool MoogMotor::setID(){

  if (MoogMotor::id != 0) {

    String setAddress = "SADDR" + String(id);
    sendCommand(setAddress,true);  // Set address of motor
    delay(MoogMotor::delayTime);

    int setID = MoogMotor::getData("RADDR");
    //Serial.print("  ID:");
    //Serial.println(setID);
    bool complete = (setID == MoogMotor::id);

    if (!complete && (MoogMotor::setIDTrys <= MoogMotor::setIDMax)) {
      MoogMotor::setIDTrys += 1;
      delay(MoogMotor::delayTime);
      MoogMotor::setID();
    }
    
    //Serial.print("  Final ID: ");
    //Serial.println(setID);
    return complete;
  }
  return true;
}

void MoogMotor::enable(){
  sendCommand("MDT");
  sendCommand("MDB");
  sendCommand("BRKSRV");   // Engage Break When not Moving
  sendCommand("G");        // Go Command to turn on coils
  sendCommand("X");        // Send Stop Request'
}

bool MoogMotor::sendCommand(String command, bool global){
  char sendAddr = ((uint8_t) MoogMotor::id | 0b10000000);

  if (global) sendAddr = ((uint8_t) 0 | 0b10000000);
  String messageOut = sendAddr + command + " ";

  Serial.println(String(MoogMotor::id) + " " + messageOut);
  Serial1.print(messageOut);
  //Serial.println("Made & snet Output String: "+command);
  //delay(50);
  //Serial.println("Sent Output String");
  //delay(50);
  delay(MoogMotor::delayTime);
}

void MoogMotor::statusCheck(){
  statusCode = getData("RW(0)");
  statusCode1 = getData("RW(1)");
  statusCode2 = getData("RW(2)");
  statusCode3 = getData("RW(3)");
  statusCode4 = getData("RW(4)");
  statusCode5 = getData("RW(5)");
  statusCode6 = getData("RW(6)");
  statusCode7 = getData("RW(7)");
}

int MoogMotor::getData(char command[]){
  MoogMotor::sendCommand(command);
  if (MoogMotor::serial->available()) MoogMotor::connected = true;
  else MoogMotor::connected = false;
  int data = MoogMotor::serial->parseInt();
  return data;
}

unsigned int MoogMotor::getStatusCode(){
  return MoogMotor::statusCode;
}

bool MoogMotor::isConnected(){
  return MoogMotor::connected;
}

bool MoogMotor::resetStatusCodes(){
  sendCommand("ZS");       // Clear All Warning Tags
  //park();
  return statusCode == 1;
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
void MoogMotor::ESTOP(){
  sendCommand("S");    // Hard Stop
  sendCommand("OFF");  // Turn Coils Off
  sendCommand("B(0,0)=0");
}

boolean MoogMotor::setVelocity(float rps, float acceleration){
  // RPM Can only be from -1 to 1
    
  //if(abs(rpm) <= 1 && 0 <= acceleration <= 1){
    //rpm = rpm * RPMMAX;
  acceleration = acceleration * ACCMAX;
  
  double eCounts = rps * MoogMotor::gearRatio * (MoogMotor::resolution/MoogMotor::sampleRate) * 65536;

  //Serial.print("E Counts: ");
  //Serial.println(eCounts);

  //Serial.print(eCounts);
  //Serial.print(", ");
  //Serial.println(acceleration);
    
    
  MoogMotor::sendCommand("MV");     //Set to motor velocity mode
  MoogMotor::sendCommand("VT="+String(eCounts));       //Set the rps
  MoogMotor::sendCommand("AT="+String(acceleration));      //Set the acceration/deceleration
  MoogMotor::sendCommand("G");      //Go Command


  return true;
  //}
  //return false;
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

