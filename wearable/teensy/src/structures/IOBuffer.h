/*
  IOBuffer.cpp

  Alexander S. Adranly

  A buffer that contains MedData structs. The buffer can handle only one
  producer and one consumer
*/
#include "stdint.h"
#include "Data.h"

#ifndef IOBUFFER_H
#define IOBUFFER_H

class IOMedBuffer {
public:
  IOMedBuffer(uint8_t bsize);
  ~IOMedBuffer();

  /* ACCESSORS */
  uint8_t num_elts(){ return count; }           // how many items are stored
  bool has_more_elts(){ return (count > 0); }   // are there any more items
  uint8_t buffer_size(){ return SIZE; }  // size of whole buffer
  bool is_full(){ return count == SIZE; }
  bool is_empty(){ return count == 0; }

  /* MUTATORS */
  MedData remove_front();           // consuming an item from the front
  bool push_back(MedData* item);    // producing an item and putting it in back

private:
  MedData* buffer;        // array for storing all the data
  uint8_t SIZE;    // Buffer's static size
  uint8_t pfront, pback;  // Pointers for the program
  uint8_t count;          // how many items are in the buffer currently
};

#endif
