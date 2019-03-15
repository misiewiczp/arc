#include <SPI.h>

#define SERVO_OUT PB1
#define MOTOR_OUT PB2

void SetupPWM(){
    // 16-bit timer for 50 Hz, with an 8 MHz clock
    DDRB|=(_BV(PB1)|_BV(PB0)); // 16-bit PWM output on PB1
//    TCCR1A &= ~_BV(COM1A1); // Clear OC1A/OC1B on Compare Match when upcounting
    TCCR1B|= ((1<<WGM12)|(1<<WGM13)); // mode CTC
    TCCR1B|=(1<<CS11); // /8 prescaler
    ICR1=20000; // set the top value (up to 2^16)
    OCR1A=1000; // set PWM pulse width (duty)
    TCNT1 = 0;
    TIMSK1|=(1<<OCIE1A); // timer A compare match interrupt
    TIMSK1|=(1<<TOIE1); // overflow interrupt
    PORTB |= _BV(PB1);

    sei();
}

void setup() {
    SetupPWM();
}

void loop() {

}

volatile short pwm = 10000;
ISR(TIMER1_COMPA_vect) {
//    PORTB &= ~_BV(PB0);
//    PORTB ^= (1<<PB1);
//    volatile byte pb = PORTB;
    PORTB ^= ((1<<PB1)|(1<<PB0));
//    pb |= ;
//    PORTB = pb;

//    OCR1A = 500;
}

ISR(TIMER1_OVF_vect){
//    PORTB &= ~((1<<PB1)|(1<<PB0));
//    PORTB |= _BV(PB0);
//    PORTB ^= _BV(PB1);
    TCNT1 = 0;
    PORTB ^= ((1<<PB1)|(1<<PB0));
    OCR1A = pwm;
/*    pwm += 10;
    if (pwm > 2000)
	pwm = 100;
*/
}
