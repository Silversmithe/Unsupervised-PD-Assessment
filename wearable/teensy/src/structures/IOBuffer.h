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
  IOBuffer(unsigned bsize);
  ~IOBuffer(void);

  /* ACCESSORS */
  inline unsigned num_elts(void){ return count; }
  inline bool is_full(void){ return count == SIZE; }
  inline bool is_empty(void){ return count == 0; }

  /* MUTATORS */
  Data* remove_front(void); // consuming an item from the front
  bool push_back(Data item);     // producing an item and putting it in back

private:
  Data** buffer;   // array for storing all the data
  unsigned SIZE;              // Buffer's static size
  unsigned pfront, pback;     // Pointers for the program
  unsigned count;             // how many items are in the buffer currently
};

#endif
