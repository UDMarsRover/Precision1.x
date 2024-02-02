#include <Arduino_LSM9DS1.h>

// Debug settings for serial printing.
#define DEBUG 1
#if DEBUG == 1
#define debug(x) Serial.print(x)
#define debugln(x) Serial.println(x)
#else
#define debug(x)
#define debugln(x)
#endif

// Timing variables for Loop
uint32_t LoopTimer;
int LastLoop;

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//1d Kalman filter setup
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
float RateRoll, RatePitch, RateYaw;
float RateCalibrationRoll, RateCalibrationPitch, RateCalibrationYaw;
int RateCalibrationNumber;
float AccX, AccY, AccZ;
float AccX_offset, Accy_offset, AccZ_offset;
float AngleRoll, AnglePitch;
uint32_t last_power_down;
float KalmanAngleRoll = 0, KalmanUncertaintyAngleRoll = 2 * 2;
float KalmanAnglePitch = 0, KalmanUncertaintyAnglePitch = 2 * 2;
float Kalman1DOutput[] = { 0, 0 };
bool startup = true;

void setup() {
  LoopTimer = 0;

  // Initialize Serial
  Serial.begin(9600);
  while (!Serial);
  debugln("Begun");

  // Initialize IMU
  if (!IMU.begin()) {
    debugln("Failed to initialize IMU!");
    while (1);
  }

}

void loop() {
  LastLoop = micros();
  // put your main code here, to run repeatedly:
  // debugln() -- Use this instead of Print-- See lines 2-9

  gyro_signals();
  calculate_orientation();

  debug(KalmanAngleRoll);
  debug(", ");
  debugln(KalmanAnglePitch);
  
  while (micros() - LoopTimer < 4000);
  LoopTimer = micros();
}

void calculate_orientation() {
  RateRoll -= RateCalibrationRoll;
  RatePitch -= RateCalibrationPitch;
  RateYaw -= RateCalibrationYaw;
  kalman_1d(KalmanAngleRoll, KalmanUncertaintyAngleRoll, RateRoll, AngleRoll);
  KalmanAngleRoll = Kalman1DOutput[0];
  KalmanUncertaintyAngleRoll = Kalman1DOutput[1];
  kalman_1d(KalmanAnglePitch, KalmanUncertaintyAnglePitch, RatePitch, AnglePitch);
  KalmanAnglePitch = Kalman1DOutput[0];
  KalmanUncertaintyAnglePitch = Kalman1DOutput[1];
}

//-------------------------------------------------------------------------------------------------------------------------------------
//1D Kalman filter
//inputs: KalmanState, KalmanUncertainty, KalmanInput, KalmanMeasurement => Kalman filter inputs
//outputs: Kalman1DOutput => Gives Kalman filter outputs
//-------------------------------------------------------------------------------------------------------------------------------------
void kalman_1d(float KalmanState, float KalmanUncertainty, float KalmanInput, float KalmanMeasurement) {
  //Don't forget that 0.004 is the time separation (4 ms)
  KalmanState = KalmanState + 0.004 * KalmanInput;
  KalmanUncertainty = KalmanUncertainty + 0.004 * 0.004 * 4 * 4;
  float KalmanGain = KalmanUncertainty * 1 / (1 * KalmanUncertainty + 3 * 3);
  KalmanState = KalmanState + KalmanGain * (KalmanMeasurement - KalmanState);
  KalmanUncertainty = (1 - KalmanGain) * KalmanUncertainty;
  Kalman1DOutput[0] = KalmanState;
  Kalman1DOutput[1] = KalmanUncertainty;
}
//-------------------------------------------------------------------------------------------------------------------------------------
//Get Gyroscope signals
//inputs: AngleRoll, AnglePitch => For integrating
//outputs: AngleRoll, AnglePitch => Integrated
//-------------------------------------------------------------------------------------------------------------------------------------
void gyro_signals(void) {
  if (startup) {delay(10); startup = false;} //Instead of this, implement accelAvailable() and gyroAvailable() to ensure data is collected for continuing, could be done in setup
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(RateRoll, RatePitch, RateYaw); //Provides angular velocity in degrees/sec
    //RateRoll -> gyro x, RatePitch -> gyro y, RateYaw -> gyro z=
  }
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(AccX, AccY, AccZ); //Provides angular velocity in degrees/sec=
  }
  AngleRoll = atan(AccY / sqrt(AccX * AccX + AccZ * AccZ)) * 1 / (3.142 / 180);
  AnglePitch = -atan(AccX / sqrt(AccY * AccY + AccZ * AccZ)) * 1 / (3.142 / 180);

  //if (startup) {delay(1000); startup = false;}
}
