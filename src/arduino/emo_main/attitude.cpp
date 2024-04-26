// attitude.cpp
#include "attitude.h"

Attitude::Attitude() {

}

void Attitude::initialize() {
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
    Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif

  mpu.initialize();
  devStatus = mpu.dmpInitialize();

  if (devStatus == 0) {

    mpu.CalibrateAccel(7);
    mpu.CalibrateGyro(7);
    mpu.PrintActiveOffsets();
    mpu.setDMPEnabled(true);

    mpuIntStatus = mpu.getIntStatus();

    dmpReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
  }
}

float * Attitude::getYpr() {
  if (!dmpReady) return ypr;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&aaWorld, &aa, &q);
    mpu.dmpGetGyro(&gg, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&ggWorld, &gg, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
    return ypr;

  }
}

float * Attitude::getAcc() {
  if (!dmpReady) return acc;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&aaWorld, &aa, &q);
    acc[0] = aaWorld.x * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    acc[1] = aaWorld.y * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    acc[2] = aaWorld.z * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    return acc;
  }
}