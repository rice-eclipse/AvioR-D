#include <MobaTools.h>

//Move 8 steps pause 1 second and repeat endlessly
const byte stepPin = 3;
const byte dirPin = 2;
//const byte enablePin = 8;
int stepsToMove = 8;
unsigned long stepDelay = 1000; // milliseconds
MoToStepper stepper( 200, STEPDIR );

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  stepper.attach( stepPin, dirPin );
  stepper.setSpeedSteps(750);  // = 75 steps/second (steps in 10 seconds)
  stepper.setRampLen(10);
  stepper.setZero();
}

void loop() {
  // put your main code here, to run repeatedly:
  // while (!Serial.available());

  int x = Serial.readString().toInt();
  if (x != 0)
  {
    stepper.setSpeedSteps(x);
  }

  stepper.moveTo(50);
  delay(stepDelay);
  stepper.moveTo(100);
  delay(stepDelay);
  stepper.moveTo(150);
  delay(stepDelay);
}
  
