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
#include <../sd/SD.h>
#include <SPI.h>
#include <math.h>

#ifndef COM_H
#define COM_H

/* hardware variables */
#define HW_TIMEOUT        10000          /* 10000ms : 10 seconds */
#define XBEE_INIT_TIMEOUT 5000
#define XBEE_COM_TIMEOUT  10

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
bool init_com();                      /* Initialize Communication Device */
void write_console(Data* src);
void write_radio(Data* src);
bool isAnyoneThere();

/* helper functions */
uint16_t pack_float(float src);       /* pack float into 16 bit */

/* VISUAL HARDWARE COMMUNICATION */
void search_light();
void kill_light();

#endif
