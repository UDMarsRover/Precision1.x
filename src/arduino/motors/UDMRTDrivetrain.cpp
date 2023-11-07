
#include "UDMRTDrivetrain.h"


UDMRTDrivetrain::UDMRTDrivetrain(int numberOfMotors, HardwareSerial* serial){

  int delayTime = 500; //in micro seconds
  motor[0] = MoogMotor(0, serial);
  for(int i = 1 ; i <= numberOfMotors; i ++){
    motor[i] = MoogMotor(i, serial);
    String setAddress = "SADDR" + String(i);
    sendCommand(setAddress);
    delay(delayTime);
    sendCommand("ECHO",i);
    delay(delayTime);
    sendCommand("SLEEP",i);
    delay(delayTime);
  }
  sendCommand("WAKE");
  sendCommand("EIGN(2)");
  sendCommand("EIGN(3)");
  sendCommand("ZS");
  sendCommand("SLD");

  setGear(PARK);

}

void UDMRTDrivetrain::setup(int leftMotors[], int rightMotors[]){
  leftMotors = leftMotors;
  rightMotors = rightMotors;
}

bool UDMRTDrivetrain::sendCommand( String command, int addr = 0){
  motor[addr].sendCommand(command);
}

void UDMRTDrivetrain::setGear(int gear){
  if (gear = PARK) motor[0].holdON();       // Send braking command to all motors
  else if (gear = DRIVE) motor[0].enable(); // Send enable commands to all motors
  if (gear = NEUTRAL) motor[0].holdOFF();   // Send breaking-off to all motors
}

bool UDMRTDrivetrain::drive(float kmPerHour, float degPerSecond, float acceleration){

  float mpm = (kmPerHour*1000)/60;  //Meters per minute
  float dm = degPerSecond * 60;         //Dergees per minute
  
  float rdw = ((mpm + (ROVERWIDTH/2) * dm) / WHEELRADIUS);   // right wheel rotations /min
  float ldw = ((mpm - (ROVERWIDTH/2) * dm) / WHEELRADIUS);   // left wheel rotations /min

  float rdc = ((rdw/360) / REVSPERROTATION) * GEARRATIO;    // encode counts/min
  float ldc = ((ldw/360) / REVSPERROTATION) * GEARRATIO;    // encoder counts/min

  bool good = true;

  // Set every left motor to the left speed
  for (int i = 1; i <= sizeof(leftMotors); i ++) good = good && motor[i].setVelocity(ldc, acceleration);
  // Set every right motor to the rigth speed
  for (int i = 1; i <= sizeof(rightMotors); i ++) good = good && motor[i].setVelocity(rdc, acceleration);

  // Return true if executied properly, else return false
  return good;
}

void UDMRTDrivetrain::reset(){
  motor[0].resetStatusCodes();
}

void UDMRTDrivetrain::ESHUTDOWN(){
  motor[0].ESHUTDOWN();
}

int* UDMRTDrivetrain::getStatus(){
  int statuses[sizeof(motor)+1];
  for (int i = 1; i < sizeof(motor); i ++ ){
   statuses[i] = motor[i].getStatusCode();
  }
  return statuses;
}
