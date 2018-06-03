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

      // write_console(temp_data);

      /* DATA TRANSFER */
      __error = log_payload(temp_data);

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
  if(HAND_SELECT){
    Hand.MPU9250SelfTest(Hand.SelfTest);
    Hand.calibrateMPU9250(Hand.gyroBias, Hand.accelBias);
    Hand.initAK8963(Hand.magCalibration);
  }

  if(THUMB_SELECT){
    Thumb.MPU9250SelfTest(Thumb.SelfTest);
    Thumb.calibrateMPU9250(Thumb.gyroBias, Thumb.accelBias);
    Thumb.initAK8963(Thumb.magCalibration);
  }

  if(POINT_SELECT){
    Point.MPU9250SelfTest(Point.SelfTest);
    Point.calibrateMPU9250(Point.gyroBias, Point.accelBias);
    Point.initAK8963(Point.magCalibration);
  }

  if(RING_SELECT){
    Ring.MPU9250SelfTest(Ring.SelfTest);
    Ring.calibrateMPU9250(Ring.gyroBias, Ring.accelBias);
    Ring.initAK8963(Ring.magCalibration);
  }

  return true;
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
    Hand.readAccelData(Hand.accelCount);  // Read the x/y/z adc values
    Hand.getAres();
    Hand.readAccelData(Hand.accelCount);  // Read the x/y/z adc values

    Hand.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    Hand.ax = (float)Hand.accelCount[0]*Hand.aRes; // - accelBias[0];
    Hand.ay = (float)Hand.accelCount[1]*Hand.aRes; // - accelBias[1];
    Hand.az = (float)Hand.accelCount[2]*Hand.aRes; // - accelBias[2];

    Hand.readGyroData(Hand.gyroCount);  // Read the x/y/z adc values
    Hand.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    Hand.gx = (float)Hand.gyroCount[0]*Hand.gRes;
    Hand.gy = (float)Hand.gyroCount[1]*Hand.gRes;
    Hand.gz = (float)Hand.gyroCount[2]*Hand.gRes;

    Hand.readMagData(Hand.magCount);  // Read the x/y/z adc values
    Hand.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    Hand.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    Hand.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    Hand.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    Hand.mx = (float)Hand.magCount[0]*Hand.mRes*Hand.magCalibration[0] -
               Hand.magbias[0];
    Hand.my = (float)Hand.magCount[1]*Hand.mRes*Hand.magCalibration[1] -
               Hand.magbias[1];
    Hand.mz = (float)Hand.magCount[2]*Hand.mRes*Hand.magCalibration[2] -
    Hand.magbias[2];

    // accel
    packet.hand[0] = Hand.ax;
    packet.hand[1] = Hand.ay; // getAccelX_mss
    packet.hand[2] = Hand.az;
    // gyro
    packet.hand[3] = Hand.gx;
    packet.hand[4] = Hand.gy; // getGyroX_rads
    packet.hand[5] = Hand.gz;
    // mag
    packet.hand[6] = Hand.mx;
    packet.hand[7] = Hand.my; // getMagX_uT
    packet.hand[8] = Hand.mz;
  }

  if(THUMB_SELECT){
    Thumb.readAccelData(Thumb.accelCount);  // Read the x/y/z adc values
    Thumb.getAres();
    Thumb.readAccelData(Thumb.accelCount);  // Read the x/y/z adc values

    Thumb.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    Thumb.ax = (float)Thumb.accelCount[0]*Thumb.aRes; // - accelBias[0];
    Thumb.ay = (float)Thumb.accelCount[1]*Thumb.aRes; // - accelBias[1];
    Thumb.az = (float)Thumb.accelCount[2]*Thumb.aRes; // - accelBias[2];

    Thumb.readGyroData(Thumb.gyroCount);  // Read the x/y/z adc values
    Thumb.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    Thumb.gx = (float)Thumb.gyroCount[0]*Thumb.gRes;
    Thumb.gy = (float)Thumb.gyroCount[1]*Thumb.gRes;
    Thumb.gz = (float)Thumb.gyroCount[2]*Thumb.gRes;

    Thumb.readMagData(Thumb.magCount);  // Read the x/y/z adc values
    Thumb.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    Thumb.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    Thumb.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    Thumb.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    Thumb.mx = (float)Thumb.magCount[0]*Thumb.mRes*Thumb.magCalibration[0] -
               Thumb.magbias[0];
    Thumb.my = (float)Thumb.magCount[1]*Thumb.mRes*Thumb.magCalibration[1] -
               Thumb.magbias[1];
    Thumb.mz = (float)Thumb.magCount[2]*Thumb.mRes*Thumb.magCalibration[2] -
    Thumb.magbias[2];

    // accel
    packet.thumb[0] = Thumb.ax;
    packet.thumb[1] = Thumb.ay; // getAccelX_mss
    packet.thumb[2] = Thumb.az;
    // gyro
    packet.thumb[3] = Thumb.gx;
    packet.thumb[4] = Thumb.gy; // getGyroX_rads
    packet.thumb[5] = Thumb.gz;
    // mag
    packet.thumb[6] = Thumb.mx;
    packet.thumb[7] = Thumb.my; // getMagX_uT
    packet.thumb[8] = Thumb.mz;
  }

  if(POINT_SELECT){
    Point.readAccelData(Point.accelCount);  // Read the x/y/z adc values
    Point.getAres();
    Point.readAccelData(Point.accelCount);  // Read the x/y/z adc values

    Point.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    Point.ax = (float)Point.accelCount[0]*Point.aRes; // - accelBias[0];
    Point.ay = (float)Point.accelCount[1]*Point.aRes; // - accelBias[1];
    Point.az = (float)Point.accelCount[2]*Point.aRes; // - accelBias[2];

    Point.readGyroData(Point.gyroCount);  // Read the x/y/z adc values
    Point.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    Point.gx = (float)Point.gyroCount[0]*Point.gRes;
    Point.gy = (float)Point.gyroCount[1]*Point.gRes;
    Point.gz = (float)Point.gyroCount[2]*Point.gRes;

    Point.readMagData(Point.magCount);  // Read the x/y/z adc values
    Point.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    Point.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    Point.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    Point.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    Point.mx = (float)Point.magCount[0]*Point.mRes*Point.magCalibration[0] -
               Point.magbias[0];
    Point.my = (float)Point.magCount[1]*Point.mRes*Point.magCalibration[1] -
               Point.magbias[1];
    Point.mz = (float)Point.magCount[2]*Point.mRes*Point.magCalibration[2] -
    Point.magbias[2];

    // accel
    packet.point[0] = Point.ax;
    packet.point[1] = Point.ay; // getAccelX_mss
    packet.point[2] = Point.az;
    // gyro
    packet.point[3] = Point.gx;
    packet.point[4] = Point.gy; // getGyroX_rads
    packet.point[5] = Point.gz;
    // mag
    packet.point[6] = Point.mx;
    packet.point[7] = Point.my; // getMagX_uT
    packet.point[8] = Point.mz;
  }

  if(RING_SELECT){
    Ring.readAccelData(Ring.accelCount);  // Read the x/y/z adc values
    Ring.getAres();
    Ring.readAccelData(Ring.accelCount);  // Read the x/y/z adc values

    Ring.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    Ring.ax = (float)Ring.accelCount[0]*Ring.aRes; // - accelBias[0];
    Ring.ay = (float)Ring.accelCount[1]*Ring.aRes; // - accelBias[1];
    Ring.az = (float)Ring.accelCount[2]*Ring.aRes; // - accelBias[2];

    Ring.readGyroData(Ring.gyroCount);  // Read the x/y/z adc values
    Ring.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    Ring.gx = (float)Ring.gyroCount[0]*Ring.gRes;
    Ring.gy = (float)Ring.gyroCount[1]*Ring.gRes;
    Ring.gz = (float)Ring.gyroCount[2]*Ring.gRes;

    Ring.readMagData(Ring.magCount);  // Read the x/y/z adc values
    Ring.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    Ring.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    Ring.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    Ring.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    Ring.mx = (float)Ring.magCount[0]*Ring.mRes*Ring.magCalibration[0] -
               Ring.magbias[0];
    Ring.my = (float)Ring.magCount[1]*Ring.mRes*Ring.magCalibration[1] -
               Ring.magbias[1];
    Ring.mz = (float)Ring.magCount[2]*Ring.mRes*Ring.magCalibration[2] -
    Ring.magbias[2];

    // accel
    packet.ring[0] = Ring.ax;
    packet.ring[1] = Ring.ay; // getAccelX_mss
    packet.ring[2] = Ring.az;
    // gyro
    packet.ring[3] = Ring.gx;
    packet.ring[4] = Ring.gy; // getGyroX_rads
    packet.ring[5] = Ring.gz;
    // mag
    packet.ring[6] = Ring.mx;
    packet.ring[7] = Ring.my; // getMagX_uT
    packet.ring[8] = Ring.mz;
  }

  if(!BUFFER.push_back(packet)){ __isr_buffer_overflow = true; }
}
