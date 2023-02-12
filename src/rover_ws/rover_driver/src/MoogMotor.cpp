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
  //initSerial();
}

boolean MoogMotor::setVelocity(float rpm, float acceleration){
    // RPM Can only be from -1 to 1
    
    if(abs(rpm) <= 1 && 0 <= acceleration <= 1){
        
        rpm = int(rpm * 214783647.0);   // Motor ranged from +- 2147483647
        
        acceleration = int(acceleration * 32767); //Range 0 -> 2147483647
        
        
        serial->print("MV\r");     //Set to motor velocity mode
        serial->print("VT=");       //Set the rpm
        serial->print(rpm);
        serial->print("\r");
        serial->print("ADT=");      //Set the acceration/deceleration
        serial->print(acceleration);
        serial->print("\r");
        
        
        serial->print("G\r");      //Go Command
        delay(1);
        return true;                //Retrun a true to confirm operation complete
    }
    return false;                   //Reteun a false if there is an error
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
        value = int(value * 2147483647.0);   // Motor ranged from +- 2147483647
        acceleration = int(acceleration * 2147483647.0); //Range 0 -> 2147483647
        
        
        serial->print("MP\r");     //Set to motor position mode
        serial->print("VT=");       //Set the rpm
        serial->print(velocity);
        serial->print("\r");
        serial->print("ADT=");      //Set the acceration/deceleration
        serial->print(acceleration);
        serial->print("\r");
        serial->print("PT=");
        serial->print(value);       //Set the position
        serial->print("\r");
        
        serial->print("G\r");      //Go Command
        delay(1);
        return true;                //Retrun a true to confirm operation complete
    }
    return false;
}

void MoogMotor::ESTOP()
{
  serial->print("S \r"); //EStop command
}

void MoogMotor::stop()
{
  serial->print("X \r"); //Standard stop command
}

void MoogMotor::setUp()
{
      serial->begin(9600);
      //serial->print("MDE \r");
      delay(200);
      serial->print("EIGN(2) \r");
      delay(200);
      serial->print("EIGN(3) \r");
      delay(200);
      serial->print("ZS \r");
      delay(200);
    
      serial->print("O=0");          //Set the current position to zero
}

void MoogMotor::off(){
    serial->print("OFF");               //Turn the servo off (with breaking)
    serial->print("\r");
    
    serial->print("ZS \r BRKRLS \r");   //Clear errors and release break
}
