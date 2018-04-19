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
  ----------------------------------------------------------------------------*/
#include "Arduino.h"
#include "../structures/Data.h"
#include <XBee.h>
#include <../sd/SD.h>
#include <SPI.h>
#include <math.h>
#include "../errors.h"

#ifndef COM_H
#define COM_H

/* identification */
extern const uint8_t DEVICE_ID;

/* addressing */
extern const int SERVER_ADDR;
extern const int WEAR_ADDR;

/* hardware variables */
#define HW_TIMEOUT        10000          /* 10000ms : 10 seconds */
#define XBEE_INIT_TIMEOUT 500
#define XBEE_COM_TIMEOUT  10

/* serial information */
#define HWSERIAL    Serial3
#define USB_BAUD    115200
#define RADIO_BAUD  57600
#define MISSED_LIMIT 100

/* pins */
extern const bool SERIAL_SELECT;
extern const bool XBEE_SELECT;
extern const unsigned BUILTIN_LED;        /* builtin led on pin 13 */

/* sd card communication */
const int chip_select = BUILTIN_SDCARD;

/* communication functions */
bool init_com(void);                      /* Initialize Communication Device */
ERROR write_console(Data* src);
ERROR write_radio(Data* src);
bool isAnyoneThere(void);

/* zigbee stack */
int xbee_push();
int xbee_pull();

/* helper functions */
uint16_t pack_float(float src);           /* pack float into 16 bit */

/* sd card functions */
void open_datastream(void);
void close_datastream(void);
void log(const char* msg);
ERROR log_payload(Data* src);

/* VISUAL HARDWARE COMMUNICATION */
void online_light(void);
void offline_light(void);
void search_light(void);
void kill_light(void);

#endif
