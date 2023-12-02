
#include "UDMRTDrivetrain.h"



UDMRTDrivetrain::UDMRTDrivetrain(int numberOfMotors, HardwareSerial* serial, float roverWidth=1.2, float tireDiameter=0.254){

  UDMRTDrivetrain::serial = serial;
  UDMRTDrivetrain::serial->begin(9600);
  UDMRTDrivetrain::numberOfMotors = numberOfMotors;
  UDMRTDrivetrain::roverWidth = roverWidth;
  UDMRTDrivetrain::tireDiameter = tireDiameter;
  
}

void UDMRTDrivetrain::setup(int leftMotors[], int rightMotors[], int gearRatios[]){
  UDMRTDrivetrain::leftMotors = leftMotors;
  UDMRTDrivetrain::rightMotors = rightMotors;
    
  int delayTime = 500; //in ms
  motor[0] = MoogMotor(0, serial, 0);  // Initalize global motor
  motor[1] = MoogMotor(1, serial, gearRatios[0]);  // Initalize Host Motor
  sendCommand("SADDR1");  // Set address of root motor
  sendCommand("ECHO");    // Turn on echo for host
  
  for(int i = 2 ; i <= numberOfMotors; i ++){
    UDMRTDrivetrain::motor[i] = MoogMotor(i, serial, gearRatios[i-1]);
    String setAddress = "SADDR" + String(i);
    sendCommand(setAddress);
    delay(delayTime);

    //Remove Software Limits
    sendCommand("EIGN(2)",i);
    sendCommand("EIGN(3)",i);
    sendCommand("SLD",i);

    // Clear Flags
    sendCommand("ZS",i);

    // Turn on the echo commnad to ensure the motors send commnads down the line
    sendCommand("ECHO",i);
    delay(delayTime);

    // Tell the motor to sleep to ensure it doenst react to the additional setup commands
    sendCommand("SLEEP",i);
    delay(delayTime);
    
  }
  
  sendCommand("WAKE");  // Wake all motors to allow them to recive commands

  setGear(PARK); // Put all the motors in park and wait for commands
  
}

bool UDMRTDrivetrain::sendCommand( String command, int addr = 0){
  char sendAddr = ((uint8_t) addr | 0b10000000);
  serial->print(sendAddr);
  serial->print(command);
  serial->print(" ");

  //motor[addr].sendCommand(command);
}

void UDMRTDrivetrain::setGear(int gear){
  if (gear = PARK) motor[0].holdON();       // Send braking command to all motors
  else if (gear = DRIVE) motor[0].enable(); // Send enable commands to all motors
  if (gear = NEUTRAL) motor[0].holdOFF();   // Send breaking-off to all motors
}

bool UDMRTDrivetrain::drive(float kmPerHour, float degPerSecond, float acceleration){

  float mpm = (kmPerHour*1000)/60;  //Meters per minute
  float dm = degPerSecond * 60;         //Dergees per minute
  
  float rdw = ((mpm + (roverWidth/2) * dm) / (2 * 3.14159 * tireDiameter));   // right wheel rotations /min
  float ldw = ((mpm - (roverWidth/2) * dm) / (2 * 3.14159 * tireDiameter));   // left wheel rotations /min

  bool good = true;

  
  //good = good && motor[0].setVelocity(ldc, acceleration);
  Serial.println(sizeof(motor));

  
  // Set every left motor to the left speed
  for (int i = 0; i <= sizeof(leftMotors); i ++){
    Serial.print(leftMotors[i]);
    Serial.print(" ");
    Serial.println(UDMRTDrivetrain::motor[leftMotors[i]].id);
    good = good && UDMRTDrivetrain::motor[leftMotors[i]].setVelocity(ldw, acceleration);
  }
  
  
  // Set every right motor to the rigth speed
  for (int i = 0; i <= sizeof(rightMotors); i ++){
    //Serial.print(rightMotors[i]);
    //Serial.print(" ");
    //Serial.println(motor[rightMotors[i]].id);
    //good = good && motor[rightMotors[i]].setVelocity(rdw, acceleration);
  }
  
  
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
