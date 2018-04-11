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
uint8_t broadcast[11] = { 'U','P','D','A','-','W','E','A','R','-', DEVICE_ID};
Tx16Request tx_pl = Tx16Request(DEST_XBEE_ADDRESS, payload, sizeof(payload));
Tx16Request tx_bc = Tx16Request(DEST_XBEE_ADDRESS, broadcast, sizeof(broadcast));
TxStatusResponse tx_status = TxStatusResponse();
uint8_t __missed_messages;
uint32_t __packet_counter; // FOR PACKET ACCOUNTABILITY EXPERIMENT

/* logger and SD card */
File __file;

/*
 * @function:            initialize all hardware connections for all mediums
 *                       of communication
 *
 * @description:         the function attempts to connect the wearable device
 *                       with the chosen method of communication and will react
 *                       accordingly if unable to do so. It will also always
 *                       open a connection with the SD card port as a place to
 *                       do logging
 */
bool init_com(void){
  unsigned long start_time, current_time;
  bool hardware_success = true;
  /* ------------------------------- SERIAL ------------------------------ */
  if(SERIAL_SELECT){
    start_time = millis();
    Serial.begin(USB_BAUD);
    while(!Serial) {
      search_light();
      current_time = millis();
      if((current_time-start_time) > HW_TIMEOUT){
        hardware_success = false;
        break;
      }
    }
  }
  /* ------------------------------- XBEE ------------------------------- */
  if (XBEE_SELECT){
    start_time = millis();
    HWSERIAL.begin(RADIO_BAUD);
    while(!(HWSERIAL.availableForWrite() > 0)){
      search_light();
      current_time = millis();
      if((current_time-start_time) > HW_TIMEOUT){
        hardware_success = false;
        break;
      }
    }
    xbee.setSerial(HWSERIAL);
  }
  /* ------------------------------- SD ------------------------------- */
  if (!SD.begin(chip_select)){ hardware_success = false; }
  else {
    /* initialize logger */
    __file = SD.open("log.txt", FILE_WRITE);
    if(__file){ /* file created successfully */
      __file.println("----- logfile -----");
      __file.close();
    } else { /* error creating file */
      hardware_success = false;
    }

    __file = SD.open("data.txt", FILE_WRITE);
    if(__file){ /* file created successfully */
      __file.println("----- datafile -----");
      __file.close();
    } else { /* error creating file */
      hardware_success = false;
    }
  }

  /* initialize missed messages */
  __missed_messages = 0;

  return hardware_success;
}

/*
 * @function:     isAnyoneThere
 *
 * @description:  have the radio try and contact the local server and wait for
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

/*
 * @function:     open_datastream
 *
 * @description:  Open the file for data logging so that it can be read
 *                constantly to flush out the buffer
 */
void open_datastream(void){
  if(!__file) { __file = SD.open("data.txt", FILE_WRITE); }
}

/*
 * @function:     close_datastream
 *
 * @description:  Close the file for data logging so that other files can be
 *                written to
 */
void close_datastream(void){
  if(__file) { __file.close(); }
}

/*
 * @function:     log
 *
 * @param:        (const char*) message:  message to send to log
 *
 * @description:  record the given message in a new line in the log
 */
void log(const char* message){
  __file = SD.open("log.txt", FILE_WRITE);
  if(__file){
    __file.println(message);
    __file.close();
  }
}

/*
 * @function:     log_payload
 *
 * @param:        (Data*) src:  sample to record
 *
 * @description:  record the given message in a new line in the log
 */
