/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 2: Iron Fist)

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  Main Application for gathering and reporting information of both
  sensors in one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.

  NOTE: ADD A CAPACITOR THAT WILL KEEP THE PROTOTYPE RUNNING LONG ENOUGH SO THAT
  THE DEVICE CAN SHUT DOWN CORRECTLY

  check switch:
  if voltage == 0 :
    close data stream
  ----------------------------------------------------------------------------*/
#include "main.h"
#include <Arduino.h>              // Arduino Library
#include "analysis/analysis.h"    // analysis functions
#include "stdint.h"               // Integer Library
#include "TimerOne.h"             // Timer Libaray

/* VARIABLES */
static IOBuffer BUFFER(BUFFER_SIZE);
static Data* temp_data;
static uint32_t current_time, instant_time, delta_time;
static bool burst_write;

/* STATE */
volatile State __current_state;
volatile ERROR __error;

/* DEVICE INITIALIZATION */
bool __enabled[4] = {
  HAND_SELECT,
  RING_SELECT,
  POINT_SELECT,
  THUMB_SELECT
};

EMG forearm(RECT_PIN, RAW_PIN);
MPU9250 __imus[4] = {
  MPU9250(Wire, IMU_ADDR_HI),   // hand
  MPU9250(Wire, IMU_ADDR_LO),   // ring
  MPU9250(Wire1, IMU_ADDR_LO),   // pointer finger
  MPU9250(Wire1, IMU_ADDR_HI)   // thumb
};

/*
 * @function:     setup
 *
 * @description:  main initialization function, responsible creating all of the
 *                variables and doing the initial checks for hardware, networking,
 *                logging, and initializing the automata and error states.
 */
void setup(void) {
  burst_write = false;
  bool hardware_success = true;
  bool network_success = false;
  __error = NONE;           // initialize error
  __current_state = INIT;   // Initialization state
  current_time = micros();  // initial time

  /* HARDWARE INITIALIZATION PROCEDURE */
  // 1. can you initialize all hardware?
  // STATE <- YES: INIT, NO: KILL
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(XBEE_SLEEP_PIN, OUTPUT);
  hardware_success &= init_com();            // setup HWSERIAL & XBEE
  hardware_success &= imu_setup(false);      // setup IMU
  if(!hardware_success){
    __current_state = KILL;
    __error = IMU_ERROR;
    kill();
  }

  /* NETWORK INITIALIZATION PROCEDURE */
  // 1. Can you contact the server?
  //    STATE <- YES: ONLINE, NO: OFFLINE
  if(XBEE_SELECT){
    log("checking network status...");
    if(SERIAL_SELECT){ Serial.println("checking network status..."); }
    digitalWrite(XBEE_SLEEP_PIN, HIGH);
    delay(100);
    network_success = isAnyoneThere();
    digitalWrite(XBEE_SLEEP_PIN, LOW);
  }

  __current_state = (network_success)? ONLINE : OFFLINE;
  if(__current_state == ONLINE){
    log("state: online");
    if(SERIAL_SELECT){ Serial.println("state: online"); }
    /* FUTURE */
    // try to send data stored on SD wirelessly before getting a new batch
  } else {
    log("state: offline");
    if(SERIAL_SELECT){ Serial.println("state: offline"); }
    // if a data file exists, send it up
  }

  /* turn the radio off */
  digitalWrite(XBEE_SLEEP_PIN, LOW);

  /* delay and signal before running */
  for(int i=0; i<5; i++){
    if(__current_state == ONLINE) { online_light(); }
    else { offline_light(); }
  }
  log("starting device...");
  if(SERIAL_SELECT){ Serial.println("starting device..."); }

  /* START SENSOR INTERRUPT */
  Timer1.initialize(FULL_SAMPLE_RATE);
  Timer1.attachInterrupt(sensor_isr);
}

/*
 * @function:     loop
 *
 * @description:  main consumer thread, responsible for picking packets out
 *                of the buffer and sending it over the radio or the serial
 *                monitor.
 */
