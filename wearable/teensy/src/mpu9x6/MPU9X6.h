/*
--------------------------------------------------------------------------------
Code for simple Raw information reading from:

    MPU9250 : 9 DOF IMU
    MPU6050 : 6 DOF IMU

Alexander S. Adranly (aadranly@scu.edu)
--------------------------------------------------------------------------------
*/
#include <stdint.h>        // different int types

#ifndef MPU9X6_H
#define MPU9X6_H

// Possible Addresses
#define MPU_ADDR_LO        0x68
#define MPU_ADDR_HI        0x69

// Power Information
#define PWR_MGMT_1         0x6B

// Registers with important information
#define ACCEL_XOUT_H       0x3B
#define ACCEL_XOUT_L       0x3C
#define ACCEL_YOUT_H       0x3D
#define ACCEL_YOUT_L       0x3E
#define ACCEL_ZOUT_H       0x3F
#define ACCEL_ZOUT_L       0x40
#define TEMP_OUT_H         0x41
#define TEMP_OUT_L         0x42
#define GYRO_XOUT_H        0x43
#define GYRO_XOUT_L        0x44
#define GYRO_YOUT_H        0x45
#define GYRO_YOUT_L        0x46
#define GYRO_ZOUT_H        0x47
#define GYRO_ZOUT_L        0x48

// container for the MPU
typedef struct MPU9X6 {
  // IMU Address
  uint8_t address;

  // IMU Information
  int16_t Ax, Ay, Az;     // Accelerometer data
  int16_t Tmp;            // temperature data
  int16_t Gx, Gy, Gz;     // Gyroscope data

} MPU9X6;

#endif
