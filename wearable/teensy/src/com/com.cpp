/*------------------------------------------------------------------------------
  file:         com.cpp

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  a library of functions that are designed for sending information
                and displaying information to the user. for instance, the device
                needs to be able to transmit data over Serial USB or Xbee to
                the server for future processing. Furthermore, the wearable
                device may want to react to an error by displaying an error
                message or flashing a light indicator.
  ----------------------------------------------------------------------------*/
#include "com.h"

/*
  @param: (int) sselect: variable to discern if the wearable device should be
                         attempting to connect via a USB serial connection
  @param: (int) sxbee:   variable to discern if the wearable device should be
                         attempting to connect via a Xbee radio connection

  @description:          the function attempts to connect the wearable device
                         with the chosen method of communication and will react
                         accordingly if unable to do so
*/
void init_com(int sselect, int sxbee){
  if(sselect){
    // connect with the Serial USB connection
  } else if (sxbee){
    // connect with the Xbee
  } else {
    // throw an error
    // no communication medium selected
    // panic
  } // endif
}

/*
  @param: (Data*) src:    the data point that contains all the information for one
                          instance of data collection
  @param: (bool*) ehtpr:  an array of boolean variables that specifies which of
                          the following sensors should and should not be read

  @description:           this function will transfer the following medical data
                          over the USB serial medium and handle all situations
                          in terms of communication of this message
*/
void send_to_console(Data* src, bool* ehtpr){
  /*
    Print Data over Serial
  */

}

/*
  @param: (Data*) src:    the data point that contains all the information for one
                          instance of data collection
  @param: (bool*) ehtpr:  an array of boolean variables that specifies which of
                          the following sensors should and should not be read

  @description:           this function will transfer the following medical data
                          over the Xbee serial medium and handle all situations
                          in terms of communication of this message
*/
void send_to_radio(Data* src, bool* ehtpr){
  /* work on this later */

}

/*
  @param: (int) led: the digital io pin to control an LED

  @description:      command the specified LED to output this particular pattern
                     to signal to the user that the device is searching for a
                     communication medium to connect and use
*/
void com_search_light(int led){
  /*
    Display if searching
  */
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(100);
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(1000);
}
