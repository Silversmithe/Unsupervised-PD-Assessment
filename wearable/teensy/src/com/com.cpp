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

/* xbee communication */
XBee xbee = XBee();
uint8_t payload[52];
uint8_t broadcast[1] = { 0xFF };
Tx16Request tx_pl = Tx16Request(DEST_XBEE_ADDRESS, payload, sizeof(payload));
Tx16Request tx_bc = Tx16Request(DEST_XBEE_ADDRESS, broadcast, sizeof(broadcast));
TxStatusResponse txStatus = TxStatusResponse();

/* logger and SD card */
File __logfile;
bool __log_open;

/*
 * function:             initialize all hardware connections for all mediums
 *                       of communication
 *
 *  description:         the function attempts to connect the wearable device
 *                       with the chosen method of communication and will react
 *                       accordingly if unable to do so. It will also always
 *                       open a connection with the SD card port as a place to
 *                       do logging
 */
bool init_com(void){
  unsigned long start_time, current_time;
  bool hardware_success = true;
  /* SERIAL */
  if(SERIAL_SELECT){
    start_time = millis();
    Serial.begin(USB_BAUD);
    while(!Serial.available()) {
      search_light();
      current_time = millis();
      if((current_time-start_time) < HW_TIMEOUT){
        hardware_success = false;
        break;
      }
    }
  }
  /* XBEE */
  if (XBEE_SELECT){
    start_time = millis();
    HWSERIAL.begin(RADIO_BAUD);
    while(!(HWSERIAL.availableForWrite() > 0)){
      search_light();
      current_time = millis();
      if((current_time-start_time) < HW_TIMEOUT){
        hardware_success = false;
        break;
      }
    }
    xbee.setSerial(HWSERIAL);
  }
  /* SD */
  if (!SD.begin(chip_select)){ hardware_success = false; }
  else {
    /* initialize logger */
    __logfile = SD.open("log.txt", FILE_WRITE);
    if(__logfile){
      /* file created successfully */
      __logfile.println("----- logfile -----");
      __logfile.close();
    } else {
      /* error creating file */
      hardware_success = false;
    }
  }
  __log_open = false;

  return hardware_success;
}

/*
 * function:     isAnyoneThere
 *
 *  description:  have the radio try and contact the local server and wait for
 *                a response. Return true or false depending on if you get a
 *                response or not. (true) a server is there, (false) a server
 *                is NOT there.
 */
bool isAnyoneThere(void){
  xbee.send(tx_bc);
  if(xbee.readPacket(XBEE_INIT_TIMEOUT)){ // wait for timeout
    if(xbee.getResponse().getApiId() == RX_16_RESPONSE)
      return true;
    return false;
  } else if (xbee.getResponse().isError()){
    return false;
  } else {
    return false; // could not contact local xbee
  }
}

void open_log(void){
  if(!__log_open){__logfile = SD.open("log.txt", FILE_WRITE); }
  __log_open = true;
}

/*
*/
void close_log(void){
  if(__log_open){ __logfile.close(); }
  __log_open = false;
}

/*
*/
void log(char * message){
  if(!__log_open){ __logfile = SD.open("log.txt", FILE_WRITE); }
  __logfile.println(message);
  __logfile.close();
}

/*
*/
void log_payload(Data* src, bool burst){
  if(!burst){open_log();}
  float * point = src->hand;

  /* print emg*/
  __logfile.print(src->emg[0]);
  __logfile.print(" ");
  __logfile.print(src->emg[1]);
  __logfile.print(" ");

  /* print emg and position */
  for(int i=0; i<4; i++){ // IMUS
    __logfile.print(point[0]);
    __logfile.print(" ");
    __logfile.print(point[1]);
    __logfile.print(" ");
    __logfile.print(point[2]);
    __logfile.print(" ");
    __logfile.print(point[3]);
    __logfile.print(" ");
    __logfile.print(point[4]);
    __logfile.print(" ");
    __logfile.print(point[5]);
    __logfile.print(" ");
    __logfile.print(point[6]);
    __logfile.print(" ");
    __logfile.print(point[7]);
    __logfile.print(" ");
    __logfile.print(point[8]);
    __logfile.print(" ");
    __logfile.print(point[9]);
    __logfile.print(" ");
    __logfile.print(point[10]);
    __logfile.print(" ");
    __logfile.print(point[11]);
    __logfile.print(" ");
    __logfile.print(point[12]);
    __logfile.print(" ");
    point = point + 13; // go to the next set
  }
  
  __logfile.println();
  if(!burst){close_log();}
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

  xbee.send(tx_pl);
}

/*
*/
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
void search_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(100);
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(1000);
}

/*
  function:     kill_light

  description:  a command to tell the builtin LED to light up and never turn
                off to get the user's attention that the device needs to be
                rebooted.
 */
void kill_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
}
