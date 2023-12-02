#include "HardwareSerial.h"
//#include "SoftwareSerial.h"
#include "UDMRTDrivetrain.h"
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16MultiArray.h>
#include <diagnostic_msgs/DiagnosticStatus.h>
#include <geometry_msgs/Accel.h>
 

int input;
float linearVelocity = 15;  //km/h
float angularVelocity = 10; //deg/sec
float acceleration = 0.25;
float positionM = 0;
boolean goodl = false;
boolean goodr = false;
int numberOfMotors = 6;
int* driveStatus;
int rightMotors[] = {4,5,6};
int leftMotors[] = {1,2,3};
int mid = 2;
int led = 7;
bool ok = false;
bool warn = false;
bool error = false;
int faultedDrive = 0;

UDMRTDrivetrain driveTrain = UDMRTDrivetrain(numberOfMotors, &Serial1);

std_msgs::String currentDriveGear;
diagnostic_msgs::DiagnosticStatus currentDriveStatus;
//ros::NodeHandle driverNode;
//ros::Publisher DriveGear("DriveGear", &currentDriveGear);
//ros::Publisher DriveError("DriveStatus", &currentDriveStatus);

/*
void runTankDrive(geometry_msgs::Accel command){
  float kmh = command.linear.x;     // km/h
  float ds = command.angular.x;     // deg/sec
  if(driveTrain.drive(kmh, ds, acceleration)) {
    //driverNode.loginfo("Running Tankd Drive ...");
    //currentDriveGear.data = "D";
  } else {
    //driverNode.loginfo("!!! Tank Drive Error !!!");
    currentDriveGear.data = "X";
  }
  
}

void keyboard_teleop_ros(std_msgs::String msg){
  String input = msg.data;
  digitalWrite(led,HIGH);
  if(input == "w"){
    if(driveTrain.drive(linearVelocity, 0, acceleration)) {
      //driverNode.loginfo("Running Forward...");
      currentDriveGear.data = "D";
    } else {
      //driverNode.loginfo("!!! Forward Drive Error !!!");
      currentDriveGear.data = "X";
    }
  }

  else if (input == "s"){
    if(driveTrain.drive(-linearVelocity, 0, acceleration)) {
      //driverNode.loginfo("Running In Reverse...");
      currentDriveGear.data = "D";
    } else {
      //driverNode.loginfo("!!! Reverse Drive Error !!!");
      currentDriveGear.data = "X";
    }
  }

  else if (input == "d"){
    if(driveTrain.drive(0, angularVelocity, acceleration)) {
      //driverNode.loginfo("Turning Right...");
      currentDriveGear.data = "D";
    } else {
      //driverNode.loginfo("!!! Right Drive Error !!!");
      currentDriveGear.data = "X";
    }
  }

  else if (input == "a"){
    if(driveTrain.drive(0, -angularVelocity, acceleration)) {
      //driverNode.loginfo("Turning Left...");
      currentDriveGear.data = "D";
    } else {
      //driverNode.loginfo("!!! Left Drive Error !!!");
      currentDriveGear.data = "X";
    }
  }

  else if(input == "e"){
    if(driveTrain.drive(0, 0, acceleration)) {
      //driverNode.loginfo("Stopping...");
      currentDriveGear.data = "D";
    } else {
      //driverNode.loginfo("!!! Stop Drive Error !!!");
      currentDriveGear.data = "X";
    }
  }

  else if (input == "q"){
    driveTrain.setup(leftMotors, rightMotors);
    //driverNode.loginfo("Startup...");
  }

  else if (input == "p"){
    driveTrain.setGear(PARK);
    //driverNode.loginfo("Break Engaged..");
    currentDriveGear.data = "P";
  }

  else if (input == "x"){
    driveTrain.ESHUTDOWN();
    //driverNode.loginfo("ESHUTDOWN..");
  }

  else if (input == "n"){
    driveTrain.setGear(NEUTRAL);
    //driverNode.loginfo("In Nutural...");
    currentDriveGear.data = "N";
    
  }

  else if (input == "r"){
    driveTrain.reset();
    //driverNode.loginfo("Reseting Tags");
  }
  
  //DriveGear.publish(&currentDriveGear);
  
  digitalWrite(led,LOW);
}

ros::Subscriber<std_msgs::String> commandsIn("DriveCommand", &keyboard_teleop_ros);
ros::Subscriber<geometry_msgs::Accel> velocityIn("DriveVelocity", &runTankDrive);

*/
void setup() {

  Serial.begin(9600); //Start a serial to take in keyboard commands

  delay(100);
  Serial.println("Hi Setup 1");

  //driverNode.initNode();
  //driverNode.advertise(DriveGear);
  //driverNode.advertise(DriveError);
  //driverNode.subscribe(commandsIn);
  //driverNode.subscribe(velocityIn);
  
  pinMode(led,OUTPUT);
  currentDriveStatus.name = "Drivetrain Software";
  currentDriveStatus.message = "Drivetrain Motors Status";
  currentDriveStatus.hardware_id = "Arduino Mega - Drivetrain";

  driveTrain.setup(leftMotors, rightMotors);

}

