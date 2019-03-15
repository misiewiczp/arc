#include <SPI.h>

#define KTIR_PIN A5
#define MISO_PIN 12
#define BUF_SIZE sizeof(int)

volatile int val = 0;

bool active = false;
volatile union {
    int ival;
    char cval[BUF_SIZE];
} buf;



void setup() {
  pinMode(KTIR_PIN, INPUT);
  // have to send on master in, *slave out*
  pinMode(MISO_PIN, OUTPUT);
  // turn on SPI in slave mode
  SPCR |= bit(SPE);
  // turn on interrupts
  SPCR |= bit(SPIE);
}

void loop() {
    val = analogRead( KTIR_PIN );
    delay(10);
}

ISR (SPI_STC_vect)
{
  byte c = SPDR;

  if (c == 1)  // starting new sequence?
  {
    buf.ival = val;
    SPDR = buf.cval[c - 1];   // send first byte
    return;
  }

  if (c <=0 || c > BUF_SIZE)
  {
    SPDR = -1;
    return;
  }

  SPDR = buf.cval[c-1];
}
