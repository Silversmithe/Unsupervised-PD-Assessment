/*
  IOBuffer.cpp

  Alexander S. Adranly
*/
#include "IOBuffer.h"

IOMedBuffer::IOMedBuffer(uint8_t bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new MedData*[SIZE];
  for(int i=0; i<SIZE; i++){
    buffer[i] = new MedData;
  }
}

IOMedBuffer::~IOMedBuffer(){
  for(int i=0; i<SIZE; i++) {
    delete buffer[i];
  }
  delete[] buffer;
}

MedData* IOMedBuffer::remove_front(){
  MedData* temp = buffer[pfront];
  pfront = (pfront + 1) % SIZE;
  count--;
  return temp;
}

bool IOMedBuffer::push_back(MedData item){
  if(count == SIZE){ return false; } // if full do not add
  // store all information
  // time
  buffer[pback]->dT = item.dT;

  // emg
  buffer[pback]->emg_raw = item.emg_raw;
  buffer[pback]->emg_rect = item.emg_rect;

  // hand
  // acceleration
  buffer[pback]->Hand_Ax = item.Hand_Ax;
  buffer[pback]->Hand_Ay = item.Hand_Ay;
  buffer[pback]->Hand_Az = item.Hand_Az;
  // gyroscope
  buffer[pback]->Hand_Gx = item.Hand_Gx;
  buffer[pback]->Hand_Gy = item.Hand_Gy;
  buffer[pback]->Hand_Gz = item.Hand_Gz;

  // thumb
  // acceleration
  buffer[pback]->Thumb_Ax = item.Thumb_Ax;
  buffer[pback]->Thumb_Ay = item.Thumb_Ay;
  buffer[pback]->Thumb_Az = item.Thumb_Az;
  // gyroscope
  buffer[pback]->Thumb_Gx = item.Thumb_Gx;
  buffer[pback]->Thumb_Gy = item.Thumb_Gy;
  buffer[pback]->Thumb_Gz = item.Thumb_Gz;

  // pointer
  // acceleration
  buffer[pback]->Point_Ax = item.Point_Ax;
  buffer[pback]->Point_Ay = item.Point_Ay;
  buffer[pback]->Point_Az = item.Point_Az;
  // gyroscope
  buffer[pback]->Point_Gx = item.Point_Gx;
  buffer[pback]->Point_Gy = item.Point_Gy;
  buffer[pback]->Point_Gz = item.Point_Gz;

  // ring
  // acceleration
  buffer[pback]->Ring_Ax = item.Ring_Ax;
  buffer[pback]->Ring_Ay = item.Ring_Ay;
  buffer[pback]->Ring_Az = item.Ring_Az;
  // gyroscope
  buffer[pback]->Ring_Gx = item.Ring_Gx;
  buffer[pback]->Ring_Gy = item.Ring_Gy;
  buffer[pback]->Ring_Gz = item.Ring_Gz;

  pback = (pback + 1) % SIZE;
  count++;
  return true;
}
