/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 2: SECOND SKIN)

  author:       Alexander S. Adranly
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
static Data* temp_data;
static uint32_t current_time, instant_time, delta_time;

/* STATE */
State __current_state;
ERROR __error;

/* DEVICE INITIALIZATION */
bool __enabled[4] = {
  HAND_SELECT,
  THUMB_SELECT,
  POINT_SELECT,
  RING_SELECT
};

EMG forearm(RECT_PIN, RAW_PIN);
MPU9250 __imus[4] = {
  MPU9250(Wire1, IMU_ADDR_HI),   // hand
  MPU9250(Wire, IMU_ADDR_LO),   // thumb finger
  MPU9250(Wire, IMU_ADDR_HI),   // pointer finger
  MPU9250(Wire1, IMU_ADDR_LO)   // ring finger
};

/*
 * @function:     setup
 *
 * @description:  main initialization function, responsible creating all of the
 *                variables and doing the initial checks for hardware, networking,
 *                logging, and initializing the automata and error states.
 */
void setup(void) {
  bool hardware_success = false;
  bool network_success = false;
  __error = NONE;           // initialize error
  __current_state = INIT;   // Initialization state

  /* HARDWARE INITIALIZATION PROCEDURE */
  // 1. can you initialize all hardware?
  // STATE <- YES: INIT, NO: KILL
  pinMode(BUILTIN_LED, OUTPUT);   // BUILTIN_LED -> 13 D
  hardware_success |= init_com();            // setup HWSERIAL & XBEE
  hardware_success |= imu_setup(true);      // setup IMU
  if(!hardware_success){
    __current_state = KILL;
    kill();
  }

  /* NETWORK INITIALIZATION PROCEDURE */
  // 1. Can you contact the server?
  //    STATE <- YES: ONLINE, NO: OFFLINE
  // 2. How strong is the connection?
  //    STATE <- > 50%: ONLINE, < 50%: OFFLINE
  if(XBEE_SELECT){ network_success = isAnyoneThere(); }

  __current_state = (network_success)? ONLINE : OFFLINE;
  if(__current_state == ONLINE)
    log("current state: ONLINE");
  else
    log("current state: OFFLINE");

  /* delay and signal before running */
  for(int i=0; i<5; i++){
    if(__current_state == ONLINE) { online_light(); }
    else { offline_light(); }
  }
  log("starting device...");

  // kill();
  /* START SENSOR INTERRUPT */
  Timer1.initialize(FULL_SAMPLE_RATE); // DEMO_RATE FULL_SAMPLE_RATE DOUBLE_SAMPLE_RATE
  Timer1.attachInterrupt(sensor_isr);
  current_time = micros();            // initialize timer
}

/*
 * @function:     loop
 *
 * @description:  main consumer thread, responsible for picking packets out
 *                of the buffer and sending it over the radio or the serial
 *                monitor.
 */
void loop(void) {
  /* check errors */
  if(__error != NONE){
    // could eventually do error recovery here
    /* output into the log */
    log("error: an error has occurred...");
    log(__error);
    __current_state = KILL;
    kill();
  }

  // eventually do BURST logging
  // wait to log after a set of points have been collected

  if(!BUFFER.is_empty()){
      // remove a Data item from buffer
      temp_data = BUFFER.remove_front();
      /* DATA PROCESSING */
      // Load Position data into Data structures using Mahony Filter
      // orient(data, HAND_SELECT, THUMB_SELECT, POINT_SELECT, RING_SELECT);
      /* DATA TRANSFER */
      if(SERIAL_SELECT){ write_console(temp_data); }

      if(__current_state == ONLINE){ /* ONLINE */
        write_radio(temp_data);
      } else { /* OFFLINE */
        log_payload(temp_data);
      }
  }
  delay(CONSUMER_RATE);
}

/*
 * @function:     kill
 *
 * @description:  put the device in an infinite state of waiting and notify
 *                the user that the device should be rebooted or debugged
 */
void kill(void){
  kill_light();
  while(1){ delay(10000); }
}

