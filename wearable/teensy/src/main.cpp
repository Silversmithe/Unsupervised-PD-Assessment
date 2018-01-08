/*
--------------------------------------------------------------------------------
  main.cpp (Wearable Version 1)

  Main Application for gathering and reporting information of both sensors in
  one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.

  Alexander Sami Adranly
--------------------------------------------------------------------------------
NOTES
January 4th, 2018
- Pointer and Thumb IMU will be on the same BUS
- Hand and Ring IMU will be on the same BUS
--------------------------------------------------------------------------------
*/
#include "main.h"
#include "Arduino.h"              // Arduino Library
#include "stdint.h"               // Integer Library
#include "TimerOne.h"             // Timer Libaray

/* VARIABLES */
IOMedBuffer BUFFER(BUFFER_SIZE);
uint32_t current_time, instant_time, delta_time;

/* DEVICE INITIALIZATION */
EMG forearm(RECT_PIN, RAW_PIN);   // initialize the forearm
MPU9250 tfinger_imu(Wire, IMU_ADDR_LO);
MPU9250 pfinger_imu(Wire, IMU_ADDR_HI);
MPU9250 dhand_imu(Wire1, IMU_ADDR_LO);
MPU9250 rfinger_imu(Wire1, IMU_ADDR_HI);

/* SETUP */
void setup() {
  /* PIN SETUP */
  pinMode(BUILTIN_LED, OUTPUT);

  /* COMMUNICATION SETUP */
  if (SERIAL_SELECT){
    Serial.begin(BAUD_RATE);
    while(!Serial) { com_search_light(); }
  } // endif

  /* SENSOR SETUP */
  imu_setup();

  /* TIMER SETUP */
  Timer1.initialize(FULL_SAMPLE_RATE);
  Timer1.attachInterrupt(sensor_isr);

  current_time = micros();            // initialize timer
}

/* MAIN LOOP */
void loop() {

  delay(1000);
}

/* FUNCTIONS */
// -----------------------------------------------------------------------------
void imu_setup(){
  /*
    Initialize all IMUs accordingly
  */
  /* TEMPORARY VARS */
  int status;                                 // status for imu setup

  if(THUMB_SELECT){
    status = tfinger_imu.begin();
    if(status < 0){
      fprint("thumb imu: unable to be initialized...\n");
      fprint("\tstatus: %d\n", status);
    } // end bad status
  } // init thumb imu

  if(POINT_SELECT){
    status = pfinger_imu.begin();
    if(status < 0){
      fprint("point imu: unable to be initialized...\n");
      fprint("\tstatus: %d\n", status);
    } // end bad status
  } // init pointer imu

  if(RING_SELECT){
    status = rfinger_imu.begin();
    if(status < 0){
      fprint("ring imu: unable to be initialized...\n");
      fprint("\tstatus: %d\n", status);
    } // end bad status
  } // init thumb imu

  if(HAND_SELECT){
    status = dhand_imu.begin();
    if(status < 0){
      fprint("hand imu: unable to be initialized...\n");
      fprint("\tstatus: %d\n", status);
    } // end bad status
  } // init thumb imu
}

// -----------------------------------------------------------------------------

