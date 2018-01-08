/*
  IOBuffer.cpp

  Alexander S. Adranly
*/
#include "IOBuffer.h"

IOMedBuffer::IOMedBuffer(uint8_t bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new MedData[SIZE];
}

IOMedBuffer::~IOMedBuffer(){
  delete[] buffer;
}

MedData IOMedBuffer::remove_front(){
  MedData temp = buffer[pfront];
  pfront = (pfront + 1) % SIZE;
  count--;
  return temp;
}

bool IOMedBuffer::push_back(MedData *item){
  if(count == SIZE){ return false; } // if full do not add
  pback = (pback + 1) % SIZE;
  buffer[pback] = *item;
  count++;
  return true;
}
