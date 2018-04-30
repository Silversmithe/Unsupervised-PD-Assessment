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
#include "../sd/SD.h"
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
#define HW_TIMEOUT        5000          /* 10000ms : 10 seconds */
#define XBEE_INIT_TIMEOUT 500
#define XBEE_COM_TIMEOUT  10

/* serial information */
#define HWSERIAL     Serial3
#define USB_BAUD     115200
#define RADIO_BAUD   38400  // 57600
#define MISSED_LIMIT 100

/* buffer variables */
#define FILE_BUFFER  300

/* radio information */
#define PAYLOAD_SIZE 100
#define TX_STAT_WAIT 100

/* communication protocol variables */
/* should have a byte for identifying the message type */
// new_datafile
// continue_datafile
// sample/payload
// broadcast
const uint8_t BROADCAST     = 0x01;   // tell the server you are here
const uint8_t NEW_DATA      = 0x02;   // signify server to create new file
const uint8_t CONTINUE_DATA = 0x03;   // if not all data in segment transferred
const uint8_t PAYLOAD       = 0x04;
static uint8_t __packet_id;           // modulo 100

/* pins */
extern const bool SERIAL_SELECT;
extern const bool XBEE_SELECT;
extern const unsigned BUILTIN_LED;        /* builtin led on pin 13 */
extern const unsigned LED_MODE_STAT;      /* for controlling mode */

/* sd card communication */
const int chip_select = BUILTIN_SDCARD;

/* communication functions */
bool init_com(bool erase);                 /* Initialize Communication Device */
ERROR write_console(Data* src);

/* sending data */
uint32_t write_to_server(uint32_t pos);
ERROR write_radio(Data* src);
bool isAnyoneThere(void);

/* helper functions */
uint16_t float_to_halfword(float src);
/* read line of current file */
unsigned read_line(uint8_t* buffer);
/* parse buffer and create packet*/
bool parse_line(unsigned& size, uint8_t* buffer, Data* store);
bool match(unsigned& index, uint8_t* buffer, uint8_t val);

/* sd card functions */
void open_datastream(void);
void close_datastream(void);
bool clear_datastream(void);
void log(const char* msg);
ERROR log_payload(Data* src);

/* VISUAL HARDWARE COMMUNICATION */
void transfer_mode_light(void);
void online_light(void);
void offline_light(void);
void search_light(void);
void kill_light(void);

#endif
