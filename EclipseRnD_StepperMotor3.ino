//Move 8 steps pause 1 second and repeat endlessly

#include <MobaTools.h>

const byte stepPin = 3;
const byte dirPin = 2;
//const byte enablePin = 8;

int stepsToMove = 8;
unsigned long stepDelay = 1000; // milliseconds

MoToStepper stepper( 200, STEPDIR );

void setup()
{
  Serial.begin(115200);

  stepper.attach( stepPin, dirPin );   
  stepper.setSpeedSteps(750);  // = 75 steps/second (steps in 10 seconds)
  stepper.setRampLen(10);
  stepper.setZero();
}

void loop()
{
  //gear ratio 3:1
  
  /*
  stepper.move(stepsToMove);
  while(stepper.distanceToGo() > 0);
  delay(stepDelay);
  */
  /*
  stepper.write(30);
  delay(stepDelay);
  stepper.write(60);
  delay(stepDelay);
  stepper.write(90);
  */
  stepper.moveTo(50);
  delay(stepDelay);
  stepper.moveTo(100);
  delay(stepDelay);
  stepper.moveTo(150);
  delay(stepDelay);
}


