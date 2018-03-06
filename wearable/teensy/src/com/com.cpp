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

/* Global Functions for Use */
XBee xbee = XBee();
uint8_t payload[52];
Tx16Request tx = Tx16Request(DEST_XBEE_ADDRESS, payload, sizeof(payload));

/*
  @description:          the function attempts to connect the wearable device
                         with the chosen method of communication and will react
                         accordingly if unable to do so
*/
void init_com(){
  if(SERIAL_SELECT){
    // connect with the Serial USB connection
    Serial.begin(USB_BAUD);
    while(!Serial.available()) { com_search_light(); }
  } // fin

  if (XBEE_SELECT){
    // connect with the Xbee
    HWSERIAL.begin(RADIO_BAUD);
    while(!(HWSERIAL.availableForWrite() > 0)) { com_search_light(); }
    xbee.setSerial(HWSERIAL);
  } // fin

  if(!SERIAL_SELECT && !XBEE_SELECT){
    // throw an error
    // no communication medium selected
    // panic
  } // fin
}

/*
  @param: (Data*) src: a pointer to a data sample to print out to the console

  @description: output the information of a given data point to the serial
                console if the serial monitor has been activated
*/
void write_console(Data* src){
  if(!SERIAL_SELECT){ return; } // exit if the serial select has not been seleced

  // write time elapsed since last sample
  Serial.print("(");
  Serial.print(src->dt);
  Serial.print(")\t");

  // emg
  Serial.print("(");
  for(int iter=0; iter<2; iter++){
    Serial.print(src->emg[iter]);
    if(iter < 1) { Serial.print(", "); }
  }
  Serial.print(")\t");

  // hand
  Serial.print("(");
  for(int iter=0; iter<10; iter++){
    Serial.print(src->hand[iter]);
    if(iter < 9) { Serial.print(", "); }
  }
  Serial.print(")");
  Serial.print("[");
  for(int iter=0; iter<3; iter++){
    Serial.print(src->hand_pos[iter]);
    if(iter < 2) { Serial.print(", "); }
  }
  Serial.print("]\t");

  // thumb
  Serial.print("(");
  for(int iter=0; iter<10; iter++){
    Serial.print(src->thumb[iter]);
    if(iter < 9) { Serial.print(", "); }
  }
  Serial.print(")");
  Serial.print("[");
  for(int iter=0; iter<3; iter++){
    Serial.print(src->thumb_pos[iter]);
    if(iter < 2) { Serial.print(", "); }
  }
  Serial.print("]\t");

  // point
  Serial.print("(");
  for(int iter=0; iter<10; iter++){
    Serial.print(src->point[iter]);
    if(iter < 9) { Serial.print(", "); }
  }
  Serial.print(")");
  Serial.print("[");
  for(int iter=0; iter<3; iter++){
    Serial.print(src->point_pos[iter]);
    if(iter < 2) { Serial.print(", "); }
  }
  Serial.print("]\t");

  // ring
  Serial.print("(");
  for(int iter=0; iter<10; iter++){
    Serial.print(src->ring[iter]);
    if(iter < 9) { Serial.print(", "); }
  }
  Serial.print(")");
  Serial.print("[");
  for(int iter=0; iter<3; iter++){
    Serial.print(src->ring_pos[iter]);
    if(iter < 2) { Serial.print(", "); }
  }
  Serial.println("]");
}

/*
  @param: (Data*) src: a pointer to a data sample to send over Xbee radio.

  @description:       check to make sure that the data point has been sent
                      successfully by waiting for an ACK for a certian amount
                      of time. Otherwise try resending it.
                      Eventually, if the message has not been achnowledged a couple
                      times, the wearable should throw an error and standby
*/
void write_radio(Data* src){
  if(!XBEE_SELECT || src == NULL) { return; } /* check radio */
  /* check error messages */
  uint16_t packet_info;
  unsigned packet_index = 0;

  // transform into a packet
  /* emg */
  for(int i=0; i<2; i++){
    payload[packet_index] = (src->emg[i] >> 8) & 0x00FF;
    packet_index = packet_index + 1;
    payload[packet_index] = src->emg[i] & 0x00FF;
    packet_index = packet_index + 1;
  }

  /* hand */
  for(int i=0; i<6; i++){
    packet_info = pack_float(src->hand[i]);
    payload[packet_index] = (packet_info >> 8) & 0x00FF;
    packet_index = packet_index + 1;
    payload[packet_index] = packet_info & 0x00FF;
    packet_index = packet_index + 1;
  }

  /* thumb */
  for(int i=0; i<6; i++){
    packet_info = pack_float(src->thumb[i]);
    payload[packet_index] = (packet_info >> 8) & 0x00FF;
    packet_index = packet_index + 1;
    payload[packet_index] = packet_info & 0x00FF;
    packet_index = packet_index + 1;
  }

  /* point */
  for(int i=0; i<6; i++){
    packet_info = pack_float(src->point[i]);
    payload[packet_index] = (packet_info >> 8) & 0x00FF;
    packet_index = packet_index + 1;
    payload[packet_index] = packet_info & 0x00FF;
    packet_index = packet_index + 1;
  }

  /* ring */
  for(int i=0; i<6; i++){
    packet_info = pack_float(src->ring[i]);
    payload[packet_index] = (packet_info >> 8) & 0x00FF;
    packet_index = packet_index + 1;
    payload[packet_index] = packet_info & 0x00FF;
    packet_index = packet_index + 1;
  }

  // float tosend = -34.53;
  // uint16_t send = pack_float(tosend);
  // payload[0] = (send >> 8) & 0x00FF;
  // payload[1] = send & 0x00FF;

  // send packet over to xbee

  xbee.send(tx);

  // wait for a response, if not, resend
  // once we are done
}

uint16_t pack_float(float src){
  /* to get decimals mult by 100 */
  if(src >= 0){
    return (uint16_t)(src*100);
  } else {
    // turn positive and then manually
    // place bit
    uint16_t result = (uint16_t) ((-1 * src) * 100);
    result = result | 0x8000;  // set MSB for negation
    return result;
  }
}
/*
  @param: (int) led: the digital io pin to control an LED

  @description:      command the specified LED to output this particular pattern
                     to signal to the user that the device is searching for a
                     communication medium to connect and use
*/
void com_search_light(){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(1000);
}
