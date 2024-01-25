//#include "HardwareSerial.h"
//#include "SoftwareSerial.h"
#include "UDMRTDrivetrain.h"
#include "MoogMotor.h"
//#include <ros.h>
//#include <ros/time.h>
//#include <std_msgs/String.h>
//#include <std_msgs/Float32.h>
//#include <std_msgs/Int16MultiArray.h>
//#include <diagnostic_msgs/DiagnosticStatus.h>
//#include <geometry_msgs/Twist.h>
//#include <geometry_msgs/Vector3.h>

 
#define ROVERWIDTH 1.2    // In Meters
#define WHEELRADIUS 0.254 // In Meters
#define GEARRATIO 40      // Number of input shaft roations for every output shaft roation
#define RED 22     
#define BLUE 24     
#define GREEN 23
#define LED_PWR 25

//SoftwareSerial ss1 = SoftwareSerial(2,3);
//SoftwareSerial ss2 = SoftwareSerial(4,5);
//SoftwareSerial ss3 = SoftwareSerial(6,7);

int input;
float linearVelocity = 15;  //km/h
float angularVelocity = 10; //deg/sec
float acceleration = 0.25;
float positionM = 0;
boolean goodl = false;
boolean goodr = false;
int numberOfMotors = 3;
int* driveStatus;
int leftMotors[] = {1,2,3};
int mid = 2;
int led = 7;
bool ok = false;
bool warn = false;
bool error = false;
int faultedDrive = 0;

//SoftwareSerial s1(2,3);

UDMRTDrivetrain driveTrain = UDMRTDrivetrain();

/*
std_msgs::Float32 currentDriveGear;
//diagnostic_msgs::DiagnosticStatus currentDriveStatus;
ros::NodeHandle driverNode;
//ros::Publisher DriveGear("DriveGear", &currentDriveGear);
//ros::Publisher DriveError("DriveStatus", &currentDriveStatus);


void runTankDrive(geometry_msgs::Twist command){
  //geometry_msgs::Vector3 linearVel = command.linear;
  //geometry_msgs::Vector3 angularVel = command.angular;
  float kmh = command.linear.x;     // km/h
  float ds = command.angular.x;     // deg/sec
  //currentDriveGear.data = kmh;
  //DriveGear.publish(&currentDriveGear);
  driveTrain.drive(10, 0, 0.25);
  /*
  if(driveTrain.drive(kmh, ds, acceleration)) {
    //driverNode.loginfo("Running Tankd Drive ...");
    currentDriveGear.data = "D";
  } else {
    //driverNode.loginfo("!!! Tank Drive Error !!!");
    currentDriveGear.data = "X";
  }
  
  delay(50);
  
}

/*
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


//ros::Subscriber<std_msgs::String> commandsIn("DriveCommand", &runTankDrive);
//ros::Subscriber sub = driverNode.subscribe("DriveCommand",10, runTankDrive);
ros::Subscriber<geometry_msgs::Twist> velocityIn("DriveVelocity", &runTankDrive);

*/

void setup() {

  pinMode(RED, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(LED_PWR, OUTPUT);
  digitalWrite(BLUE, HIGH);
  digitalWrite(RED, HIGH);
  digitalWrite(GREEN, HIGH);

  Serial.begin(9600); //Start a serial to take in keyboard commands
  while(!Serial);
  digitalWrite(BLUE, LOW);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial1.begin(9600);
  while(!Serial1);
  digitalWrite(BLUE, HIGH);
  digitalWrite(RED, LOW);
  //Serial1.begin(9600);
  //Serial2.begin(9600);
  //Serial3.begin(9600);
  //Serial.println("Serial Ports Started..");
  std::vector<MoogMotor> rightMotors;
  std::vector<MoogMotor> leftMotors;
  Serial.println("Starting Up Motors...");
  leftMotors.push_back(MoogMotor(1,&Serial1,40));
  leftMotors.push_back(MoogMotor(2,&Serial1,40));
  //leftMotors.push_back(MoogMotor(0,&Serial1,40));
  //rightMotors[0] = MoogMotor(0,&Serial2,28);
  //rightMotors[1] = MoogMotor(0,&Serial2,28);
  //rightMotors[2] = MoogMotor(0,&Serial3,40);
  //Serial.println("Motors Started...");

  driveTrain = UDMRTDrivetrain(leftMotors, rightMotors);

  //Serial.println("Drivetrain Started...");
  //driverNode.getHardware()->setBaud(115200);
  //driverNode.initNode();
  
  //driverNode.advertise(DriveGear);
  //driverNode.advertise(DriveError);
  //driverNode.subscribe(commandsIn);
  //driverNode.subscribe(velocityIn);
  
  //pinMode(led,OUTPUT);
  //currentDriveStatus.name = "Drivetrain Software";
  //currentDriveStatus.message = "Drivetrain Motors Status";
  //currentDriveStatus.hardware_id = "Arduino Mega - Drivetrain";

  delay(1000);
  Serial.println("Motor Setup Complete");

}

void loop() {
  //delay(1000); // To Avoid improper startup
  
  //driverNode.spinOnce();
  driveTrain.drive(5, 0, 0.25);
  digitalWrite(BLUE, HIGH);
  digitalWrite(RED, HIGH);
  digitalWrite(GREEN, LOW);

  Serial.println("Driving");
  Serial1.print("ZS ");
  /*
  //driveStatus = *driveTrain.getStatus();
  faultedDrive = 0;
  error = false;
  warn = false;
  ok = false;

  
  //driveTrain.drive(8, 0, acceleration);
  //Serial.println("Trying to Drive...");
  //rightDrive.setVelocity(10, 100);

  
  
  //Serial.println("Hi Start");
  
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
  */
  
  
  delay(1000);

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