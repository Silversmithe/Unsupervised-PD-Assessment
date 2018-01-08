/*
  multiDeviceBus.cpp

  Alexander Sami Adranly
*/

#include "MPU9250/MPU9250.h"

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire, 0x68);
MPU9250 IMU1(Wire,0x69);
int status, status1;

void setup() {
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

  // start communication with IMU
  status = IMU.begin();
  if (status < 0) {
    while(1) {
      Serial.println("IMU initialization unsuccessful");
      Serial.println("Check IMU wiring or try cycling power");
      Serial.print("Status: ");
      Serial.println(status);
      delay(1000);
    }
  }

  status1 = IMU1.begin();
  if (status1 < 0) {
    while(1) {
      Serial.println("IMU1 initialization unsuccessful");
      Serial.println("Check IMU1 wiring or try cycling power");
      Serial.print("Status: ");
      Serial.println(status1);
      delay(1000);
    }
  }
}

void loop() {
  // read the sensor
  IMU.readSensor();
  // display the data
  Serial.print("0x68: ");
  Serial.print(IMU.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelZ_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroX_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroY_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getGyroZ_rads(),6);
  Serial.print("\t");
  Serial.print(IMU.getMagX_uT(),6);
  Serial.print("\t");
  Serial.print(IMU.getMagY_uT(),6);
  Serial.print("\t");
  Serial.print(IMU.getMagZ_uT(),6);
  Serial.print("\t");
  Serial.println(IMU.getTemperature_C(),6);

  IMU1.readSensor();
  // display the data
  Serial.print("0x69: ");
  Serial.print(IMU1.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(IMU1.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.print(IMU1.getAccelZ_mss(),6);
  Serial.print("\t");
  Serial.print(IMU1.getGyroX_rads(),6);
  Serial.print("\t");
  Serial.print(IMU1.getGyroY_rads(),6);
  Serial.print("\t");
  Serial.print(IMU1.getGyroZ_rads(),6);
  Serial.print("\t");
  Serial.print(IMU1.getMagX_uT(),6);
  Serial.print("\t");
  Serial.print(IMU1.getMagY_uT(),6);
  Serial.print("\t");
  Serial.print(IMU1.getMagZ_uT(),6);
  Serial.print("\t");
  Serial.println(IMU1.getTemperature_C(),6);
  Serial.println();
  delay(200);
}
