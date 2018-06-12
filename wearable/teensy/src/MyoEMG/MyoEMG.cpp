/*------------------------------------------------------------------------------
  file:         MyoEMG.cpp

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  A wrapper data structure to represent the EMG sensor attached
                to the wearable device. responsible for keeping track of which
                pins the device is attached to, which pin allows the device
                to read raw data, and which pin allows the device to read
                rectified data.
  ----------------------------------------------------------------------------*/
#include "Arduino.h"
#include "stdint.h"
#include "MyoEMG.h"

/*
 * @function:        EMG::EMG
 *
 * @param:           (uint8_t) prect: analog GPIO pin that will read the rectified and
 *                                     integrated signal
 * @param:           (uint8_t) praw: analog GPIO pin that will read the raw emg signal
 *
 * @description:     constructor for the emg class, allows the user to specify
 *                   both the raw pin and the rectified pin although both may not
 *                   be used. However, it is mandatory for the user to specify a
 *                   rectified pin at list. The constructor just stores the data
 *                   for future collection
 */
EMG::EMG(uint8_t prect, uint8_t praw):
  raw_pin(praw),
  rect_pin(prect)
{}

/*
 * @function:      EMG::getRaw
 *
 * @description:   Function that polls the raw emg signal for the instantaneous value
 *
 * @return:        (int16_t) raw emg signal
 */
int16_t EMG::getRaw(void){ return analogRead(raw_pin); }

/*
 * @function:         EMG::getRect
 *
 * @description:      Function that polls rectified and integrated emg signal for the
 *                    instantaneous value
 *
 * @return:           (int16_t) rectified and integrated emg signal
 */
int16_t EMG::getRect(void){ return analogRead(rect_pin); }
