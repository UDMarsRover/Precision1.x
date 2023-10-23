/*
 * MoogMotor.cpp - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Moldkow Mar 27, 2021
 */

#include "Arduino.h"
#include "HardwareSerial.h"
#include "MoogMotor.h"


MoogMotor::MoogMotor(HardwareSerial* associatedSerial)
{
  serial = associatedSerial;
  serial->setTimeout(50); // In Milliseconds
  
  //initSerial();
}

boolean MoogMotor::setVelocity(int motorAdd, float rpm, float acceleration){
    // RPM Can only be from -1 to 1
    
    //if(abs(rpm) <= 1 && 0 <= acceleration <= 1){
        

    //vel = rpm * (32768 / 8000) * 65536;
    rpm = rpm * 4423680;   // Motor ranged from +- 2,147,483,647
    //rpm = rpm * 32768;
    
    acceleration = int(acceleration * 1000); //Range 0 -> 2147483647
    sendCommand("MV",motorAdd);     //Set to motor velocity mode
    sendCommand("VT="+String(rpm),motorAdd);       //Set the rpm
    sendCommand("ADT=" + String(acceleration),motorAdd);      //Set the acceration/deceleration
    sendCommand("G",motorAdd);      //Go Command
    
}

boolean MoogMotor::setTorque(float torque){
    if(abs(torque) <= 1){
        torque = int(torque * 32767.0);//Ranges from +- 32767
        
        serial->print("MT \r");     //Set motor to torque mode
        serial->print("T=");        //Set the torque value
        serial->print(torque);
        serial->print("\r");
        
        
        serial->print("G \r");     //Go command
        delay(1);
        return true;
    }
    return false;
    
}

boolean MoogMotor::setPosition(float value, float velocity, float acceleration){
    
    if(abs(value) <= 1 && 0 <= acceleration <=1){
        value = int(value * 32768.0);   // Motor ranged from +- 2147483647
        acceleration = int(acceleration * 2147483647.0); //Range 0 -> 2147483647
        
        
        serial->print("MP ");     //Set to motor position mode
        serial->print("VT=");       //Set the rpm
        serial->print(velocity);
        serial->print(" ");
        serial->print("ADT=");      //Set the acceration/deceleration
        serial->print(acceleration);
        serial->print(" ");
        serial->print("PT=");
        serial->print(value);       //Set the position
        serial->print(" ");
        
        serial->print("G ");      //Go Command
        delay(1);
        return true;                //Retrun a true to confirm operation complete
    }
    return false;
}

/* ESHUTDOWN
 * This command will imediatly kill power to the motor coils AND throw an overcurrent and positon
 * error to prevent further use. Use this function in case of an ESTOP button press only. This 
 * command WILL NOT ENGAGE BREAKING. To do a hard stop with breaking, call the stop() function.
 */
void MoogMotor::ESHUTDOWN(){
  serial->print("S ");    // Hard Stop
  serial->print("OFF ");  // Turn Coils Off
  serial->print("B(0,0)=0 ");
}

void MoogMotor::stop()
{
  serial->print("X "); //Standard stop command
}

void MoogMotor::setUp()
{

  serial->begin(9600);
  //serial->write("AMPS=1000 ");
  sendCommand("SADDR0");
  delay(500);
  sendCommand("SADDR1");
  delay(500);
  sendCommand("ECHO",1);
  delay(500);
  sendCommand("SLEEP",1);
  delay(500);
  sendCommand("SADDR2");
  delay(500);
  sendCommand("ECHO",2);
  delay(500);
  sendCommand("SLEEP",2);
  delay(500);
  sendCommand("SADDR3");
  delay(500);
  sendCommand("ECHO",3);
  delay(500);
  sendCommand("SLEEP",3);
  delay(500);
  sendCommand("SADDR4");
  delay(500);
  sendCommand("WAKE");


  sendCommand("EIGN(2)");
  sendCommand("EIGN(3)");
  sendCommand("ZS");
  sendCommand("SLD");

  park(1);
  park(2);
  park(3);
  park(4);

  //statusCheck();
}

void MoogMotor::drive(){
  serial->print("MDT ");
  serial->print("MDB ");
  serial->print("BRKSRV ");   // Engage Break When not Moving
  serial->print("G ");        // Go Command to turn on coils
  serial->print("X ");        // Send Stop Request'
}

void MoogMotor::neutral(){
  serial->print("BRKRLS ");   // Disengage breaking system
  serial->print("OFF ");       // Turn Coils Off
  
}

void MoogMotor::park(int motorAdd){
  sendCommand("BRKSRV", motorAdd);   // Engage Break When not Moving
  sendCommand("G",motorAdd);        // Go Command to turn on coils
  sendCommand("X", motorAdd);        // Send Stop Request
  
}

bool MoogMotor::sendCommand( String command, int motorAdd){
  //char output[sizeof(command) + 2];
  char sendAddr = ((uint8_t) motorAdd | 0b10000000);
  //strcpy(output, sendAddr);
  //strcat(output, command);
  //strcat(output, " ");

  //serial->print(output);

  serial->print(sendAddr);
  serial->print(command);
  serial->print(" ");
}

int MoogMotor::getData(char command[]){
  sendCommand(command);
  if (serial->available()) connected = true;
  else connected = false;
  return int(serial->parseInt());
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

bool MoogMotor::isConnected(){
  return MoogMotor::connected;
}

unsigned int MoogMotor::getStatusCode(){
  return MoogMotor::statusCode;
}

bool MoogMotor::resetStatusCodes(){
  serial->print("ZS ");       // Clear All Warning Tags
  //park();
  return statusCode == DRIVEREADY;
}