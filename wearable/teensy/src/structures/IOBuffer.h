/*------------------------------------------------------------------------------
  file:         IOBuffer.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  An ADT that works as a circular data buffer for one consumer
                and one producer.
  ----------------------------------------------------------------------------*/
#include "stdint.h"
#include "Data.h"

#ifndef IOBUFFER_H
#define IOBUFFER_H

class IOBuffer {
public:
  IOBuffer(uint8_t bsize);
  ~IOBuffer();

  /* ACCESSORS */
  uint8_t num_elts(){ return count; }           // how many items are stored
  bool is_full(){ return count == SIZE; }
  bool is_empty(){ return count == 0; }

  /* MUTATORS */
  Data* remove_front(); // consuming an item from the front
  bool push_back(Data item);     // producing an item and putting it in back

private:
  Data** buffer;        // array for storing all the data
  uint8_t SIZE;           // Buffer's static size
  uint8_t pfront, pback;  // Pointers for the program
  uint8_t count;          // how many items are in the buffer currently
};

#endif
