#include <MobaTools.h>

const byte stepPin0 = 3;
const byte dirPin0 = 2;
const byte stepPin1 = 5;
const byte dirPin1 = 4;

MoToStepper stepper0( 200, STEPDIR );
MoToStepper stepper1( 200, STEPDIR );

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);

  stepper0.attach( stepPin0, dirPin0 );   
  stepper0.setSpeedSteps(750);  // = 75 steps/second (steps in 10 seconds)
  stepper0.setRampLen(10);
  stepper0.setZero();

  stepper1.attach( stepPin1, dirPin1 );   
  stepper1.setSpeedSteps(500);  // = 50 steps/second (steps in 10 seconds)
  stepper1.setRampLen(10);
  stepper1.setZero();
}

void loop()
{ 

  int x = Serial.readString().toInt();
  if (x != 0)
  {
    //stepper0.setSpeedSteps(x);
    moveStepper0(100, x);
  }

  //moveStepper0(100, 500); 
  //moveStepper1(100, 500);
  //delay(5000);

}


void moveStepper0(long stepPosToMove, long stepSpeed)
{
  stepper0.setSpeedSteps(stepSpeed);
  stepper0.moveTo(stepPosToMove);
  stepper0.setZero();
}

void moveStepper1(long stepPosToMove, long stepSpeed)
{
  stepper1.setSpeedSteps(stepSpeed);
  stepper1.moveTo(stepPosToMove);
  stepper1.setZero();
}


/* Nonblocking version

#include <MobaTools.h>

#define HOLDING true
#define ON_MOVE false 

const byte stepPin0 = 3;
const byte dirPin0 = 2;
const byte stepPin1 = 5;
const byte dirPin1 = 4;

unsigned long timer = 0;

MoToStepper stepper0( 200, STEPDIR );
MoToStepper stepper1( 200, STEPDIR );

bool mode = false;
bool moving = false;

void setup()
{
  Serial.begin(115200);

  stepper0.attach( stepPin0, dirPin0 );   
  stepper0.setSpeedSteps(750);  // = 75 steps/second (steps in 10 seconds)
  stepper0.setRampLen(10);
  stepper0.setZero();

  stepper1.attach( stepPin1, dirPin1 );   
  stepper1.setSpeedSteps(500);  // = 50 steps/second (steps in 10 seconds)
  stepper1.setRampLen(10);
  stepper1.setZero();
}

void loop()
{
  // how many steps, speed (steps/sec * 10, 2000 = 200 sps)
  moveStepper(stepper0, 200, 750); 
  moveStepper(stepper1, 100, 500);
  // time between move in millis() 
  holdup(5000);  
}

void moveStepper(MoToStepper stepper, long stepsToMove, long stepSpeed)
{
   if (mode == ON_MOVE) // time to go?  
   {
      if (moving == false) // stopped, set speed and steps. set to move
      {
         stepper.setSpeedSteps(stepSpeed);
         stepper.move(stepsToMove);
         moving = true;
      }
      else // in motion, check for ending position.  mode to hold on end
      {
         if (stepper.moving() == 0)
         {
            mode = HOLDING;
            moving = false;  
            timer = millis(); // record current time
         }
      }
   }
}

void holdup(unsigned long stepDelay) // dwell between moves
{
   if(mode == HOLDING)
   {
      if(millis() - timer >= stepDelay)
      {
         mode = ON_MOVE; // time to move again
      }
   }
}
*/