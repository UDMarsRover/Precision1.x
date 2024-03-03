#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <NewPing.h>


// trigger and echo pins for each sensor
#define TRIG1 2
#define ECHO1 3

#define TRIG2 4
#define ECHO2 5

#define TRIG3 6
#define ECHO3 7

#define TRIG4 8
#define ECHO4 9

#define MAX_DISTANCE 100 // maximum distance for sensors in cm
#define NUM_SONAR 4 // number of ultrasonic sensors

NewPing sonar[NUM_SONAR] = { // array of ultrasonic pings
  NewPing(TRIG1, ECHO1, MAX_DISTANCE),
  NewPing(TRIG2, ECHO2, MAX_DISTANCE),
  NewPing(TRIG3, ECHO3, MAX_DISTANCE),
  NewPing(TRIG4, ECHO4, MAX_DISTANCE)
};

double curDuration[NUM_SONAR]; // array for pings in microseconds
double prevDistance[NUM_SONAR]; // arrays for pings
double curDistance[NUM_SONAR];// in cm

// arrays to store distance output as string
String curDistanceCM[NUM_SONAR];
String curDistanceOutput[NUM_SONAR];

// ros node, message, and publisher setup
ros::NodeHandle nh;
float ultraArray[4]; // initialize array to assign to msg
std_msgs::Float32MultiArray msg;
ros::Publisher pub("ultrasonic_pub", &msg);

void setup() {
  // node and publisher setup
  nh.initNode();
  nh.advertise(pub);
  msg.data_length = 4; // initialize length of msg array
}

void loop() {
  updateSonar(); // update the distance array
 
  pub.publish(&msg); // publish the array of distance values
  nh.spinOnce();
}

// takes a new reading from each sensor and updates the
// distance array
void updateSonar() {
  for (int i = 0; i < NUM_SONAR; i++) {
    curDuration[i] = sonar[i].ping(); // ping distance in microseconds
    // sonar sensors return 0 if no obstacle is detected

    curDistance[i] = (curDuration[i] * 0.034) / 2; // convert microseconds to cm

    // if no object is detected set current distance to previous 
    if (curDistance[i] == 0){
      curDistanceOutput[i] = prevDistance[i];
    }
    else{
      curDistance[i] = expFilter(0.1, prevDistance[i], curDistance[i]); // filter distance values
      curDistanceCM[i] = String(curDistance[i]); // convert distance in cm to string
      curDistanceOutput[i] = curDistanceCM[i].substring(0,curDistanceCM[i].length()-1); // concatanate cm with decimal mm
    }  

    ultraArray[i] = curDistanceOutput[i].toFloat(); // convert output to float and assign to
    prevDistance[i] = curDistance[i]; // set previous distance to current 

  }
  
  msg.data = ultraArray; // update msg with curent array of values
}

// method for filtering distance values
double expFilter(double alpha, double prevReading, double curReading){
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}