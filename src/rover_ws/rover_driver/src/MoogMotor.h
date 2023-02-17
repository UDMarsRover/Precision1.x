/*
 * MoogMotor.h - Library for controlling Moog Smart Motors via HardwareSerial.
 * Created by Joe Ditz on Jan 27, 2021
 * Edited by Greg Molskow on Mar 27, 2021
 */

 #ifndef MoogMotor_h
 #define MoogMotor_h

 #include "Arduino.h"
 #include "HardwareSerial.h"

 class MoogMotor
 {
  public:
    enum MotorMode {POS, VEL, TOR};

     MoogMotor(HardwareSerial* associatedSerial);
    //boolean driveMotor(MotorMode operationMode, float value);
     boolean setVelocity(float rpm, float acceleration);
     boolean setTorque(float torque);
     boolean setPosition(float value,float velocity, float acceleration);
     
     void ESTOP();
     void stop();
     void setUp();
     void off();

  private:
    HardwareSerial *serial = NULL;
    MotorMode mode = POS;

    
  
 };

#endif
