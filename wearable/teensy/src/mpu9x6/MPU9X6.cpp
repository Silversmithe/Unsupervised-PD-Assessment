/*
--------------------------------------------------------------------------------
Code for simple Raw information reading from:

    MPU9250 : 9 DOF IMU
    MPU6050 : 6 DOF IMU

Alexander S. Adranly (aadranly@scu.edu)
--------------------------------------------------------------------------------
Using Resources from Sparkfun
Using pins 18,19 & 37,38 for Wire & Wire1, should be able to handle 4 devices
--------------------------------------------------------------------------------
*/
#include "MPU9X6.h"
#include "../i2c/i2c_t3.h"

int8_t init_buses(){
  /*
    Initialize Busses
    -------------------

    Initialize all I2C interfaces
  */
  Wire.begin(I2C_MASTER, 0x00, I2C_PINS_18_19, I2C_PULLUP_EXT, 400000);
  Wire1.begin(I2C_MASTER, 0x00, I2C_PINS_37_38, I2C_PULLUP_EXT, 400000);
  busses_initialized = true;
}

int8_t stim_imus(uint8_t control){
  /*
    stimulate IMUs
    --------------
    Given a control variable where the lower nyble represents the power states
    of the four imus controlled by the teensy.

    The two lower bits represent the two addresses on the first bus (Wire) and
    the two upper bits represent the two addresses of the second bus (Wire1)

    bus2(hi lo) bus1(hi lo)

    @param: (uint8_t) control: a byte that tells which devices should be on or
                               off.
                               example control var:

                               0000 1010
                               From left to right (1 nyble)
                               - bus1 (Wire) address 0x68 (MPU_ADDR_LO) : OFF
                               - bus1 (Wire) address 0x69 (MPU_ADDR_HI) : ON
                               - bus2 (Wire1) address 0x68 (MPU_ADDR_LO) : OFF
                               - bus2 (Wire1) address 0x69 (MPU_ADDR_HI) : ON
  */
  if(!busses_initialized) return -1; // error

  // check each byte of the nyble
  // CHECK BUS1 LO ADDR
  Wire.beginTransmission(MPU_ADDR_LO);
  Wire.write(PWR_MGMT_1);   // start by writing to the power management
  // writing 0 --> ON, writing 1 --> OFF
  if((control & 0x01) == 0x01){ Wire.write(0); } else { Wire.write(1); }
  Wire.endTransmission(true);

  // CHECK BUS1 HI ADDR
  Wire.beginTransmission(MPU_ADDR_HI);
  Wire.write(PWR_MGMT_1);   // start by writing to the power management
  if((control & 0x02) == 0x02){ Wire.write(0); } else { Wire.write(1); }
  Wire.endTransmission(true);

  // CHECK BUS2 LO ADDR
  Wire1.beginTransmission(MPU_ADDR_LO);
  Wire1.write(PWR_MGMT_1);   // start by writing to the power management
  if((control & 0x04) == 0x04){ Wire1.write(0); } else { Wire1.write(1); }
  Wire1.endTransmission(true);

  // CHECK BUS2 HI ADDR
  Wire1.beginTransmission(MPU_ADDR_HI);
  Wire1.write(PWR_MGMT_1);   // start by writing to the power management
  if((control & 0x08) == 0x08){ Wire1.write(0); } else { Wire1.write(1); }
  Wire1.endTransmission(true);

  return 1; // success
}

uint8_t who_am_i(MPU9X6* imu){
  /*
   Who Am I?
   ----------------
   Just identify what address the device is on
   DEBUGGING CODE

   @param: (MPU9X6*) imu: pointer to the imu struct

   @return: (uint8_t): -1 (error), device address?
  */
  return read_byte(imu, WHO_AM_I_MPU9X6);
}

/* SENSOR COLLECTION */
uint8_t get_sensor_data(MPU9X6* imu){
  // collect all of the info at front
}

/* I2C functions */
uint8_t read_byte(MPU9X6* imu, uint8_t reg_address){
  /*
    Read Byte
    -----------
    Reads bytes from a specific device register and returns the value
    Reads from the address specified in the IMU struct and the register address

    @param: (MPU9X6*) imu: pointer to the imu struct
    @param: (uint8_t) reg_address: address to read from the imu

    @return: (uint8_t): resulting value of register
  */
  if(!busses_initialized) return -1; // error

  // announce that you want to identify IMU
  if(imu->bus == 0){
    // start bus0 transmission on address
    Wire.beginTransmission(imu->address);
    // read data
    Wire.write(reg_address); // start reading from the identification reg
    Wire.endTransmission(false);
    // WHO AM I
    Wire.requestFrom(imu->address, 1, true); // reading the one byte
    return Wire.read();

  } else {
    // start bus 1 transmission on address
    Wire1.beginTransmission(imu->address);
    Wire1.write(reg_address); // start reading from the identification reg
    Wire1.endTransmission(false);
    // WHO AM I
    Wire1.requestFrom(imu->address, 1, true); // reading the one byte
    return Wire1.read();
  }

  return -1; // error if you get here
}

uint8_t read_bytes(MPU9X6* imu, uint8_t reg_address, uint8_t bytes){

}
