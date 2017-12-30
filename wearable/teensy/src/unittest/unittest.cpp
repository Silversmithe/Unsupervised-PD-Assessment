/*
  ------------------------------------------------------------------------------
  unittest.cpp

  Alexander S. Adranly
  December 29th, 2017
  ------------------------------------------------------------------------------
  Code to test different levels of functionality
  ------------------------------------------------------------------------------
*/
#include "Arduino.h"
#include "stdint.h"
#include "i2c/i2c_t3.h"       // Teensy wire library
#include "MPU9250/MPU9250.h"
#include "MyoEMG/MyoEMG.h"
#include "unittest.h"

/* DEFAULT PIN DEFINITIONS */

/* FUNCTIONS */
bool unittest_runner(uint8_t mode_type){
/*
  Runs selected unit test

  @param: (uint8_t) mode_type: the selector to determine what unittest to run
  @return: (bool) a boolean value to determine success (true) or failure (false)
*/
  switch (mode_type) {
    case 0x01: return emg_0(); break;
    case 0x02: return emg_1(); break;
    case 0x03: return imu_0(); break;
    case 0x04: return imu_1(); break;
  }
}

/* UNIT TESTS */
// EMG
bool emg_0 (){
/*
  testing one emg for rectified signal on console, SERIAL
*/
  /* SETUP */
  Serial.begin(9600);
  while(!Serial) {};

  EMG my_emg(13);    // creating an EMG
  const uint32_t runtime = 1000; // 1 second --> 1,000 miliseconds
  uint32_t current_time = millis();
  uint32_t final_time = current_time + runtime;

  /* TIMED LOOP */
  while(current_time < final_time){
    Serial.print("Rect: ");
    Serial.println(my_emg.getRect());    // display information (bad practice)
    current_time = millis();         // collect EMG information
    delay(50);
  }

  Serial.end();                      // close the serial monitor
  return true;
}

bool emg_1 (){
/*
  testing emg for raw signal, SERIAL
*/
    /* SETUP */
    Serial.begin(9600);
    while(!Serial) {};

    EMG my_emg(13);    // creating an EMG
    const uint32_t runtime = 1000; // 1 second --> 1,000 miliseconds
    uint32_t current_time = millis();
    uint32_t final_time = current_time + runtime;

    /* TIMED LOOP */
    while(current_time < final_time){
      Serial.print("Rect: ");
      Serial.print(my_emg.getRect());    // display information (bad practice)
      Serial.print(", Raw: ");
      Serial.println(my_emg.getRaw());
      current_time = millis();         // collect EMG information
      delay(50);
    }

    Serial.end();                      // close the serial monitor
    return true;
}

// IMU
bool imu_0 (){
/*
  testing one imu, all signals, SERIAL
*/
  /* SETUP */
  Serial.begin(9600);
  while(!Serial) {};

  MPU9250 imu(Wire, 0x68);
  int status;
  // TIMING
  const uint32_t runtime = 1000; // 1 second --> 1,000 miliseconds
  uint32_t current_time = millis();
  uint32_t final_time = current_time + runtime;

  status = imu.begin();
  // check to ensure successful startup
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }

  /* TIMED LOOP */
  while(current_time < final_time){
    // read the sensor
    IMU.readSensor();
    // display the data
    Serial.print(imu.getAccelX_mss(),6);
    Serial.print("\t");
    Serial.print(imu.getAccelY_mss(),6);
    Serial.print("\t");
    Serial.print(imu.getAccelZ_mss(),6);
    Serial.print("\t");
    Serial.print(imu.getGyroX_rads(),6);
    Serial.print("\t");
    Serial.print(imu.getGyroY_rads(),6);
    Serial.print("\t");
    Serial.print(imu.getGyroZ_rads(),6);
    Serial.print("\t");
    Serial.print(imu.getMagX_uT(),6);
    Serial.print("\t");
    Serial.print(imu.getMagY_uT(),6);
    Serial.print("\t");
    Serial.print(imu.getMagZ_uT(),6);
    Serial.print("\t");
    Serial.println(imu.getTemperature_C(),6);
    delay(100);
  }
}

bool imu_1 (){
/*
  testing two imu, on one bus, SERIAL
*/
  /* SETUP */

  /* TIMED LOOP */

}
