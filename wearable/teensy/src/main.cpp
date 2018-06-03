/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 2: Iron Fist)

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
static uint32_t __file_pos, __prev_pos;        // position of the data file
static bool __new_data;

/* STATE */
volatile bool __sampling_mode;          // sampling (true), transferring (false)
volatile State __current_state;         // what peripherals can device use
volatile ERROR __error;                 // any complications
volatile bool __isr_buffer_overflow;    // isr-triggered error
volatile bool __enable_sampling;        // the button has been pushed
volatile bool __radio_sleeping;         // is the radio asleep?
volatile bool __imu_sleeping;           // are the imus sleeping

/* DEVICE INITIALIZATION */
bool __enabled[4] = {
  HAND_SELECT,
  RING_SELECT,
  POINT_SELECT,
  THUMB_SELECT
};

EMG forearm(EMG_RECT_PIN, EMG_RAW_PIN);
MPU9250 Hand(Wire, MPU9250_AD1);
MPU9250 Ring(Wire, MPU9250_AD0);
MPU9250 Point(Wire1, MPU9250_AD0);
MPU9250 Thumb(Wire1, MPU9250_AD1);

/*
 * @function:     setup
 *
 * @description:  main initialization function, responsible creating all of the
 *                variables and doing the initial checks for hardware, networking,
 *                logging, and initializing the automata and error states.
 */
void setup(void) {
  bool hardware_success = true;
  bool network_success = false;
  __enable_sampling = false;
  __new_data = false; // usually false
  __file_pos = 0;
  __prev_pos = 0;
  __sampling_mode = false;
  __isr_buffer_overflow = false;
  __error = NONE;
  __current_state = INIT;

  /* HARDWARE INITIALIZATION PROCEDURE */
  // 1. can you initialize all hardware?
  // STATE <- YES: INIT, NO: KILL
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(BTN_MODE, INPUT);
  pinMode(LED_MODE_STAT, OUTPUT);
  pinMode(XBEE_SLEEP_PIN, OUTPUT);
  delay(1000);

  digitalWrite(XBEE_SLEEP_PIN, LOW); // set radio low
  __radio_sleeping = false;

  hardware_success = init_com(false) && hardware_success;
  hardware_success = imu_setup(false) && hardware_success;
  if(!hardware_success){
    __current_state = KILL;
    __error = IMU_ERROR;
    close_datastream();
    kill();
  }

  /* NETWORK INITIALIZATION PROCEDURE */
  // 1. Can you contact the server?
  //    STATE <- YES: ONLINE, NO: OFFLINE
  if(XBEE_SELECT){
    log("checking network status...");
    wakeRadio();
    delay(100);
    network_success = isAnyoneThere();
    sleepRadio();
  }

  __current_state = (network_success)? ONLINE : OFFLINE;
  if(__current_state == ONLINE){
    log("state: online");
    /* FUTURE */
    // try to send data stored on SD wirelessly before getting a new batch
  } else {
    log("state: offline");
    // if a data file exists, send it up
  }

  /* turn the radio off */
  wakeRadio();
  digitalWrite(LED_MODE_STAT, HIGH);

  /* delay and signal before running */
  for(int i=0; i<5; i++){
    if(__current_state == ONLINE) { online_light(); }
    else { offline_light(); }
  }

  /* declare start of device and current mode */
  log("starting device...");
  log("starting in transfer mode");

  /* INITIALIZE BUTTON INTERRUPT */
  attachInterrupt(BTN_MODE, btn_isr, CHANGE);
  /* INITIALIZE SENSOR INTERRUPT */
  Timer1.initialize(FULL_SAMPLE_RATE);  // FULL_SAMPLE_RATE
}

/*
 * @function:     loop
 *
 * @description:  main consumer thread, responsible for picking packets out
 *                of the buffer and sending it over the radio or the serial
 *                monitor.
 */
