
#include "UDMRTDrivetrain.h"

UDMRTDrivetrain::UDMRTDrivetrain(){}

UDMRTDrivetrain::UDMRTDrivetrain(std::vector<MoogMotor> leftMotors, 
    std::vector<MoogMotor> rightMotors,
    float roverWidth, 
    float tireDiameter, 
    float max_lin_vel, 
    float max_ang_vel){
  UDMRTDrivetrain::numberOfMotors = numberOfMotors;
  UDMRTDrivetrain::roverWidth     = roverWidth;
  UDMRTDrivetrain::tireDiameter   = tireDiameter;
  UDMRTDrivetrain::rightMotors    = rightMotors;
  UDMRTDrivetrain::leftMotors     = leftMotors;
  UDMRTDrivetrain::max_ang_vel    = max_ang_vel;
  UDMRTDrivetrain::max_lin_vel    = max_lin_vel;

  
}

bool UDMRTDrivetrain::drive(float kmPerHour_prec, float degPerSecond_prec, float acceleration){

  float mps = (UDMRTDrivetrain::max_lin_vel*1000)/60/60 * kmPerHour_prec;  //Meters per sec
  float ds = UDMRTDrivetrain::max_ang_vel * -degPerSecond_prec;              //Dergees per sec
  
  float rdw = ((mps + (UDMRTDrivetrain::roverWidth/2) * ds) / (3.14159 * UDMRTDrivetrain::tireDiameter));   // right wheel rotations / sec
  float ldw = ((((UDMRTDrivetrain::roverWidth/2) * ds) - mps) / (3.14159 * UDMRTDrivetrain::tireDiameter));   // left wheel rotations / sec

  bool good = true;

  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].setVelocity(ldw, acceleration);
  }
  
  for (int i = 0; i < UDMRTDrivetrain::rightMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].setVelocity(rdw, acceleration);
  }
  return good;
}

void UDMRTDrivetrain::reset(){
  
  for (int i = 0; i <= UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].resetStatusCodes();
  }
  for (int i = 0; i <= UDMRTDrivetrain::rightMotors.size(); i ++){
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

