#include "HardwareSerial.h"
#include "MoogMotor.h"
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/String.h>


int input;
float velocity = 1;
float acceleration = 1;
float positionM = 0;
boolean goodl = false;
boolean goodr = false;
float motor1, motor2, motor3, motor4 = 0;

MoogMotor leftDrive = MoogMotor(&Serial2); //Comms for left drive
MoogMotor rightDrive = MoogMotor(&Serial1); //Comms for right drive

ros::NodeHandle driverNode;
std_msgs::String str_msg;
ros::Publisher errors("DriverToPi", &str_msg);
ros::Subscriber<std_msgs::String> sub("PiToDriver", &messageCb );

void setup() {

  //Serial.begin(9600); //Start a serial to take in keyboard commands
  driverNode.initNode();
  driverNode.advertise(chatter);
  leftDrive.setUp();
  rightDrive.setUp();

}

void messageCb(const std_msgs::String& dataIn){
    digitalWrite(13, HIGH-digitalRead(13));   // blink the led
    commands = dataIn.data;

    motor1 = int(commands[0:2])/100;
    motor2 = int(commands[3:5])/100;
    motor3 = int(commands[6:8])/100;
    motor4 = int(commands[9:11])/100;
}




void loop() {

    goodl = leftDrive.setVelocity(motor1, acceleration);
    goodr = rightDrive.setVelocity(motor3, acceleration);

    str_msg.data = "FF";
    errors.publish( &str_msg );
    driverNode.spinOnce();
    delay(1000);

    /*
  if(Serial.available()){
    
    input = Serial.read(); //Check for an input
    
    if(input == 'w'){
      goodl = leftDrive.setVelocity(velocity, acceleration);
      goodr = rightDrive.setVelocity(velocity, acceleration);

      if(goodl && goodr){
        Serial.println("Running Forward");
        positionM = positionM + 0.1;
        }
      
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
      Serial.println("Stopped");
    }

    else if (input == 'q'){
      leftDrive.setUp();
      rightDrive.setUp();
      Serial.println("Startup...");
    }

    else if (input == 'p'){
      leftDrive.off();
      rightDrive.off();
      Serial.println("Shutdown..");
    }
    
  }

  */
}