/*
 * @function:     imu_setup
 *
 * @param:        (bool) trace: turn on debugger tracer
 *
 * @description:  hardware initialization of the inertial measurement
 *                units. should return some status of the operations.
 *                Returns true if the initialization was 100% successful.
 */
bool imu_setup(bool trace){
  int status[4];
  bool out = false;
  if(trace && !SERIAL_SELECT) { return false; }

  for(int i=0; i<4; i++){
    if(__enabled[i]){
      status[i] = __imus[i].begin();
      out = out | !(status[i] < 0);
      if(trace && status[i] < 0){
        Serial.print("(");
        Serial.print(i);
        Serial.print("): hardware error, CODE: ");
        Serial.println(status[i]);
        delay(1000);
      }
    }
  }
  return out;
}

/*
 * @function:     sensor_isr
 *
 * @description:  method that runs after each interrupt from the main thread.
 *                this function is responsible for gathering all the information
 *                from the sensors and store it in a packet, which gets pushed
 *                onto the buffer.
 */
void sensor_isr(void){
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
    __imus[0].readSensor();
    // accel
    packet.hand[0] = __imus[0].getAccelX_mss();
    packet.hand[1] = __imus[0].getAccelY_mss();
    packet.hand[2] = __imus[0].getAccelZ_mss();
    // gyro
    packet.hand[3] = __imus[0].getGyroX_rads();
    packet.hand[4] = __imus[0].getGyroY_rads();
    packet.hand[5] = __imus[0].getGyroZ_rads();
    // mag
    packet.hand[6] = __imus[0].getMagX_uT();
    packet.hand[7] = __imus[0].getMagY_uT();
    packet.hand[8] = __imus[0].getMagZ_uT();
    // temp
    packet.hand[9] = __imus[0].getTemperature_C();
  }

  if(THUMB_SELECT){
    __imus[1].readSensor();
    // accel
    packet.thumb[0] = __imus[1].getAccelX_mss();
    packet.thumb[1] = __imus[1].getAccelY_mss();
    packet.thumb[2] = __imus[1].getAccelZ_mss();
    // gyro
    packet.thumb[3] = __imus[1].getGyroX_rads();
    packet.thumb[4] = __imus[1].getGyroY_rads();
    packet.thumb[5] = __imus[1].getGyroZ_rads();
    // mag
    packet.thumb[6] = __imus[1].getMagX_uT();
    packet.thumb[7] = __imus[1].getMagY_uT();
    packet.thumb[8] = __imus[1].getMagZ_uT();
    // temp
    packet.thumb[9] = __imus[1].getTemperature_C();
  }

  if(POINT_SELECT){
    __imus[2].readSensor();
    // accel
    packet.point[0] = __imus[2].getAccelX_mss();
    packet.point[1] = __imus[2].getAccelY_mss();
    packet.point[2] = __imus[2].getAccelZ_mss();
    // gyro
    packet.point[3] = __imus[2].getGyroX_rads();
    packet.point[4] = __imus[2].getGyroY_rads();
    packet.point[5] = __imus[2].getGyroZ_rads();
    // mag
    packet.point[6] = __imus[2].getMagX_uT();
    packet.point[7] = __imus[2].getMagY_uT();
    packet.point[8] = __imus[2].getMagZ_uT();
    // temp
    packet.point[9] = __imus[2].getTemperature_C();
  }

  if(RING_SELECT){
    __imus[3].readSensor();
    // accel
    packet.ring[0] = __imus[3].getAccelX_mss();
    packet.ring[1] = __imus[3].getAccelY_mss();
    packet.ring[2] = __imus[3].getAccelZ_mss();
    // gyro
    packet.ring[3] = __imus[3].getGyroX_rads();
    packet.ring[4] = __imus[3].getGyroY_rads();
    packet.ring[5] = __imus[3].getGyroZ_rads();
    // mag
    packet.ring[6] = __imus[3].getMagX_uT();
    packet.ring[7] = __imus[3].getMagY_uT();
    packet.ring[8] = __imus[3].getMagZ_uT();
    // temp
    packet.ring[9] = __imus[3].getTemperature_C();
  }

  // store packet in buffer
  BUFFER.push_back(packet);
}
