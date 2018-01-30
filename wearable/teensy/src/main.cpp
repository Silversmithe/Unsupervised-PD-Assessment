/*
--------------------------------------------------------------------------------
  main.cpp (Wearable Version 1: IRON FIST)

  Main Application for gathering and reporting information of both sensors in
  one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.

  Alexander S. Adranly
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
MPU9250 dhand_imu(Wire1, IMU_ADDR_HI);
MPU9250 rfinger_imu(Wire1, IMU_ADDR_LO);

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
  Timer1.initialize(FULL_SAMPLE_RATE); // DEMO_RATE FULL_SAMPLE_RATE DOUBLE_SAMPLE_RATE
  Timer1.attachInterrupt(sensor_isr);

  current_time = micros();            // initialize timer
}

/* MAIN LOOP */
void loop() {
  /* consumer of the IOBuffer */
  if(!BUFFER.is_empty()){
    // remove a Data item from buffer
    Data* data = BUFFER.remove_front();
    // convert Data into PAYLOAD

    /* BUFFER TESTING */
    // send payload over communication medium
    // print data from buffers
    serial_print_data(data);
  }

  delay(10);
}

/* FUNCTIONS */
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

void get_orientation(Data* item){
// Define output variables from updated quaternion---these are Tait-Bryan
// angles, commonly used in aircraft orientation. In this coordinate system,
// the positive z-axis is down toward Earth. Yaw is the angle between Sensor
// x-axis and Earth magnetic North (or true North if corrected for local
// declination, looking down on the sensor positive yaw is counterclockwise.
// Pitch is angle between sensor x-axis and Earth ground plane, toward the
// Earth is positive, up toward the sky is negative. Roll is angle between
// sensor y-axis and Earth ground plane, y-axis up is positive roll. These
// arise from the definition of the homogeneous rotation matrix constructed
// from quaternions. Tait-Bryan angles as well as Euler angles are
// non-commutative; that is, the get the correct orientation the rotations
// must be applied in the correct order which for this configuration is yaw,
// pitch, and then roll.
// For more see
// http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
// which has additional links.

// hand
MahonyQuaternionUpdate(item->hand[0], item->hand[1], item->hand[2], // Axyz
                       item->hand[3], item->hand[4], item->hand[5], // Gxyz
                       item->hand[6], item->hand[7], item->hand[8], // Mxyz
                       item->hand[9]);                              // dT

// pitch
item->hand_pos[0] = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                 *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
                 - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
// roll
item->hand_pos[1] = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                   *(getQ()+2)));

// yaw
item->hand_pos[2] = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                 *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
                 - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));


// thumb
MahonyQuaternionUpdate(item->thumb[0], item->thumb[1], item->thumb[2], // Axyz
                      item->thumb[3], item->thumb[4], item->thumb[5], // Gxyz
                      item->thumb[6], item->thumb[7], item->thumb[8], // Mxyz
                      item->thumb[9]);                              // dT

// pitch
item->thumb_pos[0] = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                  *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
                  - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
// roll
item->thumb_pos[1] = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                    *(getQ()+2)));

// yaw
item->thumb_pos[2] = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                  *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
                  - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));

// point
MahonyQuaternionUpdate(item->point[0], item->point[1], item->point[2], // Axyz
                       item->point[3], item->point[4], item->point[5], // Gxyz
                       item->point[6], item->point[7], item->point[8], // Mxyz
                       item->point[9]);                              // dT

// pitch
item->point_pos[0] = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                 *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
                 - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
// roll
item->point_pos[1] = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                   *(getQ()+2)));

// yaw
item->point_pos[2] = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                 *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
                 - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));

// ring
MahonyQuaternionUpdate(item->ring[0], item->ring[1], item->ring[2], // Axyz
                      item->ring[3], item->ring[4], item->ring[5], // Gxyz
                      item->ring[6], item->ring[7], item->ring[8], // Mxyz
                      item->ring[9]);                              // dT

// pitch
item->ring_pos[0] = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                  *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
                  - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
// roll
item->ring_pos[1] = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                    *(getQ()+2)));

// yaw
item->ring_pos[2] = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                  *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
                  - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));

}

void serial_print_data(Data* src){
  /*
    Print Data over Serial
  */
  if(!SERIAL_SELECT){ return; }
  else{
    // display information
    // time
    Serial.print(src->dt);
    Serial.print("\t");

    if(EMG_SELECT){
      for(int i=0; i<2; i++){
        Serial.print(src->emg[i]);
        Serial.print("\t");
      }
    } // end EMG
    if(HAND_SELECT){
      for(int i=0; i<6; i++){
        Serial.print(src->hand[i]);
        Serial.print("\t");
      }
    } // end hand
    if(THUMB_SELECT){
      for(int i=0; i<6; i++){
        Serial.print(src->thumb[i]);
        Serial.print("\t");
      }
    } // end thumb
    if(POINT_SELECT){
      for(int i=0; i<6; i++){
        Serial.print(src->point[i]);
        Serial.print("\t");
      }
    }// end point
    if(RING_SELECT){
      for(int i=0; i<6; i++){
        Serial.print(src->ring[i]);
        Serial.print("\t");
      }
    } // end ring
    Serial.println("");
  }
}

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
