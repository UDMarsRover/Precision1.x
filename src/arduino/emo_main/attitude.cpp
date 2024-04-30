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

Quaternion * Attitude::getQrt() {
  if (!dmpReady) return &q;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    //qrt[0] = q.w;
    //qrt[1] = q.x;
    //qrt[2] = q.y;
    //qrt[3] = q.z;
    return &q;
  }
}

float * Attitude::getYpr() {
  if (!dmpReady) return NULL;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&aaWorld, &aa, &q);
    mpu.dmpGetGyro(&gg, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&ggWorld, &gg, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
    ypr[0] = ypr[0] * (RAD_TO_DEG);
    ypr[1] = ypr[1] * (RAD_TO_DEG);
    ypr[2] = ypr[2] * (RAD_TO_DEG);
    return ypr;

  }
}

float * Attitude::getAcc() {
  if (!dmpReady) return NULL;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&aaWorld, &aa, &q);
    acc[0] = aaWorld.x * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    acc[1] = aaWorld.y * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    acc[2] = aaWorld.z * mpu.get_acce_resolution() * EARTH_GRAVITY_MS2;
    return acc;
  }
}

float * Attitude::getGyr() {
  if (!dmpReady) return NULL;
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 
    mpu.dmpGetGyro(&gg, fifoBuffer);
    mpu.dmpConvertToWorldFrame(&ggWorld, &gg, &q);
    gyr[0] = aaWorld.x * mpu.get_gyro_resolution() * DEG_TO_RAD;
    gyr[1] = aaWorld.y * mpu.get_gyro_resolution() * DEG_TO_RAD;
    gyr[2] = aaWorld.z * mpu.get_gyro_resolution() * DEG_TO_RAD;
    return gyr;
  }
}