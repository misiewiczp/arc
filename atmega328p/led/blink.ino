int led = A5;

void setup() {
	pinMode(led, OUTPUT);
	digitalWrite(led, HIGH);
}

void loop() {
	digitalWrite(led, HIGH);
	delay(1000);
//	digitalWrite(led, LOW);
//	delay(1000);
}