void sensor_isr(){
  /*
    Should time to see how long this takes
  */
  uint32_t delta;
  uint32_t start = micros();
  MedData packet;   // new information set for buffer

  // update the time
  instant_time = micros();
  delta_time = instant_time - current_time;
  current_time = instant_time;
  // add the change in time always to the packet
  packet.dT = delta_time;

  if(EMG_SELECT){
    packet.emg_raw = forearm.getRaw();
    packet.emg_rect = forearm.getRect();
  } else {
    // fill packet with zeros
    packet.emg_raw = 0;
    packet.emg_rect = 0;
  }

  if(HAND_SELECT){
    dhand_imu.readSensor();
    // accel
    packet.Hand_Ax = dhand_imu.getAccelX_mss();
    packet.Hand_Ay = dhand_imu.getAccelY_mss();
    packet.Hand_Az = dhand_imu.getAccelZ_mss();
    // gyro
    packet.Hand_Gx = dhand_imu.getGyroX_rads();
    packet.Hand_Gy = dhand_imu.getGyroY_rads();
    packet.Hand_Gz = dhand_imu.getGyroZ_rads();
    // mag
    packet.Hand_Mx = dhand_imu.getMagX_uT();
    packet.Hand_My = dhand_imu.getMagY_uT();
    packet.Hand_Mz = dhand_imu.getMagZ_uT();
    // temp
    packet.Hand_T = dhand_imu.getTemperature_C();
  } else {
    // accel
    packet.Hand_Ax = 0.0;
    packet.Hand_Ay = 0.0;
    packet.Hand_Az = 0.0;
    // gyro
    packet.Hand_Gx = 0.0;
    packet.Hand_Gy = 0.0;
    packet.Hand_Gz = 0.0;
    // mag
    packet.Hand_Mx = 0.0;
    packet.Hand_My = 0.0;
    packet.Hand_Mz = 0.0;
    // temp
    packet.Hand_T = 0.0;
  }

  if(THUMB_SELECT){
    tfinger_imu.readSensor();
    // accel
    packet.Thumb_Ax = tfinger_imu.getAccelX_mss();
    packet.Thumb_Ay = tfinger_imu.getAccelY_mss();
    packet.Thumb_Az = tfinger_imu.getAccelZ_mss();
    // gyro
    packet.Thumb_Gx = tfinger_imu.getGyroX_rads();
    packet.Thumb_Gy = tfinger_imu.getGyroY_rads();
    packet.Thumb_Gz = tfinger_imu.getGyroZ_rads();
    // mag
    packet.Thumb_Mx = tfinger_imu.getMagX_uT();
    packet.Thumb_My = tfinger_imu.getMagY_uT();
    packet.Thumb_Mz = tfinger_imu.getMagZ_uT();
    // temp
    packet.Thumb_T = tfinger_imu.getTemperature_C();
  } else {
    // accel
    packet.Thumb_Ax = 0.0;
    packet.Thumb_Ay = 0.0;
    packet.Thumb_Az = 0.0;
    // gyro
    packet.Thumb_Gx = 0.0;
    packet.Thumb_Gy = 0.0;
    packet.Thumb_Gz = 0.0;
    // mag
    packet.Thumb_Mx = 0.0;
    packet.Thumb_My = 0.0;
    packet.Thumb_Mz = 0.0;
    // temp
    packet.Thumb_T = 0.0;
  }

  if(POINT_SELECT){
    pfinger_imu.readSensor();
    // accel
    packet.Point_Ax = pfinger_imu.getAccelX_mss();
    packet.Point_Ay = pfinger_imu.getAccelY_mss();
    packet.Point_Az = pfinger_imu.getAccelZ_mss();
    // gyro
    packet.Point_Gx = pfinger_imu.getGyroX_rads();
    packet.Point_Gy = pfinger_imu.getGyroY_rads();
    packet.Point_Gz = pfinger_imu.getGyroZ_rads();
    // mag
    packet.Point_Mx = pfinger_imu.getMagX_uT();
    packet.Point_My = pfinger_imu.getMagY_uT();
    packet.Point_Mz = pfinger_imu.getMagZ_uT();
    // temp
    packet.Point_T = pfinger_imu.getTemperature_C();
  } else {
    // accel
    packet.Point_Ax = 0.0;
    packet.Point_Ay = 0.0;
    packet.Point_Az = 0.0;
    // gyro
    packet.Point_Gx = 0.0;
    packet.Point_Gy = 0.0;
    packet.Point_Gz = 0.0;
    // mag
    packet.Point_Mx = 0.0;
    packet.Point_My = 0.0;
    packet.Point_Mz = 0.0;
    // temp
    packet.Point_T = 0.0;
  }

  if(RING_SELECT){
    rfinger_imu.readSensor();
    // accel
    packet.Ring_Ax = rfinger_imu.getAccelX_mss();
    packet.Ring_Ay = rfinger_imu.getAccelY_mss();
    packet.Ring_Az = rfinger_imu.getAccelZ_mss();
    // gyro
    packet.Ring_Gx = rfinger_imu.getGyroX_rads();
    packet.Ring_Gy = rfinger_imu.getGyroY_rads();
    packet.Ring_Gz = rfinger_imu.getGyroZ_rads();
    // mag
    packet.Ring_Mx = rfinger_imu.getMagX_uT();
    packet.Ring_My = rfinger_imu.getMagY_uT();
    packet.Ring_Mz = rfinger_imu.getMagZ_uT();
    // temp
    packet.Ring_T = rfinger_imu.getTemperature_C();
  } else {
    // accel
    packet.Ring_Ax = 0.0;
    packet.Ring_Ay = 0.0;
    packet.Ring_Az = 0.0;
    // gyro
    packet.Ring_Gx = 0.0;
    packet.Ring_Gy = 0.0;
    packet.Ring_Gz = 0.0;
    // mag
    packet.Ring_Mx = 0.0;
    packet.Ring_My = 0.0;
    packet.Ring_Mz = 0.0;
    // temp
    packet.Ring_T = 0.0;
  }

  // store packet in buffer
  // BUFFER.push_back(&packet);
  delta = micros() - start;
  Serial.println(delta);
}

// -----------------------------------------------------------------------------

void com_search_light(){
  /*
    Display if searching
  */
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(1000);
}

// -----------------------------------------------------------------------------

void fprint(const char* msg, ...){
  // print on a single line to serial monitor
  va_list args;
  va_start(args, msg);
  // print and return carriage to serial monitor
  if(SERIAL_SELECT){
    Serial.printf(msg, args);
  } // endif
  va_end(args);
}

// -----------------------------------------------------------------------------
