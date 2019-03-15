#include <SPI.h>
#include "../pwm_read/proto.h"

#define MISO_PIN 12

#define SERVO_PIN_IN 3
#define MOTOR_PIN_IN 2

#define SERVO_PIN_ON _BV(PD3)
#define MOTOR_PIN_ON _BV(PD2)


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

// timer 16 bit, 8mhz, prescaler 8
    DDRB |= (1<<PB0)|(1<<PB1); // 16-bit PWM output on PB1
    TCCR1A = (1<<WGM11)|(1<<COM1A1); // Clear OC1A/OC1B on Compare Match when upcounting
    TCCR1B = ((1<<WGM12)|(1<<WGM13)|(1<<CS11)); // mode CTC
    ICR1=15830; // set the top value (up to 2^16)
    OCR1A=1500; // set PWM pulse width (duty)
    OCR1B=1500;
    TCNT1 = 0;
    TIMSK1|=(1<<OCIE1A); // timer A compare match interrupt
    TIMSK1|=(1<<OCIE1B); // timer B compare match interrupt
    TIMSK1|=(1<<TOIE1); // overflow interrupt

// INPUT
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(MOTOR_PIN_IN, INPUT);

  EIMSK |= (1 << INT0); // enable INT1
  EICRA |= (1 << ISC00); // CHANGE

  EIMSK |= (1 << INT1); // enable INT1
  EICRA |= (1 << ISC10); // CHANGE

  sei();
}

void loop() {
}

volatile unsigned long servo_timer_start = 0;
volatile unsigned long motor_timer_start = 0;

volatile unsigned long servo_off_timer_start = 0;
volatile unsigned long motor_off_timer_start = 0;

// MOTOR
ISR( INT0_vect ) 
{
    if(PIND & MOTOR_PIN_ON)
    { 
//	PORTD |= MOTOR_OUT_ON;
        motor_timer_start = micros();
	if (motor_off_timer_start != 0)
	{
    	    motor_off_val = (int)(motor_timer_start-motor_off_timer_start);
	    motor_off_timer_start = 0;
	}
    } 
    else
    { 
        //only worry about this if the timer has actually started
        if(motor_timer_start != 0)
        { 
//	    PORTD &= MOTOR_OUT_OFF;
	    motor_off_timer_start = micros();
            motor_val = (int)(motor_off_timer_start - motor_timer_start);
	    OCR1A = (motor_val < 1000 ? 1000 : (motor_val > 2000 ? 2000 : motor_val));
            motor_timer_start = 0;
        }
    }
} 

// SERVO
ISR( INT1_vect ) 
{
    if(PIND & SERVO_PIN_ON)
    { 
//	PORTB |= SERVO_OUT_ON;
        servo_timer_start = micros();
	if (servo_off_timer_start != 0)
	{
    	    servo_off_val = (int)(servo_timer_start-servo_off_timer_start);
	    servo_off_timer_start = 0;
	}
    } 
    else
    { 
        //only worry about this if the timer has actually started
        if(servo_timer_start != 0)
        { 
//	    PORTB &= SERVO_OUT_OFF;
	    servo_off_timer_start = micros();
            int tmp_servo_val = (int)(servo_off_timer_start - servo_timer_start);
//	    if (abs(tmp_servo_val - servo_val) >=  20)
	    servo_val = tmp_servo_val;
	    OCR1B = (servo_val < 1000 ? 1000 : (servo_val > 2000 ? 2000 : servo_val)); ;
            servo_timer_start = 0;
        }
    }
} 




ISR(TIMER1_COMPA_vect) {
//    PORTB &= ~(1<<PB0);
}

ISR(TIMER1_COMPB_vect) {
    PORTB &= ~(1<<PB0);
}


ISR(TIMER1_OVF_vect){
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
