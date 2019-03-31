#include <SPI.h>

#include "../pwm_read/proto.h"

#define KTIR_PIN A5
#define MISO_PIN 12
#define BUF_SIZE SPI_COMMAND_LEN

volatile int val = 0;

volatile spi_command buf;



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


volatile int position = -1;
ISR (SPI_STC_vect)
{
  byte c = SPDR;

  if (c == REQ_RC)  // starting new sequence?
  {
    buf.rc.motor = val;
    buf.rc.servo = 0;
    buf.rc.motor_off = 0;
    buf.rc.servo_off = 0;
    position = 0;

    SPDR = 100; // ACK
    return;
  } else if (c == 0)
  {

      if (position >= 0 && position < BUF_SIZE)
      {
	SPDR = buf.cval[position];
        position++;
	return;
      }
  }

  SPDR = 101;
}

