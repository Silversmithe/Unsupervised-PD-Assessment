/*------------------------------------------------------------------------------
  file:         errors.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  Contains a list of different errors that could potentially show
                up during the runtime of the program. Based on these error
                messages, the device should be able to either recover or shut
                down accordingly
                This file will also be in control of error handling if such a
                thing is possible.

  errors:
                NONE                      No error exists

                IMU_ERROR                 Any issue reguarding the control of
                                          the IMU including communication,
                                          reading, data quality.

                EMG_ERROR                 issues reguarding the control and use
                                          of the EMG including communication,
                                          reading, and data quality

                ISOLATED_DEVICE_ERROR     issues reguarding the complete
                                          disconnection of the wearable from
                                          the server

                BUFFER_OVERFLOW           issues reguarding the use and
                                          functionality of the RAM buffer on
                                          the device.

                SD_ERROR                  Error recording information on the sd
                                          device

                FATAL_ERROR               Errors that cannot be recovered from
                                          Usually happens when there is another
                                          error in an uncompromising state
  ----------------------------------------------------------------------------*/
#ifndef ERRORS_H
#define ERRORS_H

enum ERROR {
  NONE,
  /* NEEDS TO KILL */
  FATAL_ERROR,
  /* SENSOR ERRORS */
  IMU_ERROR,
  EMG_ERROR,
  /* COMMUNICATION ERRORS */
  ISOLATED_DEVICE_ERROR,
  /* MEMORY ERRORS */
  BUFFER_OVERFLOW,
  /* SD CARD ERRORS */
  SD_ERROR,
};

#endif
