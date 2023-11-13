// Include the AccelStepper Library
#include <AccelStepper.h>

// Define pin connections
const int dirPin = 2;
const int stepPin = 3;

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // set the maximum speed, acceleration factor,
	// initial speed and the target position
  myStepper.setCurrentPosition(0);
  myStepper.setMaxSpeed(100);
	myStepper.setAcceleration(50);
	myStepper.setSpeed(0);
	myStepper.moveTo(500);
}

void loop() {
  // Change direction once the motor reaches target position
	while (myStepper.distanceToGo() != 0){
    myStepper.move(10);
    delay(2000);
  }
  if (myStepper.distanceToGo() == 0){
    myStepper.stop();
  }
	// Move the motor one step
	myStepper.run();

}
