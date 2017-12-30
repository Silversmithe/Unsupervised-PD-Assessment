/*
--------------------------------------------------------------------------------
Headers for simple Raw information reading from:

    MPU9250 : 9 DOF IMU
    MPU6050 : 6 DOF IMU

Alexander S. Adranly (aadranly@scu.edu)
--------------------------------------------------------------------------------
Using Resources from Sparkfun
--------------------------------------------------------------------------------
*/
#include "Arduino.h"
#include <stdint.h>        // different int types

#ifndef MPU9X6_H
#define MPU9X6_H

// Possible Addresses
#define MPU_ADDR_LO        0x68
#define MPU_ADDR_HI        0x69

/* HARDWARE REGISTERS */
// HARDWARE IDENTIFIER
#define WHO_AM_I_MPU9X6   0x75

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

//Magnetometer Registers
#define AK8963_ADDRESS   0x0C
#define WHO_AM_I_AK8963  0x49 // (AKA WIA) should return 0x48
#define INFO             0x01
#define AK8963_ST1       0x02  // data ready status bit 0
#define AK8963_XOUT_L    0x03  // data
#define AK8963_XOUT_H    0x04
#define AK8963_YOUT_L    0x05
#define AK8963_YOUT_H    0x06
#define AK8963_ZOUT_L    0x07
#define AK8963_ZOUT_H    0x08
#define AK8963_ST2       0x09  // Data overflow bit 3 and data read error status bit 2
#define AK8963_CNTL      0x0A  // Power down (0000), single-measurement (0001), self-test (1000) and Fuse ROM (1111) modes on bits 3:0
#define AK8963_ASTC      0x0C  // Self test control
#define AK8963_I2CDIS    0x0F  // I2C disable
#define AK8963_ASAX      0x10  // Fuse ROM x-axis sensitivity adjustment value
#define AK8963_ASAY      0x11  // Fuse ROM y-axis sensitivity adjustment value
#define AK8963_ASAZ      0x12  // Fuse ROM z-axis sensitivity adjustment value

/* STRUCTURE */
typedef struct MPU9X6 {
  // IMU Address
  uint8_t bus;             // either bus 0 or bus 1 (values 0 | 1)
  uint8_t address;         // either MPU_ADDR_LO or MPU_ADDR_HI

  // IMU Information
  int16_t acceleration[3]; // Accelerometer data (x, y, z)
  int16_t gyroscope[3];    // Gyroscope data (x, y, z)
  int16_t magnetometer[3]; // Magnetometer Data (x, y, z)
  int16_t temp;            // temperature data
} MPU9X6;

/* STATUS VARIABLES */
bool busses_initialized = false;   // cannot do anything else until initialized

/*
  FUNCTIONS

  High Level Functinos to organize and make readable the functions for the
  wearable application.
*/
int8_t init_buses();                        // Initialize all I2C interfaces
int8_t stim_imus(uint8_t control);          // wake or sleep IMU

// individual functions
uint8_t who_am_i(MPU9X6* imu);     // Just identify what address the device is on

/* SENSOR COLLECTION */
// Accel, Gyro, Magnet, Temp --> IMU
uint8_t get_sensor_data(MPU9X6* imu); // collect all of the info at front

// I2C functions
uint8_t read_byte(MPU9X6* imu, uint8_t reg_address);
uint8_t read_bytes(MPU9X6* imu, uint8_t reg_address, uint8_t bytes);


#endif
