#include "HardwareSerial.h"
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

int led = 7;

float roverWidth  = 1;   //meters
float wheelRad    = 0.032;  //meters
float gearRatio   = 40;
float revsperrotate = 4000;

MoogMotor leftDrive = MoogMotor(&Serial2); //Comms for left drive
MoogMotor rightDrive = MoogMotor(&Serial1); //Comms for right drive

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

  goodr = rightDrive.setVelocity(rdc, acceleration);
  goodl = leftDrive.setVelocity(-ldc, acceleration);
  if(goodl && goodr){currentDriveGear.data = "D";}

}

void keyboard_teleop_ros(std_msgs::String msg){
  String input = msg.data;
  digitalWrite(led,HIGH);
  if(input == "w"){
    goodl = leftDrive.setVelocity(velocity, acceleration);
    goodr = rightDrive.setVelocity(velocity, acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Forward");}
    
  }

  else if (input == "s"){
    goodl = leftDrive.setVelocity(-velocity,acceleration);
    goodr = rightDrive.setVelocity(-velocity,acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Backwards");}
    currentDriveGear.data = "N";
  }

  else if (input == "d"){
    goodl = leftDrive.setVelocity(-velocity,acceleration);
    goodr = rightDrive.setVelocity(velocity,acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Left");}
    currentDriveGear.data = "D";
  }

  else if (input == "a"){
    goodl = leftDrive.setVelocity(velocity,acceleration);
    goodr = rightDrive.setVelocity(-velocity,acceleration);
    if(goodl && goodr){driverNode.loginfo("Running Right");}
    currentDriveGear.data = "D";
  }

  else if(input == "e"){
    leftDrive.stop();
    rightDrive.stop();
    driverNode.loginfo("Stopping...");
  }

  else if (input == "q"){
    leftDrive.setUp();
    rightDrive.setUp();
    driverNode.loginfo("Startup...");
  }

  else if (input == "p"){
    leftDrive.park();
    rightDrive.park();
    driverNode.loginfo("Break Engaged..");
    currentDriveGear.data = "P";
  }

  else if (input == "x"){
    leftDrive.ESHUTDOWN();
    rightDrive.ESHUTDOWN();
    driverNode.loginfo("ESHUTDOWN..");
  }

  else if (input == "n"){
    leftDrive.neutral();
    rightDrive.neutral();
    driverNode.loginfo("In Nutural...");
    currentDriveGear.data = "N";
    
  }

  else if (input == "r"){
    leftDrive.resetStatusCodes();
    rightDrive.resetStatusCodes();
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
  leftDrive.setUp();
  rightDrive.setUp();
  pinMode(led,OUTPUT);

}

/*
void messageCb(const std_msgs::String& dataIn){
    digitalWrite(13, HIGH-digitalRead(13));   // blink the led
    commands = dataIn.data;

    motor1 = int(commands[0:2])/100;
    motor2 = int(commands[3:5])/100;
    motor3 = int(commands[6:8])/100;
    motor4 = int(commands[9:11])/100;
}
*/


/******************************************/
/*                  Notes
/ - If you want to switch between forward 
/   and backward, call stop in between
/   velocity calls!!!! otherwise an error
/   will be thrown and the motor will stop.
/   This is by design of the manufacturer.
/******************************************/




void loop() {
  driverNode.spinOnce();
  rightDrive.statusCheck();
  leftDrive.statusCheck();
  sprintf(rightDriveError,"%x",rightDrive.getStatusCode());
  sprintf(leftDriveError,"%x",leftDrive.getStatusCode());
  sprintf(driveError,"0%-4s0%-4s",leftDriveError,rightDriveError);
  currentDriveError.data = driveError;
  DriveError.publish(&currentDriveError);

  delay(100);

}






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
