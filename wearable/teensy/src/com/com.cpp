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

uint8_t broadcast[]     = { BROADCAST, DEVICE_ID};
uint8_t new_data[]      = { NEW_DATA, DEVICE_ID };
uint8_t continue_data[] = { CONTINUE_DATA, DEVICE_ID };
uint8_t char_buffer[PAYLOAD_SIZE];

Tx16Request tx_bc = Tx16Request(SERVER_ADDR, broadcast, sizeof(broadcast));
Tx16Request tx_nd = Tx16Request(SERVER_ADDR, new_data, sizeof(new_data));
Tx16Request tx_cd = Tx16Request(SERVER_ADDR, continue_data, sizeof(continue_data));
Tx16Request tx_char = Tx16Request(SERVER_ADDR, char_buffer, sizeof(char_buffer));

/* response information */
TxStatusResponse tx16 = TxStatusResponse();

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
  if (!SD.begin(chip_select)){
    hardware_success = false;
  }
  else {
    /* initialize logger */
    __file = SD.open("log.txt", FILE_WRITE);
    if(__file){ /* file created successfully */
      __file.println("----- logfile -----");
      __file.close();
    } else { /* error creating file */
      hardware_success = false;
    }

    /* clean slate with each new run */
    if(SD.exists("data.txt")){
      SD.remove("data.txt");
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
  __packet_id = 0;

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
  /* continue to send messages until you miss the limit */
  __missed_messages = 0;
  while(__missed_messages < MISSED_LIMIT){
    xbee.send(tx_bc);
    /* get the tx status response */
    xbee.readPacket(10);
    if(xbee.getResponse().getApiId() == TX_STATUS_RESPONSE){
      xbee.getResponse().getTxStatusResponse(tx16);
      if(tx16.getStatus() == SUCCESS){ return true; }
    }
    __missed_messages++;
  }
  return false;
}

/*
 * @function:     open_datastream
 *
 * @description:  Open the file for data logging so that it can be read
 *                constantly to flush out the buffer
 */
void open_datastream(void){
  if(!__file) {
    __file = SD.open("data.txt", FILE_WRITE);
    if(__file){ /* file created successfully */
      __file.println("----- datafile -----");
    }
  }
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
  if(SERIAL_SELECT) { Serial.println(message); }
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
      if(iter < 1) { __file.print(" "); }
    }

    // hand
    __file.print(" ");
    for(int iter=0; iter<9; iter++){
      __file.print(src->hand[iter]);
      if(iter < 8) { __file.print(" "); }
    }

    // thumb
    __file.print(" ");
    for(int iter=0; iter<9; iter++){
      __file.print(src->thumb[iter]);
      if(iter < 8) { __file.print(" "); }
    }

    // point
    __file.print(" ");
    for(int iter=0; iter<9; iter++){
      __file.print(src->point[iter]);
      if(iter < 8) { __file.print(" "); }
    }

    // ring
    __file.print(" ");
    for(int iter=0; iter<9; iter++){
      __file.print(src->ring[iter]);
      if(iter < 8) { __file.print(" "); }
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

  // emg
  Serial.print("(");
  for(int iter=0; iter<2; iter++){
    Serial.print(src->emg[iter]);
    if(iter < 1) { Serial.print(", "); }
  }
  Serial.print(")\t");

  // hand
  Serial.print("(");
  for(int iter=0; iter<9; iter++){
    Serial.print(src->hand[iter]);
    if(iter < 8) { Serial.print(", "); }
  }
  Serial.print(")\t");

  // thumb
  Serial.print("(");
  for(int iter=0; iter<9; iter++){
    Serial.print(src->thumb[iter]);
    if(iter < 8) { Serial.print(", "); }
  }
  Serial.print(")\t");

  // point
  Serial.print("(");
  for(int iter=0; iter<9; iter++){
    Serial.print(src->point[iter]);
    if(iter < 8) { Serial.print(", "); }
  }
  Serial.print(")\t");

  // ring
  Serial.print("(");
  for(int iter=0; iter<9; iter++){
    Serial.print(src->ring[iter]);
    if(iter < 8) { Serial.print(", "); }
  }
  Serial.println(")");

  return NONE;
}

bool match(unsigned& index, uint8_t* buffer, uint8_t val){
  if(buffer[index] == val){
    index++;
    return true;
  }
  return false;
}

bool header(unsigned& index, uint8_t* buffer){
  bool result = false;
  // '----- '
  for(int i=0; i<5; i++){
    result |= match(index, buffer, '-');
  }
  result |= match(index, buffer, ' ');

  // match 'datafile'
  result |= match(index, buffer, 'd');
  result |= match(index, buffer, 'a');
  result |= match(index, buffer, 't');
  result |= match(index, buffer, 'a');
  result |= match(index, buffer, 'f');
  result |= match(index, buffer, 'i');
  result |= match(index, buffer, 'l');
  result |= match(index, buffer, 'e');

  // ' -----'
  result |= match(index, buffer, ' ');
  for(int i=0; i<5; i++){
    result |= match(index, buffer, '-');
  }

  return result;
}

/*
  read until a newline character

  space should already be allocated (300 bytes)
  does NOT store newline
 */
unsigned read_line(uint8_t* buffer){
  uint8_t lookahead;
  unsigned count = 0;

  /* clearing out the spaces */
  if(__file.available()) {
    lookahead = __file.read();
    while(__file.available() && (lookahead == '\n' || lookahead == 13)){
      lookahead = __file.read(); // skip to the next one
    }
  } else { return 0; } /* error */


  /* actually going to read to file */
  if(__file.available()){
    while(__file.available()){
      if(count >= FILE_BUFFER){ return count; } // too large!
      if(count != 0) { lookahead = __file.read(); }
      /* stop if nl | cr */
      if(lookahead == '\n' || lookahead == 13){ break; }
      buffer[count++] = lookahead;
    }
  } else { return 0; } /* error */

  return count;
}

/*
  parse the line

  uint8_t: buffer of the line read

  return boolean: is the line a header or not
*/
bool parse_line(unsigned size, uint8_t* buffer){
  unsigned index = 0;

  /* detect lookahead */
  if(buffer[index] == '-' && header(index, buffer)){ return true; }

  return false;
}

bool write_line(unsigned size, uint8_t* buffer){
  unsigned index = 3;

  char_buffer[0] = PAYLOAD;
  char_buffer[1] = __packet_id;
  char_buffer[2] = ' ';

  for(unsigned i = 0; i < size; i++){
    if(index == PAYLOAD_SIZE){
      /* packet is full */
      /* send information */
      while(__missed_messages < MISSED_LIMIT){
        xbee.send(tx_char);
        /* get the tx status response */
        xbee.readPacket(TX_STAT_WAIT);
        if(xbee.getResponse().getApiId() == TX_STATUS_RESPONSE){
          xbee.getResponse().getTxStatusResponse(tx16);
          if(tx16.getStatus() == SUCCESS){ break; }
          else { Serial.println("missed");}
        }
        __missed_messages = __missed_messages + 1;
      }
      if(__missed_messages >= MISSED_LIMIT) { return false; }

      index = 3; // reset that index
    }

    /* store the valuable information to send in char buffer */
    char_buffer[index++] = buffer[i];
  }

  /* send out last message */
  while(__missed_messages < MISSED_LIMIT){
    xbee.send(tx_char);
    /* get the tx status response */
    xbee.readPacket(TX_STAT_WAIT);
    if(xbee.getResponse().getApiId() == TX_STATUS_RESPONSE){
      xbee.getResponse().getTxStatusResponse(tx16);
      if(tx16.getStatus() == SUCCESS){ break; }
      else { Serial.println("missed");}
    }
    __missed_messages = __missed_messages + 1;
  }
  if(__missed_messages >= MISSED_LIMIT) { return false; }

  return true;
}

bool write_data_radio(bool isnew){
  while(__missed_messages < MISSED_LIMIT){
    if(isnew){ xbee.send(tx_nd); }
    else { xbee.send(tx_cd); }

    /* get the tx status response */
    xbee.readPacket(TX_STAT_WAIT);
    if(xbee.getResponse().getApiId() == TX_STATUS_RESPONSE){
      xbee.getResponse().getTxStatusResponse(tx16);
      if(tx16.getStatus() == SUCCESS){ return true; }
    }
    __missed_messages = __missed_messages + 1;
  }
  return false;
}

/*
 * @function:         write_to_server
 *
 * @description:      send all of the information for all the different
 *                    sessions
 *
 *  note: return value is the position of the device in the file currently
 *
 */
uint32_t write_to_server(uint32_t position){
  uint8_t* buffer = new uint8_t[FILE_BUFFER];
  unsigned size;
  uint32_t current_pos = position;
  bool header = false;

  if(__file){ __file.close(); }

  if(SD.exists("data.txt")){

    Serial.println();
    Serial.println("ready to transmit...");
    delay(5000);

    /* should prepare file to be opened */
    if(!__file){
      __file = SD.open("data.txt");
      if(__file.seek(current_pos)){
        Serial.println("found the current position");
      } else {
        Serial.println("could not reach position!!");
      }
    }
    digitalWrite(LED_MODE_STAT, LOW);

    /*
    PARSE A DATA SEGMENT

    a segment consists of a header line
    and multiple sample lines
    */
    if(__file){
      /* check for the header */
      __packet_id = 0;
      if(__file.available()){
        size = read_line(buffer);
        header = parse_line(size, buffer);
      }

      /* header devices */
      if(header){ write_data_radio(true); } /* send header signal */
      else { write_data_radio(false); }

      /* read samples */
      while(__file.available()){
        size = read_line(buffer);
        header = parse_line(size, buffer);

        if(header){ break; } // bread out of data segment

        // WRITE TO THE "XBEE"
        if(!write_line(size, buffer)) {
          Serial.println("error writing to radio");
          break;
        }
        __packet_id = (__packet_id + 1) % 16; // keep within the size of a file
        // delay(10); // slight delay is healthy for server
        transfer_mode_light();
      }

      current_pos = __file.position();
      __file.close();
    }
  } else {
    log("no data exists to write");
    if(SERIAL_SELECT){ Serial.println("no data exists to write"); }
  }
  // turn btn_mode light back on
  digitalWrite(LED_MODE_STAT, HIGH);

  delete[] buffer;
  return current_pos;
}

/*
 * @function:       online_light
 *
 * @description:    use the onboard light on the MCU to show the user that the
 *                  device is running online (aka connected via xbee to the server)
 */
void online_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(500);
  digitalWrite(BUILTIN_LED, LOW);
  delay(500);
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
 * @function:         transfer_mode_light
 *
 * @param: (int) led: the digital io pin to control an LED
 *
 * @description:      light that specifies that a radio transfer is
 *                    happening and that the power should NOT be turned off
 */
void transfer_mode_light(void){
  digitalWrite(BUILTIN_LED, HIGH);
  delay(5);
  digitalWrite(BUILTIN_LED, LOW);
  delay(5);
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
