#include <SPI.h>
#include "../pwm_read/proto.h"

#define MISO_PIN 12

volatile unsigned int motor_val = 0;
volatile unsigned int servo_val = 0;

volatile unsigned int motor_off_val = 0;
volatile unsigned int servo_off_val = 0;


#define BUF_SIZE SPI_COMMAND_LEN
volatile spi_command buf;


void setup() {
  // have to send on master in, *slave out*
  pinMode(MISO_PIN, OUTPUT);

  // turn on SPI in slave mode
  SPCR |= bit(SPE);
  // turn on interrupts
  SPCR |= bit(SPIE);

    DDRB |= (1<<PB0)|(1<<PB1); // 16-bit PWM output on PB1
    TCCR1A = (1<<WGM11)|(1<<COM1A1); // Clear OC1A/OC1B on Compare Match when upcounting
    TCCR1B = ((1<<WGM12)|(1<<WGM13)|(1<<CS11)); // mode CTC
    ICR1=15800; // set the top value (up to 2^16)
    OCR1A=1300; // set PWM pulse width (duty)
    TCNT1 = 0;
    TIMSK1|=(1<<OCIE1A); // timer A compare match interrupt
    TIMSK1|=(1<<TOIE1); // overflow interrupt
//    PORTB |= _BV(PB1);

  sei();
}

void loop() {
}

volatile unsigned long servo_timer_start = 0;
volatile unsigned long motor_timer_start = 0;

volatile unsigned long servo_off_timer_start = 0;
volatile unsigned long motor_off_timer_start = 0;


ISR(TIMER1_COMPA_vect) {
    if (motor_timer_start > 0) {
	motor_val = (int)(micros()-motor_timer_start);
    }
    motor_timer_start = micros();
    PORTB &= ~(1<<PB0);
}

ISR(TIMER1_OVF_vect){
    if (motor_timer_start > 0) {
	motor_off_val = (int)(micros()-motor_timer_start);
    }
    motor_timer_start = micros();
    servo_val++;
    PORTB |= (1<<PB0);
}


volatile int position = -1;
ISR (SPI_STC_vect)
{
  byte c = SPDR;

  if (c == REQ_RC)  // starting new sequence?
  {
    buf.rc.motor = motor_val;
    buf.rc.servo = servo_val;
    buf.rc.motor_off = motor_off_val;
    buf.rc.servo_off = servo_off_val;
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
