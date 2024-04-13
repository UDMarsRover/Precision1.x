
#include "UDMRTDrivetrain.h"

UDMRTDrivetrain::UDMRTDrivetrain(){}

UDMRTDrivetrain::UDMRTDrivetrain(std::vector<MoogMotor> leftMotors, 
                                 std::vector<MoogMotor> rightMotors,
                                 const std::vector<float> lengths,
                                 float max_length, 
                                 float max_lin_vel)
{

  UDMRTDrivetrain::numberOfMotors = numberOfMotors;
  UDMRTDrivetrain::roverWidth     = roverWidth;
  UDMRTDrivetrain::tireDiameter   = tireDiameter;
  UDMRTDrivetrain::rightMotors    = rightMotors;
  UDMRTDrivetrain::leftMotors     = leftMotors;
  
  UDMRTDrivetrain::max_lin_vel    = max_lin_vel;
  UDMRTDrivetrain::max_ang_vel    = 10;
  //UDMRTDrivetrain::max_lin_vel/(max_length * 60 * 60);
  UDMRTDrivetrain::lengths        = lengths;
}

bool UDMRTDrivetrain::drive(float kmPerHour_prec, float degPerSecond_prec, float acceleration){


  float kmph = UDMRTDrivetrain::max_lin_vel * kmPerHour_prec;  //kmph

  float radph = (UDMRTDrivetrain::max_ang_vel * degPerSecond_prec) * 60 * 60 * 0.0174533; //Rad per hour

  bool good = true;

  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){

    UDMRTDrivetrain::leftMotors[i].setVelocity((radph * UDMRTDrivetrain::lengths[i]) - kmph);
    digitalWrite(24, LOW);
    digitalWrite(22, LOW);
    digitalWrite(23, HIGH);
  }
  
  for (int i = 0; i < UDMRTDrivetrain::rightMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].setVelocity(kmph + (radph * UDMRTDrivetrain::lengths[i]));
  }
  return good;
}

void UDMRTDrivetrain::reset(){
  for (int i = 0; i < UDMRTDrivetrain::leftMotors.size(); i ++){
    UDMRTDrivetrain::leftMotors[i].resetStatusCodes();
  }
  delay(100);
  for (int i = 0; i < UDMRTDrivetrain::rightMotors.size(); i ++){
    UDMRTDrivetrain::rightMotors[i].resetStatusCodes();
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

