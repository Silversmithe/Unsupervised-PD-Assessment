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
#include "Xbee.h"
#include "../structures/Data.h"

#ifndef COM_H
#define COM_H

/* Initialize Communication Device */
void init_com(int sselect, int sxbee); 
/* Serial */
void send_to_console(Data* src, bool* ehtpr);
/* Xbee */
void send_to_radio(Data* src, bool* ehtpr);
/* LED Indicators */
void com_search_light(int led);         // if device is searching for com device

#endif
