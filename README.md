# Unsupervised Parkinson's Disease Assessment
Our goal is to create a device that will utilize patient’s daily actions instead of choreographed actions to monitor and quantify Parkinson’s disease based on part of the motor control section of the UPDRS scale.

## Library Resources
* https://github.com/sparkfun/MPU-9250_Breakout
* https://github.com/bolderflight/MPU9250
* https://github.com/andrewrapp/xbee-arduino
* http://pyopengl.sourceforge.net/documentation/
* https://pypi.python.org/pypi/XBee

## Project Notes

### December 13th, 2017
* ShareLatex information has been commented, add correction of comments to next sprint
* change design document from sensor tag to teensy, and explain to group

### January 2nd, 2018
* Latency to read from a MPU9250 is worst case 1ms

### January 21st, 2018
- wearable device (V1: Iron Fist) built

### January 22nd, 2018
- wireless communication between XBee and Artik 710 over Zigbee
- Xbee is configured using XCTU
- end-to-end system prototype by the end of January (~February 2nd, 2018)

### March 18th, 2018
- started phase 2 of code which consists of:
    * a FSM that will set the device in an online mode or offline mode depending on network availablility
    * a kill state that will put the device into a stasis
    * adding the position data to the information
    * either in online mode or offline mode
    * sd card commnication for backup
    
- currently have done most hw and network checks EXCEPT SD card initialization
- currently cannot change out of ONLINE or OFFLINE
- ONLINE just sends data out as best it can
- OFFLINE just stores all the data on the SD card
- maybe if communication is bad (given a counter) have ONLINE transition to OFFLINE and never go back

### April 11th, 2018
- mahoney filter (thanks to sparkfun), is now functional with the UPDA system
- radio energy saving
- offline code completed
   * gathers data at the correct rate
   * stores data on the SD card
   * can send information to the serial console
- error handling complete
   
