#include <SPI.h>
#include "../pwm_read/proto.h"

#define MISO_PIN 12

#define SERVO_PIN_IN 3
#define MOTOR_PIN_IN 2

#define SERVO_PIN_ON _BV(PD3)
#define MOTOR_PIN_ON _BV(PD2)

#define TIMER1_MAX 15830
#define MOTOR_0 1490
#define SERVO_0 1500

volatile unsigned int motor_val = MOTOR_0;
volatile unsigned int servo_val = SERVO_0;
volatile unsigned int distance_val = 0;

volatile unsigned long timer1_counter = 0;
volatile unsigned char timer1_idx = 0;


#define ULTRASOUND_SPEED_2 (29<<1)


volatile int motor_trimmer = 1;
volatile int motor_max = 1600;
volatile int motor_min = 1350;

volatile int is_autonomous = 1;

#define BUF_SIZE SPI_COMMAND_LEN
volatile spi_command buf;

unsigned long inline mymicros()
{   
    unsigned long val =  timer1_counter + TCNT1;
    return val;
}


unsigned long inline mymicrosdiff(unsigned long old)
{   
    unsigned long val =  timer1_counter + TCNT1;    
    return (old > val ? val+TIMER1_MAX-old : (val > old + TIMER1_MAX ? val - old - TIMER1_MAX : val-old));
}


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
    ICR1=TIMER1_MAX; // set the top value (up to 2^16)
    OCR1A=MOTOR_0; // set PWM pulse width (duty)
    OCR1B=SERVO_0;
    TCNT1 = 0;    
    TIMSK1|=(1<<OCIE1A); // timer A compare match interrupt
    TIMSK1|=(1<<OCIE1B); // timer B compare match interrupt
    TIMSK1|=(1<<TOIE1); // overflow interrupt

// INPUT
  pinMode(SERVO_PIN_IN, INPUT);
  pinMode(MOTOR_PIN_IN, INPUT);

  if (!is_autonomous)
  {
    EIMSK |= (1 << INT0); // enable INT1
    EICRA |= (1 << ISC00); // CHANGE

    EIMSK |= (1 << INT1); // enable INT1
    EICRA |= (1 << ISC10); // CHANGE
  }

// distance sensor
  DDRC |= (1<<PC5);  // DIST - TRIGGER
  DDRD &= ~(1<<PD1); // DIST - ECHO
  DDRD |= (1<<PD7); // LED
  DDRB |= (1<<PB4); // MISO

// whats that ?
  PCMSK2 |= (1<<PCINT17);
  PCICR |= (1<<PCIE2);


  sei();
}


void initMeasure()
{
  PORTC &= ~(1<<PC5);
  delayMicroseconds(2);
  PORTC |= (1<<PC5);
  delayMicroseconds(10);
  PORTC &= ~(1<<PC5);
}



volatile unsigned long servo_timer_start = 0;
volatile unsigned long motor_timer_start = 0;
volatile unsigned long distance_timer_start = 0;


void loop() {    
//    if (distance_timer_start == 0)
//        initMeasure();
//    delay(50); // shorter than maximum time of over 50ms

}

// DISTANCE value
ISR(PCINT2_vect)
{
    if (PIND & (1<<PD1)) {
	distance_timer_start = mymicros();
    } else 
    if (distance_timer_start != 0) {
	int tmp_val = (unsigned int)(mymicrosdiff(distance_timer_start));
	if (tmp_val >= ULTRASOUND_SPEED_2) {
	    distance_val = tmp_val / ULTRASOUND_SPEED_2;
	    if (distance_val > 0 && distance_val <= 30)
		PORTD |= (1<<PD7); // LED ON
	    else
		PORTD &= ~(1<<PD7); // LED OFF
	}
	distance_timer_start = 0;
    }
}


// MOTOR
ISR( INT0_vect ) 
{
    if(PIND & MOTOR_PIN_ON)
    { 
        motor_timer_start = mymicros();
    } 
    else
    { 
        //only worry about this if the timer has actually started
        if(motor_timer_start != 0)
        { 
            if (!is_autonomous)
        	motor_val = (int)(mymicrosdiff(motor_timer_start));
            motor_timer_start = 0;
        }
    }
} 

// SERVO
ISR( INT1_vect ) 
{
    if(PIND & SERVO_PIN_ON)
    { 
        servo_timer_start = mymicros();
    } 
    else
    { 
        //only worry about this if the timer has actually started
        if(servo_timer_start != 0)
        { 	    
	    if (!is_autonomous)
        	servo_val = (int)(mymicrosdiff(servo_timer_start));
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
    cli();
    PORTB |= (1<<PB0);
    timer1_counter += TIMER1_MAX;
    timer1_idx += 1;
    OCR1B = (servo_val < 1000 ? 1000 : (servo_val > 2000 ? 2000 : servo_val)); ;
    volatile int tmp_motor_val = MOTOR_0 + (motor_val >= MOTOR_0 ? (motor_val - MOTOR_0)/motor_trimmer : -((MOTOR_0-motor_val)/motor_trimmer));
    OCR1A = (tmp_motor_val < motor_min ? motor_min : (tmp_motor_val > motor_max ? motor_max : tmp_motor_val));
    sei();
    if (distance_timer_start == 0)
        initMeasure();
}


volatile int position = -1;
volatile int last_command = -1;

volatile byte motor_servo_buf[4] = {0,};

ISR (SPI_STC_vect)
{
  byte c = SPDR;

  if (last_command == -1) {
     switch(c){
         case REQ_RC:
         case 0x11:
         case 0x12:
         case 0x13:
            last_command = c;
         default:
	    break;
     }
  }
  
  if (last_command == REQ_RC)
  {
    if (c == REQ_RC)  // starting new sequence?
    {
	buf.rc.motor = motor_val;
	buf.rc.servo = servo_val;
	buf.rc.motor_off = 0; //motor_off_val;
	buf.rc.servo_off = 0; //servo_off_val;
	buf.rc.distance = distance_val;
	buf.rc.idx = timer1_idx;
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
    last_command = -1;
    position = -1;
    return;
  }

  if (last_command == 0x13) {
     if (position == -1)
         position = 0;
     else 
     if (position >= 0 && position < 4)
     {
	motor_servo_buf[position++] = c;
     }
     else
     if (position == 4 && c == 0xFF)
     {
        unsigned int tmp_motor_pwm = (((unsigned int)motor_servo_buf[1])<<8) + (unsigned int)motor_servo_buf[0];
        unsigned int tmp_servo_pwm = (((unsigned int)motor_servo_buf[3])<<8) + (unsigned int)motor_servo_buf[2];
	motor_val = tmp_motor_pwm;
        servo_val = tmp_servo_pwm;
        last_command = -1; // the end of data
	position = -1;
        SPDR = 0x13;
        return;
     }
     SPDR = 0;
     return;
  }
  
  SPDR = 0xAA; //error
  last_command = -1;
}
