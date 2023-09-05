/*
 * MoogMotor.cpp - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Moldkoe Mar 27, 2021
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

boolean MoogMotor::setVelocity(float rpm, float acceleration){
    // RPM Can only be from -1 to 1
    
    //if(abs(rpm) <= 1 && 0 <= acceleration <= 1){
        

        //vel = rpm * (32768 / 8000) * 65536;
        rpm = rpm * 4423680;   // Motor ranged from +- 2,147,483,647
        //rpm = rpm * 32768;
        
        acceleration = int(acceleration * 1000); //Range 0 -> 2147483647
        serial->print("MV ");     //Set to motor velocity mode
        serial->print("VT="+String(rpm)+" ");       //Set the rpm
        serial->print("ADT=" + String(acceleration) + " ");      //Set the acceration/deceleration
        serial->print("G ");      //Go Command
        
        //return true;                //Retrun a true to confirm operation complete
    //}
    //return false;                   //Reteun a false if there is an error
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
  serial->print("EIGN(2) ");  // Clear Limits
  serial->print("EIGN(3) ");  // Clear Limits
  serial->print("ZS ");       // Clear All Warning Tags
  serial->print("SLD ");

  drive();

  statusCheck();
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

void MoogMotor::park(){
  serial->print("BRKSRV ");   // Engage Break When not Moving
  serial->print("G ");        // Go Command to turn on coils
  serial->print("X ");        // Send Stop Request
  
}

int MoogMotor::getData(char command[]){
  serial->print(command);
  if (serial->available()) connected = true;
  else connected = false;
  return int(serial->parseInt());
}

void MoogMotor::updateStatusCode(unsigned int code, bool statusIn){
  if (connected) {
    statusCode = statusCode & ~code;              // Reset the bit
    statusCode = statusCode | (code * statusIn);  // Update to proper status
  }
  else statusCode = 0xffff;  // Set everythong to a fault if disconected
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
  park();
  return statusCode == ACTIVE;
}

