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
                IMU_ERROR                 Any issue reguarding the control of
                                          the IMU including communication,
                                          reading, data quality.

                EMG_ERROR                 issues reguarding the control and use
                                          of the EMG including communication,
                                          reading, and data quality

                ISOLATED_DEVICE_ERROR     issues reguarding the complete
                                          disconnection of the wearable from
                                          the server

                ZIGBEE_ERROR              issues reguarding the control and use
                                          of the Xbee, including device
                                          communication server communication,
                                          data quality, data loss

                SERIAL_ERROR              issues reguarding the control and use
                                          of the Serial connection between the
                                          computer and the wearable device

                BUFFER_OVERFLOW           issues reguarding the use and
                                          functionality of the RAM buffer on
                                          the device.

                EXTERAL_MEMORY_OVERFLOW   issues reguarding the use and
                                          functionality of the external storage
                                          device on the wearable device
  ----------------------------------------------------------------------------*/
#ifndef ERRORS_H
#define ERRORS_H

enum ERROR {
  /* SENSOR ERRORS */
  IMU_ERROR,
  EMG_ERROR,
  /* COMMUNICATION ERRORS */
  ISOLATED_DEVICE_ERROR,
  ZIGBEE_ERROR,
  SERIAL_ERROR,
  /* MEMORY ERRORS */
  BUFFER_OVERFLOW,
  EXTERAL_MEMORY_OVERFLOW
};

#endif
