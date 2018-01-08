/*
  ------------------------------------------------------------------------------
  main.cpp

  Alexander S. Adranly
  December 31st, 2017
  ------------------------------------------------------------------------------
  Driver program, change main code to select unittests or running the main
  program
  ------------------------------------------------------------------------------
*/
#include "Arduino.h"
#include "stdint.h"
#include "MPU9250/MPU9250.h"     // @Make a better version for the project
#include "MyoEMG/MyoEMG.h"       // Simple EMG Library
#include "TimerOne.h"            // timer & interrupt library
#include "Packet.h"              // packets to transfer information

/* GLOBAL VARIALBES */
// SYSTEM LOGISTICS
#define VERSION         1.0     // VERSION number
#define MODE            0x03    // defines code to run (codes in unittest.h)
#define DEBUG           true    // defines debug state
#define BAUD_RATE       115200  // baud rate of the serial connection
#define ISR_TIMEOUT     200     // timeout rate for ISR (to read sensors)
#define BUFFER_SIZE     200     // buffer size for the packet io buffer
// ADDRESSES
#define IMU_ADDR_LO     0x68  // lower imu address on bus
#define IMU_ADDR_HI     0x69  // higher imu address on bus
// PINS
#define ERROR_LIGHT     13    // error light
#define EMG_RAW_PIN     13    // pin on teensy for raw emg (ANALOG)
#define EMG_REC_PIN     12    // pin on teensy for rectified emg (ANALOG)
// CONTAINERS
PACKET* TEMP;                 // temporary packet pointer to read from
PACKET* BUFFER;      // IO buffer to transfer information QUEUE
int buffer_front = 0;         // keeps track of the buffer
int buffer_back = 0;          // keeps track of the buffer

/* MODE SELECTION */
#if MODE != 0x00
  #include "unittest/unittest.h"
#endif
#if MODE == 0x00
  // IMU Devices
  MPU9250 IMUPointer(Wire, IMU_ADDR_LO);            // pointer finger
  MPU9250 IMUThumb(Wire, IMU_ADDR_HI);              // thumb finger
  MPU9250 IMURing(Wire1, IMU_ADDR_LO);              // ring finger
  MPU9250 IMUHandDorsum(Wire1, IMU_ADDR_HI);        // back of palm
  // EMG Sensor
  EMG EMGForearm(EMG_REC_PIN, EMG_RAW_PIN);         // EMG signal
#endif

/* FUNCTION PROTOTYPES */
// sensor
void total_sensor_scan();  // interrupt routine to gather sensor data
// error handling
bool die();                // graceful death of program
bool reset();              // attempted recovery of the wearable program
void error_signal();       // display an error light

/* MAIN FUNCTIONS */
void setup() {
  /* MAIN SETUP */
  /* ADJUST BASED ON MODE */
  #if MODE != 0x00
    unittest_runner(MODE);        // hand off to unit tester
  #else
    /* MAIN SETUP CODE */
    pinMode(ERROR_LIGHT, OUTPUT);       // initialize error light

    // Buffer Setup
    BUFFER = new PACKET[BUFFER_SIZE](); // buffer packet
    for(int i=0; i<BUFFER_SIZE; i++){
      // Container setup
      BUFFER[i].thumb_gyro = new int16_t[3];
      BUFFER[i].pointer_gyro = new int16_t[3];
      BUFFER[i].ring_gyro = new int16_t[3];
      BUFFER[i].hand_gyro = new int16_t[3];
      BUFFER[i].hand_accel = new int16_t[3];
      BUFFER[i].emg_sig = new int16_t[2];
    } // end loop

    // Setup Variables
    int status[4] = {0, 0, 0, 0};       // startup status of the imus

    /* INITIALIZE IMUS */
    status[0] = IMUThumb.begin();
    status[1] = IMUPointer.begin();
    status[2] = IMURing.begin();
    status[3] = IMUHandDorsum.begin();

    // check for any invalid startups & show error light on error
    if(status[0] + status[1] + status[2] + status[3] != 0){ error_signal(); }

    // Timer Variable Arbitrary time at the moment
    Timer1.initialize(ISR_TIMEOUT);             // set a timer frequency
    Timer1.attachInterrupt(total_sensor_scan);  // attached sensor scan
    noInterrupts();                      // prevent timer until start

    Serial.begin(BAUD_RATE);      // INITIALIZE SERIAL MONITOR
    while(!Serial){}              // wait for serial monitor

    interrupts();          // start the timer
  #endif
}

