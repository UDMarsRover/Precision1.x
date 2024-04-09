
#include "UDMRTDrivetrain.h"

UDMRTDrivetrain::UDMRTDrivetrain(){}

UDMRTDrivetrain::UDMRTDrivetrain(std::vector<MoogMotor>* leftMotors, 
                                 std::vector<MoogMotor>* rightMotors,
                                 const std::vector<float>* length,
                                 float max_length, 
                                 float max_ang_vel)
{

  UDMRTDrivetrain::numberOfMotors = numberOfMotors;
  UDMRTDrivetrain::roverWidth     = roverWidth;
  UDMRTDrivetrain::tireDiameter   = tireDiameter;
  UDMRTDrivetrain::rightMotors    = rightMotors;
  UDMRTDrivetrain::leftMotors     = leftMotors;
  
  UDMRTDrivetrain::max_lin_vel    = max_lin_vel;
  UDMRTDrivetrain::max_ang_vel    = UDMRTDrivetrain::max_lin_vel/max_length;
  UDMRTDrivetrain::lengths        = lengths;
}

bool UDMRTDrivetrain::drive(float kmPerHour_prec, float degPerSecond_prec, float acceleration){

  float mps = UDMRTDrivetrain::max_lin_vel * kmPerHour_prec;  //kmph
  float ds = UDMRTDrivetrain::max_ang_vel * degPerSecond_prec; //Dergees per sec

  bool good = true;

  for (int i = 0; i < UDMRTDrivetrain::leftMotors->size(); i ++){
    UDMRTDrivetrain::leftMotors->at(i).setVelocity(mps + (ds * UDMRTDrivetrain::lengths->at(i)));
  }
  
  for (int i = 0; i < UDMRTDrivetrain::rightMotors->size(); i ++){
    UDMRTDrivetrain::rightMotors->at(i).setVelocity(-1 * (mps + (ds * UDMRTDrivetrain::lengths->at(i))));
  }
  return good;
}

void UDMRTDrivetrain::reset(){
  
  for (int i = 0; i <= UDMRTDrivetrain::leftMotors->size(); i ++){
    UDMRTDrivetrain::rightMotors->at(i).resetStatusCodes();
  }
  for (int i = 0; i <= UDMRTDrivetrain::rightMotors->size(); i ++){
    UDMRTDrivetrain::leftMotors->at(i).resetStatusCodes();
  }

}

void UDMRTDrivetrain::ESTOP(){
  
  for (int i = 0; i < UDMRTDrivetrain::leftMotors->size(); i ++){
    UDMRTDrivetrain::rightMotors->at(i).ESTOP();
  }
  for (int i = 0; i < UDMRTDrivetrain::leftMotors->size(); i ++){
    UDMRTDrivetrain::leftMotors->at(i).ESTOP();
  }
  
}

