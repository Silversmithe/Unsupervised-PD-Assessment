/*
 * FILE:        wearable.cpp
 *
 * AUTHOR:      Alexander S. Adranly
 *
 * DESCRIPTION: Prototyping of the system using an Arduino
 *              while the teensy is currently in transit
 *
 * NOTES:
 * December 14th, 2017
 * Help from : https://playground.arduino.cc/Main/MPU-6050#sketch
 */

#include <Arduino.h>
#include <Wire.h>

// TEST MODES
#define NO_TEST -1
#define EMG_TEST 0
#define MPU9250_TEST 1
#define MPU6050_TEST 2

// accelerometer
const int MPU6_addr = 0x68; // default address of MPU6
int16_t Ax, Ay, Az, Tmp, Gx, Gy, Gz;

// PINS
const int EMG_SIG_PIN = 0;

void setup() {
    // put your setup code here, to run once:
    const int MODE = NO_TEST;

    // set up WIRE
    Wire.begin();
    Wire.beginTransmission(MPU6_addr);
    Wire.write(0);
    Wire.endTransmission();

    // initialize the serial monitor
    Serial.begin(9600);

}

void loop() {
    // put your main code here, to run repeatedly:
}

void read_emg(){
  // read the sensor value, convert it to another value
  int sensorValue = analogRead(EMG_SIG_PIN);
  Serial.print("EMG: ");
  Serial.println(sensorValue);
}

void read_mpu6050(){
  Wire.beginTransmission(MPU6_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6_addr,14,true);  // request a total of 14 registers

  Ax=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  Ay=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  Az=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  Gx=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  Gy=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  Gz=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  Serial.print("Ax = "); Serial.print(Ax);
  Serial.print(" | Ay = "); Serial.print(Ay);
  Serial.print(" | Az = "); Serial.print(Az);
  Serial.print(" | Tmp = "); Serial.print(Tmp/340.00+36.53);  //equation for temperature in degrees C from datasheet
  Serial.print(" | Gx = "); Serial.print(Gx);
  Serial.print(" | Gy = "); Serial.print(Gy);
  Serial.print(" | Gz = "); Serial.println(Gz);
  delay(333);
}
