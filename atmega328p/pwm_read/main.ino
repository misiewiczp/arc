#include <SPI.h>
#include "proto.h"

// Arduino numbering
#define SERVO_PIN_IN 3
#define MOTOR_PIN_IN 2

#define SERVO_PIN_OUT 9
#define MOTOR_PIN_OUT 6

#define SERVO_LED_PIN  8
#define MOTOR_LED_PIN  7

#define MISO_PIN 12

#define SERVO_OUT_ON (_BV(PB0)|_BV(PB1))
#define SERVO_OUT_OFF ~(SERVO_OUT_ON)

#define MOTOR_OUT_ON (_BV(PD6)|_BV(PD7))
#define MOTOR_OUT_OFF ~(MOTOR_OUT_ON)

#define SERVO_PIN_ON _BV(PD3)
#define MOTOR_PIN_ON _BV(PD2)


volatile unsigned int motor_val = 0;
volatile unsigned int servo_val = 0;

volatile unsigned int motor_off_val = 0;
volatile unsigned int servo_off_val = 0;


#define BUF_SIZE SPI_COMMAND_LEN
volatile spi_command buf;


void calcSignal();

void setup() {
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(MOTOR_PIN_IN, INPUT);

//  pinMode(SERVO_PIN_OUT, OUTPUT);
//  pinMode(MOTOR_PIN_OUT, OUTPUT);

//  pinMode(SERVO_LED_PIN, OUTPUT);
//  pinMode(MOTOR_LED_PIN, OUTPUT);

  DDRB |= SERVO_OUT_ON;
  DDRD |= MOTOR_OUT_ON;
  
  // have to send on master in, *slave out*
  pinMode(MISO_PIN, OUTPUT);

  EIMSK |= (1 << INT0); // enable INT1
  EICRA |= (1 << ISC00); // CHANGE

  EIMSK |= (1 << INT1); // enable INT1
  EICRA |= (1 << ISC10); // CHANGE

  // turn on SPI in slave mode
  SPCR |= bit(SPE);
  // turn on interrupts
  SPCR |= bit(SPIE);

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
	PORTD |= MOTOR_OUT_ON;
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
	    PORTD &= MOTOR_OUT_OFF;
	    motor_off_timer_start = micros();
            motor_val = (int)(motor_off_timer_start - motor_timer_start);
            motor_timer_start = 0;
        }
    }
} 

// SERVO
ISR( INT1_vect ) 
{
    if(PIND & SERVO_PIN_ON)
    { 
	PORTB |= SERVO_OUT_ON;
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
	    PORTB &= SERVO_OUT_OFF;
	    servo_off_timer_start = micros();
            servo_val = (int)(servo_off_timer_start - servo_timer_start);
            servo_timer_start = 0;
        }
    }
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