void loop() {
  //driverNode.spinOnce();

  //driveStatus = *driveTrain.getStatus();
  //fautedDrive = 0;
  error = false;
  warn = false;
  ok = false;

  Serial.print(driveTrain.drive(50000000, 0, acceleration));
  Serial.println("Hi Start");

  for (int i = 1; i <= sizeof(driveStatus); i ++) {

    error  = (0 == (driveStatus && errorSTAT));
    if (!error) warn  = (0 == (driveStatus && warnSTAT));
    else if (!warn) ok = (0 == (driveStatus && okSTAT));
    if (!ok) {
      faultedDrive = i;
      break;
    }
  }



  if (faultedDrive > 0){
    if (error) currentDriveStatus.level = 2;
    else if (warn) currentDriveStatus.level = 1;
    else if (ok) currentDriveStatus.level = 0;

  } else{
    currentDriveStatus.level = 0;
  }

  //DriveError.publish(&currentDriveStatus);

  delay(50);

}





/*
void keyboard_teleop_dev(){
  if(Serial.available()){
    
    input = Serial.read(); //Get Command
    if(input == 'w'){
      goodl = leftDrive.setVelocity(velocity, acceleration);
      goodr = rightDrive.setVelocity(velocity, acceleration);
      if(goodl && goodr){Serial.println("Running Forward");}
      
    }

    else if (input == 's'){
      goodl = leftDrive.setVelocity(-velocity,acceleration);
      goodr = rightDrive.setVelocity(-velocity,acceleration);
      if(goodl && goodr){Serial.println("Running Backwards");}
    }

    else if (input == 'd'){
      goodl = leftDrive.setVelocity(-velocity,acceleration);
      goodr = rightDrive.setVelocity(velocity,acceleration);
      if(goodl && goodr){Serial.println("Running Backwards");}
    }

    else if (input == 'a'){
      goodl = leftDrive.setVelocity(velocity,acceleration);
      goodr = rightDrive.setVelocity(-velocity,acceleration);
      if(goodl && goodr){Serial.println("Running Backwards");}
    }

    else if(input == 'e'){
      leftDrive.stop();
      rightDrive.stop();
      Serial.println("Stopping...");
    }

    else if (input == 'q'){
      leftDrive.setUp();
      rightDrive.setUp();
      Serial.println("Startup...");
    }

    else if (input == 'p'){
      leftDrive.park();
      rightDrive.park();
      Serial.println("Break Engaged..");
    }

    else if (input == 'x'){
      leftDrive.ESHUTDOWN();
      rightDrive.ESHUTDOWN();
      Serial.println("ESHUTDOWN..");
    }

    else if (input == 'n'){
      leftDrive.neutral();
      rightDrive.neutral();
      Serial.println("In Nutural...");
    }

    else if (input == 'r'){
      leftDrive.resetStatusCodes();
      rightDrive.resetStatusCodes();
      Serial.println("Reseting Tags");
    }
    
  }
}
*/