#include <SPI.h>

#define LM393_PIN 3
#define MISO_PIN 12
#define BUF_SIZE sizeof(int)

volatile int val = 0;

bool active = false;
volatile union {
    int ival;
    char cval[BUF_SIZE];
} buf;

volatile unsigned long lastCounter = 0;
void counter()
{
    if (millis() - lastCounter >= 1)
    {
	lastCounter = millis();
        if (digitalRead(LM393_PIN) == HIGH)
	    val++;
    }
}

void setup() {
  pinMode(LM393_PIN, INPUT);
  // have to send on master in, *slave out*
  pinMode(MISO_PIN, OUTPUT);
  // turn on SPI in slave mode
  SPCR |= bit(SPE);
  attachInterrupt(1, counter, RISING);
  // turn on interrupts
  SPCR |= bit(SPIE);
}

void loop() {
//    int len = pulseIn( LM393_PIN, HIGH );
//    if (len > 0)
//	val++;
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
