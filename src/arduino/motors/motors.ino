#include "HardwareSerial.h"
#include "SoftwareSerial.h"
#include "MoogMotor.h"
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Accel.h>
 

int input;
float velocity = 0.9;
float acceleration = 0.25;
float positionM = 0;
boolean goodl = false;
boolean goodr = false;
char rightDriveError[4];
char leftDriveError[4];
char driveError[8];

int mid = 2;

int led = 7;
int motorRX[] = {2,4,6,8};
int motorTX[] = {3,5,7,9};

float roverWidth  = 1;   //meters
float wheelRad    = 0.032;  //meters
float gearRatio   = 40;
float revsperrotate = 4000;


//SoftwareSerial leftDrive1Serial (motorRX[0],motorTX[0]);
//SoftwareSerial leftDrive2Serial (motorRX[1],motorTX[1]);
//SoftwareSerial rightDrive1Serial (motorRX[2],motorTX[2]);
SoftwareSerial rightDrive2Serial (motorRX[0],motorTX[0]);


MoogMotor L1Drive = MoogMotor(&Serial1); //Comms for left drive
//MoogMotor R1Drive = MoogMotor(&Serial2); //Comms for right drive
//MoogMotor L2Drive = MoogMotor(&Serial3); //Comms for left drive
//MoogMotor R2Drive = MoogMotor(&rightDrive2Serial); //Comms for right drive

std_msgs::String currentDriveGear;
std_msgs::String currentDriveError;
ros::NodeHandle driverNode;
ros::Publisher DriveGear("DriveGear", &currentDriveGear);
ros::Publisher DriveError("DriveError", &currentDriveError);

void runTankDrive(geometry_msgs::Accel command){
  float kmh = command.linear.x;     // km/h
  float ds = command.angular.x;     // deg/sec

  float mpm = (kmh*1000)/60;
  float dm = ds * 60;
  
  float rdw = ((mpm + (roverWidth/2) * dm) / wheelRad);   // deg/min
  float ldw = ((mpm - (roverWidth/2) * dm) / wheelRad);   // deg/min

  float rdc = ((rdw/360) / revsperrotate) * gearRatio;    //counts/min
  float ldc = ((ldw/360) / revsperrotate) * gearRatio;    //counts/min

  //goodr = R1Drive.setVelocity(rdc, acceleration);
  goodl = L1Drive.setVelocity(mid,-ldc, acceleration);
  //goodr = goodr & R2Drive.setVelocity(rdc, acceleration);
  //goodl = goodl & L2Drive.setVelocity(-ldc, acceleration);
  if(goodl && goodr){currentDriveGear.data = "D";}

}

void keyboard_teleop_ros(std_msgs::String msg){
  String input = msg.data;
  digitalWrite(led,HIGH);
  if(input == "w"){
    goodl = L1Drive.setVelocity(mid,-velocity, acceleration);
    //goodr = R1Drive.setVelocity(velocity, acceleration);
    //goodl = goodl & L1Drive.setVelocity(-velocity, acceleration);
    //goodr = goodr & R1Drive.setVelocity(velocity, acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Forward");}
    
  }

  else if (input == "s"){
    goodl = L1Drive.setVelocity(mid,velocity, acceleration);
    //goodr = R1Drive.setVelocity(-velocity, acceleration);
    //goodl = goodl & L1Drive.setVelocity(velocity, acceleration);
    //goodr = goodr & R1Drive.setVelocity(-velocity, acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Backwards");}
    currentDriveGear.data = "N";
  }

  else if (input == "d"){
    goodl = L1Drive.setVelocity(mid,velocity, acceleration);
   // goodr = R1Drive.setVelocity(velocity, acceleration);
    //goodl = goodl & L1Drive.setVelocity(velocity, acceleration);
    //goodr = goodr & R1Drive.setVelocity(velocity, acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Left");}
    currentDriveGear.data = "D";
  }

  else if (input == "a"){
    goodl = L1Drive.setVelocity(mid,velocity, acceleration);
    //goodr = R1Drive.setVelocity(-velocity, acceleration);
    //goodl = goodl & L1Drive.setVelocity(velocity, acceleration);
    //goodr = goodr & R1Drive.setVelocity(-velocity, acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Right");}
    currentDriveGear.data = "D";
  }

  else if(input == "e"){
    L1Drive.stop();
    //R1Drive.stop();
    //L2Drive.stop();
    //R2Drive.stop();
    driverNode.loginfo("Stopping...");
  }

  else if (input == "q"){
    L1Drive.setUp();
    //R1Drive.setUp();
    //L2Drive.setUp();
    //R2Drive.setUp();
    driverNode.loginfo("Startup...");
  }

  else if (input == "p"){
    //L1Drive.park();
    //R1Drive.park();
    //L2Drive.park();
    //R2Drive.park();
    driverNode.loginfo("Break Engaged..");
    currentDriveGear.data = "P";
  }

  else if (input == "x"){
    L1Drive.ESHUTDOWN();
    //R1Drive.ESHUTDOWN();
    //L2Drive.ESHUTDOWN();
    //R2Drive.ESHUTDOWN();
    driverNode.loginfo("ESHUTDOWN..");
  }

  else if (input == "n"){
    L1Drive.neutral();
    //R1Drive.neutral();
    //L2Drive.neutral();
    //R2Drive.neutral();
    driverNode.loginfo("In Nutural...");
    currentDriveGear.data = "N";
    
  }

  else if (input == "r"){
    L1Drive.resetStatusCodes();
    //R1Drive.resetStatusCodes();
    //L2Drive.resetStatusCodes();
    //R2Drive.resetStatusCodes();
    driverNode.loginfo("Reseting Tags");
  }
  
  DriveGear.publish(&currentDriveGear);
  
  digitalWrite(led,LOW);
}



ros::Subscriber<std_msgs::String> commandsIn("DriveCommand", &keyboard_teleop_ros);
ros::Subscriber<geometry_msgs::Accel> velocityIn("DriveVelocity", &runTankDrive);


void setup() {

  //Serial.begin(9600); //Start a serial to take in keyboard commands

  driverNode.initNode();
  driverNode.advertise(DriveGear);
  driverNode.advertise(DriveError);
  driverNode.subscribe(commandsIn);
  driverNode.subscribe(velocityIn);
  L1Drive.setUp();
  //R1Drive.setUp();
  //L2Drive.setUp();
  //R2Drive.setUp();
  pinMode(led,OUTPUT);

}

void loop() {
  driverNode.spinOnce();
  L1Drive.statusCheck();
  //R1Drive.statusCheck();
  //L2Drive.statusCheck();
  //R2Drive.statusCheck();
  sprintf(currentDriveError.data,"%x%x%x%x",L1Drive.getStatusCode());
  DriveError.publish(&currentDriveError);

  //delay(50);

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