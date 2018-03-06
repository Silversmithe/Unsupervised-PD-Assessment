/*------------------------------------------------------------------------------
  file:         com.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  a library of functions that are designed for sending information
                and displaying information to the user. for instance, the device
                needs to be able to transmit data over Serial USB or Xbee to
                the server for future processing. Furthermore, the wearable
                device may want to react to an error by displaying an error
                message or flashing a light indicator.

  note:
                - ehtpr: refers to a boolean buffer containing sensor selection
                         control and the order they come in...
                         e(mg)h(and)t(humb)p(ointer)r(ing)

  ----------------------------------------------------------------------------*/
#include "Arduino.h"
#include "../structures/Data.h"
#include <XBee.h>
#include <math.h>

#ifndef COM_H
#define COM_H

/* serial information */
#define HWSERIAL    Serial3
#define USB_BAUD    115200
#define RADIO_BAUD  9600

/* addressing */
extern const int SRC_XBEE_ADDRESS;
extern const int DEST_XBEE_ADDRESS;

/* pins */
extern const bool SERIAL_SELECT;
extern const bool XBEE_SELECT;
extern const unsigned BUILTIN_LED;   /* builtin led on pin 13 */

/* communication functions */
void init_com();                      /* Initialize Communication Device */
void write_console(Data* src);
void write_radio(Data* src);

/* helper functions */
uint16_t pack_float(float src);       /* pack float into 16 bit */
uint8_t pack_upper_float(float src);  /* pack upper half in 1B */
uint8_t pack_lower_float(float src);  /* pack lower half in 1B */

/* VISUAL HARDWARE COMMUNICATION */
void com_search_light();         /* LED Indicators */

#endif
