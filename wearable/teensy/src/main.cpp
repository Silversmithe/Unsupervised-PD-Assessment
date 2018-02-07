/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 1: IRON FIST)

  author:       Alexander Sami Adranly
  ------------------------------------------------------------------------------
  description:  Main Application for gathering and reporting information of both
  sensors in one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.
  ----------------------------------------------------------------------------*/
#include "main.h"
#include <Arduino.h>              // Arduino Library
#include "stdint.h"               // Integer Library
#include "TimerOne.h"             // Timer Libaray

/* VARIABLES */
static IOBuffer BUFFER(BUFFER_SIZE);
static Data temp_data;
static uint32_t current_time, instant_time, delta_time;

/* DEVICE INITIALIZATION */
EMG forearm(RECT_PIN, RAW_PIN);
MPU9250 tfinger_imu(Wire, IMU_ADDR_LO);
MPU9250 pfinger_imu(Wire, IMU_ADDR_HI);
MPU9250 dhand_imu(Wire1, IMU_ADDR_HI);
MPU9250 rfinger_imu(Wire1, IMU_ADDR_LO);

/* SETUP */
void setup() {
  /* PIN SETUP */
  pinMode(BUILTIN_LED, OUTPUT);

  /* COMMUNICATION SETUP */
  if (SERIAL_SELECT){
    Serial.begin(BAUD_RATE);
    while(!Serial) { }//com_search_light(BUILTIN_LED); }
  } // endif

  /* SENSOR SETUP */
  imu_setup();

  /* TIMER SETUP */
  Timer1.initialize(FULL_SAMPLE_RATE); // DEMO_RATE FULL_SAMPLE_RATE DOUBLE_SAMPLE_RATE
  Timer1.attachInterrupt(sensor_isr);

  current_time = micros();            // initialize timer
}

/* MAIN LOOP */
void loop() {
  /* consumer of the IOBuffer */
  if(!BUFFER.is_empty()){
    // remove a Data item from buffer
    temp_data = BUFFER.remove_front();
    /* DATA PROCESSING */

    // Load Position data into Data structures using Mahony Filter
    // orient(data, HAND_SELECT, THUMB_SELECT, POINT_SELECT, RING_SELECT);

    /* DATA TRANSFER */
    if(SERIAL_SELECT){
      // HAND
      for(int i=0; i<3; i++){
        Serial.print(temp_data.hand[i]);
        Serial.print("\t");
      }

      // thumb
      for(int i=0; i<3; i++){
        Serial.print(temp_data.thumb[i]);
        Serial.print("\t");
      }

      // point
      for(int i=0; i<3; i++){
        Serial.print(temp_data.point[i]);
        Serial.print("\t");
      }

      // ring
      for(int i=0; i<3; i++){
        Serial.print(temp_data.ring[i]);
        Serial.print("\t");
      }
      Serial.println();


    } else if(XBEE_SELECT){

    } // fin communication
  } // fin buffer

  delay(10);
}

/* INITIALIZATION */
void imu_setup(){
  /*
    Initialize all IMUs accordingly
  */
  /* TEMPORARY VARS */
  int status;                                 // status for imu setup
  // needs to have error handling
  if(THUMB_SELECT){
    status = tfinger_imu.begin();
    if(status < 0){
      while(1){
        Serial.print("thumb imu: unable to be initialized...\n");
        Serial.print("\tstatus: ");
        Serial.println(status);
        delay(1000);
      }
    } // end bad status
  } // init thumb imu

  if(POINT_SELECT){
    status = pfinger_imu.begin();
    if(status < 0){
      while(1){
        Serial.print("point imu: unable to be initialized...\n");
        Serial.print("\tstatus: ");
        Serial.println(status);
        delay(1000);
      }
    } // end bad status
  } // init pointer imu

  if(RING_SELECT){
    status = rfinger_imu.begin();
    if(status < 0){
      while(1){
        Serial.print("ring imu: unable to be initialized...\n");
        Serial.print("\tstatus: ");
        Serial.println(status);
        delay(1000);
      }
    } // end bad status
  } // init thumb imu

  if(HAND_SELECT){
    status = dhand_imu.begin();
    if(status < 0){
      while(1){
        Serial.print("hand imu: unable to be initialized...\n");
        Serial.print("\tstatus: ");
        Serial.println(status);
        delay(1000);
      }
    } // end bad status
  } // init thumb imu
}

