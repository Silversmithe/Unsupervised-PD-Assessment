/*------------------------------------------------------------------------------
  file:         analysis.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description: the analysis file contains any algorithms that will be used
               to further process the information being recieved by the
               wearable device. possible transformations of the raw data
               set may include:

               - processing for intelligent power consumption
               - data filtering to extract data
               - device health
   ---------------------------------------------------------------------------*/
#include "analysis.h"

/*
  @description:   takes the stored variable Q, which has been updated with the
                  most recently calculated quaternion coordinates and uses the
                  coordinates to calculate the pitch of the measured IMU.

                  Calculation brought to you by:
                  http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
*/
inline float to_pitch(){
  return atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
         *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
         - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
}

/*
  @description:   takes the stored variable Q, which has been updated with the
                  most recently calculated quaternion coordinates and uses the
                  coordinates to calculate the yaw of the measured IMU.

                  Calculation brought to you by:
                  http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
*/
inline float to_yaw(){
  return -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() * *(getQ()+2)));
}

/*
  @description:   takes the stored variable Q, which has been updated with the
                  most recently calculated quaternion coordinates and uses the
                  coordinates to calculate the roll of the measured IMU.

                  Calculation brought to you by:
                  http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
*/
inline float to_roll(){
  return atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
         *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
         - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));
}

/*
  @param: (Data *) item: a pointer to a data structure to calculate orientation
                         data for
  @param: (bool) hand: determine if the hand IMU pos should be calculated
  @param: (bool) thumb: determine if the thumb IMU pos should be calculated
  @param: (bool) point: determine if the point IMU pos should be calculated
  @param: (bool) ring: determine if the ring IMU pos should be calculated

  @description: given a data point, pass the selected imu sensors through a
                mahony filter to produce quick, but accurate estimations of
                orientation in the quaternion coordinate system. then, take
                those quaternion coordinates and convert them to roll, pitch,
                and yaw for processing.
*/
void orient(Data* item, bool hand, bool thumb, bool point, bool ring){
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

  if(hand){
    MahonyQuaternionUpdate(item->hand[0], item->hand[1], item->hand[2],
                           item->hand[3], item->hand[4], item->hand[5],
                           item->hand[6], item->hand[7], item->hand[8],
                           item->hand[9]);

    item->hand_pos[0] = to_pitch();
    item->hand_pos[1] = to_roll();
    item->hand_pos[2] = to_yaw();
  }

  if(thumb){
    MahonyQuaternionUpdate(item->thumb[0], item->thumb[1], item->thumb[2],
                          item->thumb[3], item->thumb[4], item->thumb[5],
                          item->thumb[6], item->thumb[7], item->thumb[8],
                          item->thumb[9]);

    item->thumb_pos[0] = to_pitch();
    item->thumb_pos[1] = to_roll();
    item->thumb_pos[2] = to_yaw();
  }

  if(point){
    MahonyQuaternionUpdate(item->point[0], item->point[1], item->point[2],
                           item->point[3], item->point[4], item->point[5],
                           item->point[6], item->point[7], item->point[8],
                           item->point[9]);

    item->point_pos[0] = to_pitch();
    item->point_pos[1] = to_roll();
    item->point_pos[2] = to_yaw();
  }

  if(ring){
    MahonyQuaternionUpdate(item->ring[0], item->ring[1], item->ring[2],
                          item->ring[3], item->ring[4], item->ring[5],
                          item->ring[6], item->ring[7], item->ring[8],
                          item->ring[9]);

    item->ring_pos[0] = to_pitch();
    item->ring_pos[1] = to_roll();
    item->ring_pos[2] = to_yaw();
  }
}
