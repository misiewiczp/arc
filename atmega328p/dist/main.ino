#include <SPI.h>

#include "../pwm_read/proto.h"

#define MISO_PIN 12
#define BUF_SIZE SPI_COMMAND_LEN

#define ULTRASOUND_SPEED_2 (29<<1)

volatile int val = 0;
volatile spi_command buf;


void initMeasure()
{
  PORTC &= ~(1<<PC5);
  delayMicroseconds(2);
  PORTC |= (1<<PC5);
  delayMicroseconds(10);
  PORTC &= ~(1<<PC5);
}

void setup() {
  DDRC |= (1<<PC5);  // DIST - TRIGGER
  DDRD &= ~(1<<PD1); // DIST - ECHO
  DDRD |= (1<<PD7); // LED
  DDRB |= (1<<PB4); // MISO

  PCMSK2 |= (1<<PCINT17);
  PCICR |= (1<<PCIE2);
  // turn on SPI in slave mode
  SPCR |= bit(SPE);
  // turn on interrupts
  SPCR |= bit(SPIE);
}

void loop() {
    initMeasure();
    delay(100);
}

volatile long timer = 0;
volatile int cnt = 0;
ISR(PCINT2_vect)
{
    if (PIND & (1<<PD1)) {
	timer = micros();
    } else 
    if (timer != 0) {
	int tmp_val = (int)(micros()-timer);
	if (tmp_val >= ULTRASOUND_SPEED_2) {
	    val = tmp_val;
    	    cnt++;
	}
	timer = 0;
    }
    if (val > 0 && val <= 30*ULTRASOUND_SPEED_2)
	PORTD |= (1<<PD7); // LED ON
    else
	PORTD &= ~(1<<PD7); // LED OFF
}


volatile int position = -1;
ISR (SPI_STC_vect)
{
  byte c = SPDR;

  if (c == REQ_RC)  // starting new sequence?
  {
    buf.rc.motor = val/ULTRASOUND_SPEED_2; // /2 - two directions, /29 - 1 cm = 29 micorseconds
    buf.rc.servo = cnt;
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