void loop() {
  /* MAIN LOOP */
  // display information via serial
  #if MODE == 0x00
    if(buffer_front < buffer_back){
      // increment the front buffer to consume that item in the queue
      noInterrupts();
      TEMP = &BUFFER[buffer_front];  // must take pointer for future use
      interrupts();
      buffer_front = (buffer_front + 1) % BUFFER_SIZE;
      // display information
      Serial.print("EMG: raw:");
      Serial.print(TEMP->emg_sig[0]);
      Serial.print(", rect: ");
      Serial.println(TEMP->emg_sig[1]);

      Serial.print("Thumb Gyro: x: ");
      Serial.print(TEMP->thumb_gyro[0]);
      Serial.print(", y:");
      Serial.print(TEMP->thumb_gyro[1]);
      Serial.print(", z:");
      Serial.println(TEMP->thumb_gyro[2]);

      Serial.print("Pointer Gyro: x: ");
      Serial.print(TEMP->pointer_gyro[0]);
      Serial.print(", y:");
      Serial.print(TEMP->pointer_gyro[1]);
      Serial.print(", z:");
      Serial.println(TEMP->pointer_gyro[2]);

      Serial.print("Ring Gyro: x: ");
      Serial.print(TEMP->ring_gyro[0]);
      Serial.print(", y:");
      Serial.print(TEMP->ring_gyro[1]);
      Serial.print(", z:");
      Serial.println(TEMP->ring_gyro[2]);

      Serial.print("Hand Gyro: x: ");
      Serial.print(TEMP->hand_gyro[0]);
      Serial.print(", y:");
      Serial.print(TEMP->hand_gyro[1]);
      Serial.print(", z:");
      Serial.println(TEMP->hand_gyro[2]);

      Serial.print("Hand Accel: x: ");
      Serial.print(TEMP->hand_accel[0]);
      Serial.print(", y:");
      Serial.print(TEMP->hand_accel[1]);
      Serial.print(", z:");
      Serial.println(TEMP->hand_accel[2]);
      Serial.println("---------------------");

    }
    delay(100);       // should be consuming faster than producing
  #endif
}

// functions are only defined if the mode is in MAIN MODE
#if MODE == 0x00
//------------------------------------------------------------------------------
//                              SENSOR FUNCTIONS
//------------------------------------------------------------------------------
void total_sensor_scan(){
/*
  Gather all the sensor information from the EMG and IMUS and store it in a
  struct for future work. Store the information in the buffer.

*/
  buffer_back = (buffer_back + 1) % BUFFER_SIZE; // increment back pointer
  // IMU Trigger Sensor Read
  IMUThumb.readSensor();
  IMUPointer.readSensor();
  IMURing.readSensor();
  IMUHandDorsum.readSensor();
  // EMG
  BUFFER[buffer_back].emg_sig[0] = EMGForearm.getRaw();
  BUFFER[buffer_back].emg_sig[1] = EMGForearm.getRect();
  // Store thumb
  BUFFER[buffer_back].thumb_gyro[0] = IMUThumb.getGyroX_rads();
  BUFFER[buffer_back].thumb_gyro[1] = IMUThumb.getGyroY_rads();
  BUFFER[buffer_back].thumb_gyro[2] = IMUThumb.getGyroZ_rads();
  // store pointer
  BUFFER[buffer_back].pointer_gyro[0] = IMUPointer.getGyroX_rads();
  BUFFER[buffer_back].pointer_gyro[1] = IMUPointer.getGyroY_rads();
  BUFFER[buffer_back].pointer_gyro[2] = IMUPointer.getGyroZ_rads();
  // store ring
  BUFFER[buffer_back].ring_gyro[0] = IMURing.getGyroX_rads();
  BUFFER[buffer_back].ring_gyro[1] = IMURing.getGyroY_rads();
  BUFFER[buffer_back].ring_gyro[2] = IMURing.getGyroZ_rads();
  // store hand gyro
  BUFFER[buffer_back].hand_gyro[0] = IMUHandDorsum.getGyroX_rads();
  BUFFER[buffer_back].hand_gyro[1] = IMUHandDorsum.getGyroY_rads();
  BUFFER[buffer_back].hand_gyro[2] = IMUHandDorsum.getGyroZ_rads();
  // hand accel
  BUFFER[buffer_back].hand_accel[0] = IMUHandDorsum.getGyroX_rads();
  BUFFER[buffer_back].hand_accel[1] = IMUHandDorsum.getGyroY_rads();
  BUFFER[buffer_back].hand_accel[2] = IMUHandDorsum.getGyroZ_rads();
}

//------------------------------------------------------------------------------
//                              ERROR RECOVERY FUNCTIONS
//------------------------------------------------------------------------------
bool die(){
/*
  Upon any critical errors have the wearable device shut down all of its
  peripheral devices so that the device can be repaired. This code handles the
  shutdown of any main code failures, not for any of the unittests.

  @return: (bool) success or failure of the device to shut down all peripherals
                  properly
*/
// turn off interrupts
noInterrupts();
// shut down all sensors
// make the imus go to sleep

// shut down serial monitor
Serial.end();

// deallocate all Variables

// Destroying buffer variable
for(int i=0; i<BUFFER_SIZE; i++){
  delete[] BUFFER[i].thumb_gyro;
  delete[] BUFFER[i].pointer_gyro;
  delete[] BUFFER[i].ring_gyro;
  delete[] BUFFER[i].hand_gyro;
  delete[] BUFFER[i].hand_accel;
  delete[] BUFFER[i].emg_sig;
}
delete[] BUFFER;

return true;
}

bool reset(){
  /*
    Upon any minor errors have the wearable device reset all of its
    peripheral devices so that the device can attemt to self-recover.
    This code is meant for handling the main program peripherals, NOT the
    unit tests

    @return: (bool) success or failure of the device to reset all peripherals
                    properly
  */
  noInterrupts();          // turn off interrupts

  // reset sensors

  // reset serial MONITOR
  Serial.end();
  delay(1000);             // wait a second for the computer to calm down
  Serial.begin(BAUD_RATE); // restart the serial monitor at the desired BAUD
  interrupts();            // turn on inerrupts
  return true;
}

void error_signal(){
  /*
    Display a blinking light built into the teensy if the device is not running
    properly
  */
  while(1){
    digitalWrite(ERROR_LIGHT, HIGH);
    delay(1000);
    digitalWrite(ERROR_LIGHT, LOW);
    delay(1000);
  } // end while
}

#endif
