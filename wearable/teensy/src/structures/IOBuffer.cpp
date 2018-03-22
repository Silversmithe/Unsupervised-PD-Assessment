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
IOBuffer::IOBuffer(uint8_t bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new Data*[SIZE];

  // initialize all structs here
  for(int i=0; i<SIZE; i++){
    buffer[i] = new Data;
  }
}

/*
  @description:           * destructor *
                          deallocate all of the allocated memory from the
                          constructur
*/
IOBuffer::~IOBuffer(void){
  for(int i=0; i<SIZE; i++)
    delete buffer[i];

  delete[] buffer;
}

/*
  @return: (Data*):       a pointer to the frontmost data point in the circular
                          buffer
  @description:           enables the consumer to remove data points from the
                          circular buffer. changes the indicies so that the
                          frontmost datapoint can be overwritten as well as
                          returned to the calling program for use.
                          ASSUMING CHECKS ARE DONE FIRST
*/
Data* IOBuffer::remove_front(void){
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
bool IOBuffer::push_back(Data item){
  if(count == SIZE){ return false; } // if full do not add
  // store address of data in buffer
  buffer[pback]->dt = item.dt;

  /* deep copy */
  // emg
  for(int i=0; i<2; i++)
    buffer[pback]->emg[i] = item.emg[i];

  for(int i=0; i<10; i++){
    if(i<3){
      buffer[pback]->hand_pos[i] = item.hand_pos[i];
      buffer[pback]->thumb_pos[i] = item.thumb_pos[i];
      buffer[pback]->point_pos[i] = item.point_pos[i];
      buffer[pback]->ring_pos[i] = item.ring_pos[i];
    }
    // add rest
    buffer[pback]->hand[i] = item.hand[i];
    buffer[pback]->thumb[i] = item.thumb[i];
    buffer[pback]->point[i] = item.point[i];
    buffer[pback]->ring[i] = item.ring[i];
  }

  buffer[pback]->dt = item.dt;

  pback = (pback + 1) % SIZE;
  count++;
  return true;
}
