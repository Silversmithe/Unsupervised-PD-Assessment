/*
  IOBuffer.cpp

  Alexander S. Adranly
*/
#include "IOBuffer.h"

IOMedBuffer::IOMedBuffer(uint8_t bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new Data*[SIZE];
  // for(int i=0; i<SIZE; i++){
  //   buffer[i] = new Data;
  // }
}

IOMedBuffer::~IOMedBuffer(){
  // for(int i=0; i<SIZE; i++) {
  //   delete buffer[i];
  // }
  delete[] buffer;
}

Data* IOMedBuffer::remove_front(){
  Data* temp = buffer[pfront];
  pfront = (pfront + 1) % SIZE;
  count--;
  return temp;
}

bool IOMedBuffer::push_back(Data item){
  if(count == SIZE){ return false; } // if full do not add
  // store address of data in buffer
  buffer[pback] = &item;

  pback = (pback + 1) % SIZE;
  count++;
  return true;
}
