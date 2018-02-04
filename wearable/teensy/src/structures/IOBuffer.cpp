/*------------------------------------------------------------------------------
  file:         IOBuffer.cpp

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  An ADT that works as a circular data buffer for one consumer
                and one producer.
  ----------------------------------------------------------------------------*/
#include "IOBuffer.h"

/*
  @param: (uint8_t) bsize: size of the buffer to be created

  @description:            * constructor *
                           create a circular data buffer of a specified
                           size and initialize all of its different components
*/
IOMedBuffer::IOMedBuffer(uint8_t bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new Data*[SIZE];
}

/*
  @description:           * destructor *
                          deallocate all of the allocated memory from the
                          constructur
*/
IOMedBuffer::~IOMedBuffer(){
  delete[] buffer;
}

/*
  @return: (Data*):       a pointer to the frontmost data point in the circular
                          buffer
  @description:           enables the consumer to remove data points from the
                          circular buffer. changes the indicies so that the
                          frontmost datapoint can be overwritten as well as
                          returned to the calling program for use.
*/
Data* IOMedBuffer::remove_front(){
  Data* temp = buffer[pfront];
  pfront = (pfront + 1) % SIZE;
  count--;
  return temp;
}

/*
  @return: (bool):        a boolean referring to the success or failure of the
                          calling program to insert a data point into the
                          circular buffer
  @description:           attempts to place a new data point into the circular
                          buffer.
*/
bool IOMedBuffer::push_back(Data item){
  if(count == SIZE){ return false; } // if full do not add
  // store address of data in buffer
  buffer[pback] = &item;

  pback = (pback + 1) % SIZE;
  count++;
  return true;
}