/* SENSOR FUNCTIONS */
void sensor_isr(){
  /*
    Should time to see how long this takes
  */
  // update the time
  instant_time = micros();
  delta_time = instant_time - current_time;
  current_time = instant_time;

  // new information set for buffer
  Data packet = {
    {0,0},                    // EMG DATA
    {0,0,0,0,0,0,0,0,0,0},    // HAND
    {0,0,0},                  // HPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // THUMB
    {0,0,0},                  // TPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // POINT
    {0,0,0},                  // PPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // RING
    {0,0,0},                  // RPOSITION
    delta_time                // dt
  };

  if(EMG_SELECT){
    packet.emg[0] = forearm.getRaw();
    packet.emg[1] = forearm.getRect();
  }

  if(HAND_SELECT){
    dhand_imu.readSensor();
    // accel
    packet.hand[0] = dhand_imu.getAccelX_mss();
    packet.hand[1] = dhand_imu.getAccelY_mss();
    packet.hand[2] = dhand_imu.getAccelZ_mss();
    // gyro
    packet.hand[3] = dhand_imu.getGyroX_rads();
    packet.hand[4] = dhand_imu.getGyroY_rads();
    packet.hand[5] = dhand_imu.getGyroZ_rads();
    // mag
    packet.hand[6] = dhand_imu.getMagX_uT();
    packet.hand[7] = dhand_imu.getMagY_uT();
    packet.hand[8] = dhand_imu.getMagZ_uT();
    // temp
    packet.hand[9] = dhand_imu.getTemperature_C();
  }

  if(THUMB_SELECT){
    tfinger_imu.readSensor();
    // accel
    packet.thumb[0] = tfinger_imu.getAccelX_mss();
    packet.thumb[1] = tfinger_imu.getAccelY_mss();
    packet.thumb[2] = tfinger_imu.getAccelZ_mss();
    // gyro
    packet.thumb[3] = tfinger_imu.getGyroX_rads();
    packet.thumb[4] = tfinger_imu.getGyroY_rads();
    packet.thumb[5] = tfinger_imu.getGyroZ_rads();
    // mag
    packet.thumb[6] = tfinger_imu.getMagX_uT();
    packet.thumb[7] = tfinger_imu.getMagY_uT();
    packet.thumb[8] = tfinger_imu.getMagZ_uT();
    // temp
    packet.thumb[9] = tfinger_imu.getTemperature_C();
  }

  if(POINT_SELECT){
    pfinger_imu.readSensor();
    // accel
    packet.point[0] = pfinger_imu.getAccelX_mss();
    packet.point[1] = pfinger_imu.getAccelY_mss();
    packet.point[2] = pfinger_imu.getAccelZ_mss();
    // gyro
    packet.point[3] = pfinger_imu.getGyroX_rads();
    packet.point[4] = pfinger_imu.getGyroY_rads();
    packet.point[5] = pfinger_imu.getGyroZ_rads();
    // mag
    packet.point[6] = pfinger_imu.getMagX_uT();
    packet.point[7] = pfinger_imu.getMagY_uT();
    packet.point[8] = pfinger_imu.getMagZ_uT();
    // temp
    packet.point[9] = pfinger_imu.getTemperature_C();
  }

  if(RING_SELECT){
    rfinger_imu.readSensor();
    // accel
    packet.ring[0] = rfinger_imu.getAccelX_mss();
    packet.ring[1] = rfinger_imu.getAccelY_mss();
    packet.ring[2] = rfinger_imu.getAccelZ_mss();
    // gyro
    packet.ring[3] = rfinger_imu.getGyroX_rads();
    packet.ring[4] = rfinger_imu.getGyroY_rads();
    packet.ring[5] = rfinger_imu.getGyroZ_rads();
    // mag
    packet.ring[6] = rfinger_imu.getMagX_uT();
    packet.ring[7] = rfinger_imu.getMagY_uT();
    packet.ring[8] = rfinger_imu.getMagZ_uT();
    // temp
    packet.ring[9] = rfinger_imu.getTemperature_C();
  }

  // store packet in buffer
  BUFFER.push_back(packet);
}