void loop(void) {
  /* error handling */
  if(__error != NONE || __isr_buffer_overflow){
    // isr generated interrupts
    if(__isr_buffer_overflow){
      __error = BUFFER_OVERFLOW;
      __isr_buffer_overflow = false;
    }

    switch (__error) {
      case FATAL_ERROR:
        close_datastream();
        log("error: an fatal error has occurred...");
        __current_state = KILL;
        kill();
        break;

      case ISOLATED_DEVICE_ERROR:
        close_datastream();
        log("error: device is unable to sustain a network connection...");
        log("msg: transitioning to OFFLINE state");
        __current_state = OFFLINE;
        __error = NONE;
        break;

      case BUFFER_OVERFLOW:
        close_datastream();
        log("error: I/O buffer has overflown...");
        log("error: an fatal error has occurred...");
        __current_state = KILL;
        kill();
        break;

      case SD_ERROR:
        close_datastream();
        if(SERIAL_SELECT){ Serial.println("error: a sd card error has occured..."); }
        __current_state = KILL;
        kill_light();
        noInterrupts();
        while(1){ delay(10000); }
        break;

      default: /* all other errors */
        close_datastream();
        log("error: an fatal error has occurred...");
        __current_state = KILL;
        kill();
        break;
    }
  }

  /* enable interrupts */
  if(__enable_sampling){
    if(SERIAL_SELECT) {Serial.println("sampling enabled");}
    Timer1.attachInterrupt(sensor_isr);
    open_datastream();
    __enable_sampling = false;
    __new_data = true;
  }

  /* mode behavior */
  if(__sampling_mode){
    /* allow for sampling BEHAVIOR */
    if(!BUFFER.is_empty()){
      noInterrupts();
      temp_data = BUFFER.remove_front();
      interrupts();

      write_console(temp_data);

      /* DATA TRANSFER */
      // __error = log_payload(temp_data);

    }
  } else {
    /* turn off sensor isr */
    transfer_mode();
  }
}

void transfer_mode(void){
  // turn off the device
  delay(TRANSFER_POLL_TIME);
  if(__current_state == OFFLINE && !__enable_sampling){
    /* check for connection */
    State temp = __current_state;
    __current_state = (XBEE_SELECT && isAnyoneThere())? ONLINE: OFFLINE;
    if(temp != __current_state){
      if(__current_state == ONLINE){ log("state: online"); }
      else { log("state: offline");}
    }

  } else if(__current_state == ONLINE && !__enable_sampling){
    /* start sending data */
    if(__new_data){
      if (SERIAL_SELECT) {Serial.println("attempting data transfer...");}
      __prev_pos = __file_pos;
      __file_pos = write_to_server(__file_pos);
      if(SERIAL_SELECT) {Serial.println(__file_pos);}

      /* prevent device from trying to write */
      if(__prev_pos == __file_pos){
        __new_data = false;
        if(SERIAL_SELECT) {Serial.println("no new data to transfer...");}
      }
    }
  }
}

/*
 * @function:     kill
 *
 * @description:  put the device in an infinite state of waiting and notify
 *                the user that the device should be rebooted or debugged
 */
void kill(void){
  Timer1.detachInterrupt();
  detachInterrupt(BTN_MODE);
  close_datastream();
  log("state: kill");
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
      status[i] =  __imus[i].begin();
      /* initializing components */
      __imus[i].setAccelRange(MPU9250::ACCEL_RANGE_4G);

      out = out && !(status[i] < 0);
      if(trace && (status[i] < 0)){
        log("imu hardware error!");
        log("id: ");
        log(String(i).c_str());
        log("code: ");
        log(String(status[i]).c_str());
      }
    }
  }
  return out;
}

/*
 * @function:     sleepRadio
 *
 * @description:  Turn off the 802.15.4 radio
 */
void sleepRadio(void){
  if(!__radio_sleeping){ digitalWrite(XBEE_SLEEP_PIN, HIGH); }
}

/*
 * @function:     wakeRadio
 *
 * @description:  Turn on the 802.15.4 radio
 */
void wakeRadio(void){
  if(__radio_sleeping){ digitalWrite(XBEE_SLEEP_PIN, LOW); }
}

/*
  Set to sleep:
  PWR_MGMNT_1
  PWR_MGMNT_2
*/
void sleepIMU(void){

}

/*
  Set to wake:
  PWR_MGMNT_1
  PWR_MGMNT_2
*/
void wakeIMU(void){}

/*
 * @function:     btn_isr
 *
 * @description:  function that is triggered when the button changes to HIGH
 *                on the wearable device. this isr will wait for a period of
 *                time, say 10 seconds, and if the button is still high after
 *                that then the device will switch modes.
 *                There are two modes to switch between:
 *                sampling mode: collecting data
 *                transfer mode: transferring data to the network if available
 */
