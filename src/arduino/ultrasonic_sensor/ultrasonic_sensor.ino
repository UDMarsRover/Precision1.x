// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#define echoPin 3 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 2 //attach pin D3 Arduino to pin Trig of HC-SR04

// defines variables
long duration; // variable for the duration of sound wave travel
long curDuration;
//long distance; // variable for the distance measurement
String distance;
String longDistance;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");
}
void loop() {
  longDistance = "";
  // Clears the trigPin condition
  for (int i = 0; i < 4; i++) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  curDuration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  curDuration = ( curDuration * 0.034 ) / 2; // Speed of sound wave divided by 2 (go and back)
  curDuration = expFilter(0.3, duration, curDuration);
  // Displays the distance on the Serial Monitor
  //distance = (String)duration;
  //distance = stringPadding(4, (String)curDuration);
  if (curDuration > 600) {
    curDuration = duration;
  }
  distance = (String)curDuration;
  longDistance += stringPadding(4, distance);
  if (curDuration < 31) {
    Serial.println("B3");
  }
  else if (curDuration < 62) {
    Serial.println("B2");
  }
  duration = curDuration;
  
  delay(50);
  }
  Serial.println(longDistance);
}


String stringPadding(int requiredDigits, String value) {
  int diff = requiredDigits - value.length();
  while (diff > 0) {
    value = "0" + value;
    diff = diff - 1;
  }
  return value;
}

// test for different sensors
// use this within each method for the sensors
double expFilter(double alpha, double prevReading, double curReading){
  // Serial.println(alpha);
  return (alpha * curReading) + ((1 - alpha) * prevReading);
}