void loop(void) {
  /* ERROR CHECKING */
  if(__error != NONE){
    switch (__error) {
      case FATAL_ERROR:
        close_datastream();
        log("error: an fatal error has occurred...");
        if(SERIAL_SELECT){ Serial.println("error: an fatal error has occurred..."); }
        __current_state = KILL;
        kill();
        break;

      case ISOLATED_DEVICE_ERROR:
        close_datastream();
        log("error: device is unable to sustain a network connection...");
        if(SERIAL_SELECT){ Serial.println("error: device is unable to sustain a network connection..."); }
        log("msg: transitioning to OFFLINE state");
        if(SERIAL_SELECT){ Serial.println("msg: transitioning to OFFLINE state"); }
        __current_state = OFFLINE;
        __error = NONE;
        break;

      case BUFFER_OVERFLOW:
        close_datastream();
        log("error: I/O buffer has overflown...");
        if(SERIAL_SELECT){ Serial.println("error: I/O buffer has overflown..."); }
        if(__current_state == ONLINE) {
          log("msg: transitioning to OFFLINE state");
          if(SERIAL_SELECT){ Serial.println("msg: transitioning to OFFLINE state"); }
          __current_state = OFFLINE;
        } else if(__current_state == OFFLINE) {
          log("error: an fatal error has occurred...");
          if(SERIAL_SELECT){ Serial.println("error: an fatal error has occurred..."); }
          __current_state = KILL;
          kill();
        }
        break;

      case SD_ERROR:
        close_datastream();
        if(SERIAL_SELECT){ Serial.println("error: a sd card error has occured..."); }
        __current_state = KILL;
        kill_light();
        while(1){ delay(10000); }
        break;

      default: /* all other errors */
        close_datastream();
        log("error: an fatal error has occurred...");
        if(SERIAL_SELECT){ Serial.println("error: an fatal error has occurred..."); }
        __current_state = KILL;
        kill();
        break;
    } // end switch
  }

  /* CONSUMER BEHAVIOR */
  if(BUFFER.num_elts() >= BUFFER_STALL){
    /* open connection to consume */
    if(__current_state == ONLINE){
      digitalWrite(XBEE_SLEEP_PIN, HIGH);
    } else {  /* OFFLINE */
      open_datastream();
    }

    /* entirely flush the buffer */
    while(BUFFER.num_elts() > BUFFER_FLUSH){
      // remove a Data item from buffer
      digitalWrite(BUILTIN_LED, HIGH);

      noInterrupts();
      temp_data = BUFFER.remove_front();
      interrupts();

      /* DATA PROCESSING */
      orient(temp_data);    // Mahoney filtering -> orientation generation

      /* DATA TRANSFER */
      if(SERIAL_SELECT) { __error = write_console(temp_data); }

      if(__current_state == ONLINE) { __error = write_radio(temp_data); }
      else { __error = log_payload(temp_data); } /* OFFLINE */
      digitalWrite(BUILTIN_LED, LOW);
    }

    /* close connection to consume */
    if(__current_state == ONLINE){
      digitalWrite(XBEE_SLEEP_PIN, LOW);
    } else {  /* OFFLINE */
      close_datastream();
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
  log("state: kill");
  if(SERIAL_SELECT){ Serial.println("state: kill"); }
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
  bool out = true;
  if(trace && !SERIAL_SELECT) { return false; }

  for(int i=0; i<4; i++){
    if(__enabled[i]){
      status[i] = __imus[i].begin();
      out = out & !(status[i] < 0);
      if(trace && !out){
        while(true){
          Serial.print("(");
          Serial.print(i);
          Serial.print("): hardware error, CODE: ");
          Serial.println(status[i]);
          delay(1000);
        }
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
  // update the time
  instant_time = micros();
  delta_time = instant_time - current_time;
  current_time = instant_time;

  // new information set for buffer
  Data packet = {
    {0,0},                          // EMG DATA
    {0,0,0,0,0,0,0,0,0,0},          // HAND
    {0,0,0},                        // HPOSITION
    {0,0,0,0,0,0,0,0,0,0},          // THUMB
    {0,0,0},                        // TPOSITION
    {0,0,0,0,0,0,0,0,0,0},          // POINT
    {0,0,0},                        // PPOSITION
    {0,0,0,0,0,0,0,0,0,0},          // RING
    {0,0,0},                        // RPOSITION
    (float)(delta_time/1000000.0f)  // dt (seconds) = micros * sec/micros
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
    __imus[3].readSensor();
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
    __imus[1].readSensor();
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
  if(!BUFFER.push_back(packet)){ __error = BUFFER_OVERFLOW; }
}