void btn_isr(void){
  // pin should be high
  unsigned value;
  delay(250);
  value = digitalRead(BTN_MODE);
  if(value == 0){ return; } // exit if not 1

  if(__sampling_mode){Timer1.detachInterrupt(); }

  for(unsigned i=0; i < MODE_SW_TO; i+=1000){
    digitalWrite(BUILTIN_LED, HIGH);
    delay(500);
    digitalWrite(BUILTIN_LED, LOW);
    delay(500);
  }
  value = digitalRead(BTN_MODE);
  delay(250);
  /* constant val high -> change modes */
  if(value == 1){
    __sampling_mode = !__sampling_mode;
    close_datastream(); // just in case a file is being written to
    if(__sampling_mode){
      log("switching to: sampling mode");
      __enable_sampling = true;
      // tell system there is more data
      digitalWrite(LED_MODE_STAT, LOW);
      // open_datastream();
      // Timer1.attachInterrupt(sensor_isr);

    } else {
      log("switching to: transfer mode");
      digitalWrite(LED_MODE_STAT, HIGH);
      // Timer1.detachInterrupt(); // already detached for me
    }
  } else if(__sampling_mode){Timer1.attachInterrupt(sensor_isr); } // remove interrupt
  delay(1000); // just in case
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
  // new information set for buffer
  Data packet = {
    {0,0},                        // EMG DATA
    {0,0,0,0,0,0,0,0,0},          // HAND
    {0,0,0,0,0,0,0,0,0},          // THUMB
    {0,0,0,0,0,0,0,0,0},          // POINT
    {0,0,0,0,0,0,0,0,0}           // RING
  };

  if(EMG_SELECT){
    packet.emg[0] = forearm.getRaw();
    packet.emg[1] = forearm.getRect();
  }

  if(HAND_SELECT){
    __imus[0].readSensor();
    // accel
    packet.hand[0] = __imus[0].getAccelX_mss();
    packet.hand[1] = __imus[0].getAccelY_mss(); // getAccelX_mss
    packet.hand[2] = __imus[0].getAccelZ_mss();
    // gyro
    packet.hand[3] = __imus[0].getGyroX_rads();
    packet.hand[4] = __imus[0].getGyroY_rads(); // getGyroX_rads
    packet.hand[5] = __imus[0].getGyroZ_rads();
    // mag
    packet.hand[6] = __imus[0].getMagX_uT();
    packet.hand[7] = __imus[0].getMagY_uT(); // getMagX_uT
    packet.hand[8] = __imus[0].getMagZ_uT();
  }

  if(THUMB_SELECT){
    __imus[3].readSensor();
    // accel
    packet.thumb[0] = __imus[3].getAccelX_mss();
    packet.thumb[1] = __imus[3].getAccelY_mss(); // getAccelX_mss
    packet.thumb[2] = __imus[3].getAccelZ_mss();
    // gyro
    packet.thumb[3] = __imus[3].getGyroX_rads();
    packet.thumb[4] = __imus[3].getGyroY_rads(); // getGyroX_rads
    packet.thumb[5] = __imus[3].getGyroZ_rads();
    // mag
    packet.thumb[6] = __imus[3].getMagX_uT();
    packet.thumb[7] = __imus[3].getMagY_uT(); // getMagX_uT
    packet.thumb[8] = __imus[3].getMagZ_uT();
  }

  if(POINT_SELECT){
    __imus[2].readSensor();
    // accel
    packet.point[0] = __imus[2].getAccelX_mss();
    packet.point[1] = __imus[2].getAccelY_mss(); // getAccelX_mss
    packet.point[2] = __imus[2].getAccelZ_mss();
    // gyro
    packet.point[3] = __imus[2].getGyroX_rads();
    packet.point[4] = __imus[2].getGyroY_rads(); //getGyroX_rads
    packet.point[5] = __imus[2].getGyroZ_rads();
    // mag
    packet.point[6] = __imus[2].getMagX_uT();
    packet.point[7] = __imus[2].getMagY_uT(); // getMagX_uT
    packet.point[8] = __imus[2].getMagZ_uT();
  }

  if(RING_SELECT){
    __imus[1].readSensor();
    // accel
    packet.ring[0] = __imus[1].getAccelX_mss();
    packet.ring[1] = __imus[1].getAccelY_mss(); // getAccelX_mss
    packet.ring[2] = __imus[1].getAccelZ_mss();
    // gyro
    packet.ring[3] = __imus[1].getGyroX_rads();
    packet.ring[4] = __imus[1].getGyroY_rads(); //getGyroX_rads
    packet.ring[5] = __imus[1].getGyroZ_rads();
    // mag
    packet.ring[6] = __imus[1].getMagX_uT();
    packet.ring[7] = __imus[1].getMagY_uT(); // getMagX_uT
    packet.ring[8] = __imus[1].getMagZ_uT();
  }

  if(!BUFFER.push_back(packet)){ __isr_buffer_overflow = true; }
}
