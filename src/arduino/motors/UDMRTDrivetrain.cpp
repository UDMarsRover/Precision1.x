
#include "UDMRTDrivetrain.h"

UDMRTDrivetrain::UDMRTDrivetrain(){}

UDMRTDrivetrain::UDMRTDrivetrain(std::vector<MoogMotor> leftMotors, std::vector<MoogMotor> rightMotors,float roverWidth, float tireDiameter){
  UDMRTDrivetrain::numberOfMotors = numberOfMotors;
  UDMRTDrivetrain::roverWidth     = roverWidth;
  UDMRTDrivetrain::tireDiameter   = tireDiameter;
  UDMRTDrivetrain::rightMotors    = rightMotors;
  UDMRTDrivetrain::leftMotors     = leftMotors;

  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    Serial.println(UDMRTDrivetrain::leftMotors[i].setID());
    UDMRTDrivetrain::leftMotors[i].sendCommand("SLEEP");
  }

    for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].sendCommand("WAKE",true);
  }
  
}

/*
bool UDMRTDrivetrain::sendCommand( String command, int addr = 0){
  motor[addr].sendCommand(command);
}


void UDMRTDrivetrain::setGear(int gear){
  if (gear = PARK) motor[0].holdON();       // Send braking command to all motors
  else if (gear = DRIVE) motor[0].enable(); // Send enable commands to all motors
  if (gear = NEUTRAL) motor[0].holdOFF();   // Send breaking-off to all motors
}

*/
bool UDMRTDrivetrain::drive(float kmPerHour, float degPerSecond, float acceleration){

  float mps = (kmPerHour*1000)/60/60;  //Meters per sec
  float ds = degPerSecond;        //Dergees per sec
  
  float rdw = ((mps + (UDMRTDrivetrain::roverWidth/2) * ds) / (3.14159 * UDMRTDrivetrain::tireDiameter));   // right wheel rotations / sec
  float ldw = ((((UDMRTDrivetrain::roverWidth/2) * ds) - mps) / (3.14159 * UDMRTDrivetrain::tireDiameter));   // left wheel rotations / sec

  bool good = true;

  
  //good = good && motor[0].setVelocity(ldc, acceleration);

  //UDMRTDrivetrain::motor[2].setVelocity(ldw, acceleration);
  //UDMRTDrivetrain::motor[3].setVelocity(ldw, acceleration);
  //UDMRTDrivetrain::motor[4].setVelocity(ldw, acceleration);
  // Set every left motor to the left speed

  UDMRTDrivetrain::leftMotors[1].setVelocity(ldw, acceleration);

  /*
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].setVelocity(ldw, acceleration);
    
  }
  */
  
  /*
  // Set every right motor to the rigth speed
  UDMRTDrivetrain::rightMotors[0].setVelocity(rdw, acceleration);
  UDMRTDrivetrain::rightMotors[1].setVelocity(rdw, acceleration);
  UDMRTDrivetrain::rightMotors[2].setVelocity(rdw, acceleration);
  */
  
  /*
  for (int j = 0; j <= sizeof(UDMRTDrivetrain::rightMotors); j ++){
    UDMRTDrivetrain::rightMotors[j].setVelocity(rdw, acceleration);
    //Serial.print(rightMotors[i]);
    //Serial.print(" ");
    //Serial.println(motor[rightMotors[i]].id);
    //good = good && motor[rightMotors[i]].setVelocity(0, acceleration);
  }
  */
  
  // Return true if executied properly, else return false
  return good;
}

void UDMRTDrivetrain::reset(){
  
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].resetStatusCodes();
  }
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].resetStatusCodes();
  }

}

void UDMRTDrivetrain::ESTOP(){
  
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].ESTOP();
  }
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].ESTOP();
  }
  
}

