/*------------------------------------------------------------------------------
  file:         IOBuffer.cpp

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  An ADT that works as a circular data buffer for one consumer
                and one producer.
  ----------------------------------------------------------------------------*/
#include "IOBuffer.h"

/*
 * @function:       IOBuffer::IOBuffer
 *
 * @param:          (uint8_t) bsize: size of the buffer to be created
 *
 * @description:    * constructor *
 *                  create a circular data buffer of a specified
 *                  size and initialize all of its different components
 */
IOBuffer::IOBuffer(unsigned bsize){
  SIZE = bsize;
  pfront = pback = count = 0;
  buffer = new Data*[SIZE];

  // initialize all structs here
  for(unsigned i=0; i<SIZE; i++){
    buffer[i] = new Data;
  }
}

/*
 * @function:          IOBuffer::~IOBuffer
 *
 * @description:       * destructor *
 *                     deallocate all of the allocated memory from the
 *                     constructur
 */
IOBuffer::~IOBuffer(void){
  for(unsigned i=0; i<SIZE; i++)
    delete buffer[i];

  delete[] buffer;
}

/*
 * @function:             IOBuffer::remove_front
 *
 * @description:          enables the consumer to remove data points from the
 *                        circular buffer. changes the indicies so that the
 *                        frontmost datapoint can be overwritten as well as
 *                        returned to the calling program for use.
 *                        ASSUMING CHECKS ARE DONE FIRST
 *
 *  @return: (Data*):     a pointer to the frontmost data point in the circular
 *                        buffer
 */
Data* IOBuffer::remove_front(void){
  Data* temp = buffer[pfront];
  pfront = (pfront + 1) % SIZE;
  count--;
  return temp;
}

/*
 * @function:              IOBuffer::push_back
 *
 * @param:                 (Data) item: payload to push onto the buffer
 *
 * @description:           attempts to place a new data point into the circular
 *                         buffer.
 *
 * @return: (bool):        a boolean referring to the success or failure of the
 *                         calling program to insert a data point into the
 *                         circular buffer
 */
bool IOBuffer::push_back(Data item){
  if(count >= SIZE){ return false; } // if full do not add

  /* deep copy */
  for(int i=0; i<2; i++)          // emg
    buffer[pback]->emg[i] = item.emg[i];

  for(int i=0; i<9; i++){        // imu
    buffer[pback]->hand[i] = item.hand[i];
    buffer[pback]->thumb[i] = item.thumb[i];
    buffer[pback]->point[i] = item.point[i];
    buffer[pback]->ring[i] = item.ring[i];
  }

  pback = (pback + 1) % SIZE;
  count++;
  return true;
}