ERROR log_payload(Data* src){
  // __file = SD.open("data.txt", FILE_WRITE);

  if(__file){
    // emg
    for(int iter=0; iter<2; iter++){
      __file.print(src->emg[iter]);
      if(iter < 1) { __file.print("    "); }
    }

    // hand
    __file.print("    ");
    for(int iter=0; iter<10; iter++){
      __file.print(src->hand[iter]);
      if(iter < 9) { __file.print("    "); }
    }
    __file.print("    ");
    for(int iter=0; iter<3; iter++){
      __file.print(src->hand_pos[iter]);
      if(iter < 2) { __file.print("    "); }
    }

    // thumb
    __file.print("    ");
    for(int iter=0; iter<10; iter++){
      __file.print(src->thumb[iter]);
      if(iter < 9) { __file.print("    "); }
    }
    __file.print("    ");
    for(int iter=0; iter<3; iter++){
      __file.print(src->thumb_pos[iter]);
      if(iter < 2) { __file.print("    "); }
    }

    // point
    __file.print("    ");
    for(int iter=0; iter<10; iter++){
      __file.print(src->point[iter]);
      if(iter < 9) { __file.print("    "); }
    }

    __file.print("    ");
    for(int iter=0; iter<3; iter++){
      __file.print(src->point_pos[iter]);
      if(iter < 2) { __file.print("    "); }
    }

    // ring
    __file.print("    ");
    for(int iter=0; iter<10; iter++){
      __file.print(src->ring[iter]);
      if(iter < 9) { __file.print("    "); }
    }
    __file.print("    ");
    for(int iter=0; iter<3; iter++){
      __file.print(src->ring_pos[iter]);
      if(iter < 2) { __file.print("    "); }
    }
    __file.println("");
    // __file.close();
  } else { return SD_ERROR; }

  return NONE;
}

/*
 * @function:    write_console
 *
 *  @param:       (Data*) src: a pointer to a data sample to print out to the console
 *
 *  @description: output the information of a given data point to the serial
 *                console if the serial monitor has been activated
 */
ERROR write_console(Data* src){
  if(!SERIAL_SELECT){ return NONE; } // exit if the serial select has not been seleced

  // delta time
  Serial.print(src->dt);
  Serial.print("\t");
  
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

  return NONE;
}

/*
 * @function:          write_radio
 *
 * @param:             (Data*) src: a pointer to a data sample to send over Xbee radio.
 *
 * @description:       check to make sure that the data point has been sent
 *                      successfully by waiting for an ACK for a certian amount
 *                      of time. Otherwise try resending it.
 *                      Eventually, if the message has not been achnowledged a couple
 *                      times, the wearable should throw an error and standby
 */
ERROR write_radio(Data* src){
  if(!XBEE_SELECT || src == NULL) { return NONE; } /* check radio */
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

  // attempt to send information over a pseudo TCP/IP
  for(int i=0; i<MISSED_LIMIT; i++){
    xbee.send(tx_pl);
    if(xbee.readPacket(XBEE_INIT_TIMEOUT)){ // wait for timeout
      if(xbee.getResponse().getApiId() == RX_16_RESPONSE)
        break;
      else
        __missed_messages += 1;

    } else if (xbee.getResponse().isError()){
      __missed_messages += 1;
    } else {
      __missed_messages += 1;
    }
  }

  if(__missed_messages >= MISSED_LIMIT) { return ISOLATED_DEVICE_ERROR; }
  return NONE;
}

/*
 * @function:       pack_float
 *
 * @param:          (float) src: the value to pack into a smaller space
 *
 * @description:    because floats normally take up four bits, we are taking
 *                  advantage of the fact that the values the floats are assuming
 *                  are smaller than their entire space, thus they can be compacted
 *                  into two bytes instead of four.
 *                  NOTE: all float multiplied by 100 and then stored
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
 * @function:       online_light
 *
 * @description:    use the onboard light on the MCU to show the user that the
 *                  device is running online (aka connected via xbee to the server)
 */
void online_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(100);
  digitalWrite(BUILTIN_LED, LOW);
  delay(100);
}

/*
 * @function:       offline_light
 *
 * @description:    use the onboard light on the MCU to show the user that the
 *                  device is running offline (aka NOT connected via xbee to the server)
 */
void offline_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(1000);
  digitalWrite(BUILTIN_LED, LOW);
  delay(1000);
}

/*
 * @function:         search_light
 *
 * @param: (int) led: the digital io pin to control an LED
 *
 * @description:      command the specified LED to output this particular pattern
 *                    to signal to the user that the device is searching for a
 *                    communication medium to connect and use
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
 * @function:     kill_light
 *
 * @description:  a command to tell the builtin LED to light up and never turn
 *                off to get the user's attention that the device needs to be
 *                rebooted.
 */
void kill_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
}
