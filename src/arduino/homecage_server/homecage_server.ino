/*
    This program is a server for controlling the hardware peripherals attached to the HomeCage system.
    It waits for commands over a serial port (python client in our case) and performs the desired action upon receiving the command.
    There is no proper message passing system and it simply uses various magic byte values as messages.
    Note: These bytes can cause different outcomes depending on the state the program is in at the time
    of receiving. The lack of real message passing system means the program is rather fragile. I recommend
    not modifying this program too much. Utility may instead be found by recycling specific functions.
    (For controlling servos, steppers, IR breakers, etc....attached to the Arduino).


    This program enters a listening mode on boot and waits for a signal over serial to tell it to start a session.
    Once this signal is received, the program expects to receive a byte value representing how far the stepper should
    rotate from the origin (The origin is defined on start-up by retracting the stepper motor until the limit switch
    is pressed). After the stepper motor is positioned, the program expects to receive repeating requests for
    pellet presentations (with either arm). The program continues in this state until the IR breaker is connected.
    At this point the server sends a session termination message to the client and tears the session down, re-entering
    it's default listening mode.


    Author: Julian Pitney, Junzheng Wu
    Email: JulianPitney@gmail.com, jwu220@uottawa.ca
    Organization: University of Ottawa (Silasi Lab)

*/

#include <Servo.h>

// Config
const int servo1Pin = 8;
Servo servo1;

bool servo1_up_flag = false;
const int SERVO_SETTLE_DELAY = 300;
// Higher numbers make the arm go higher
int SERVO1_UP_POS = 28;
// Low numbers makehe arm go lower
int SERVO1_DOWN_POS = 100;

int SERVO_PULSE_DELAY = 19;

int SERVO_PULSE_DELAY_UP = 19;
int SERVO_PULSE_DELAY_DOWN = 25;

int servo1Pos = SERVO1_DOWN_POS;


typedef enum {x, y} whichStepper;
const int ledPin = 13;
const int switchPin1 = 9;
const int switchPin2 = 10;
const int IRBreakerPin = A2;
const int vibrationPin = A1;
const int digitalSwitchPin = A3;

const int step1_left = 2;
const int step1_right = 3;
const int step1_sleep = 4;

const int step2_left = 5;
const int step2_right = 6;
const int step2_sleep = 7;



volatile byte switchState1 = digitalRead(switchPin1);
volatile byte switchState2 = digitalRead(switchPin2);
volatile byte IRState = digitalRead(IRBreakerPin);

int stepperDistFromOrigin = -1;
double stepsToMmRatio = 420;

void handleSwitchChange1() {
  switchState1 = digitalRead(switchPin1);
}
void handleSwitchChange2() {
  switchState2 = digitalRead(switchPin2);
}

void handleIRChange() {
  IRState = digitalRead(IRBreakerPin);  
  digitalWrite(ledPin, IRState);
}

int zeroServos() {

  servo1.attach(servo1Pin);

  for (int i = servo1Pos; i <= SERVO1_DOWN_POS; i += 1) {
      servo1.write(i);
      delay(SERVO_PULSE_DELAY);
    }   
  delay(SERVO_SETTLE_DELAY);
  servo1Pos = SERVO1_DOWN_POS;
  
  servo1.detach();
  return 0;

}

int lowerServo1(){
 
  servo1.attach(servo1Pin);
   
  for (int i = servo1Pos; i <= SERVO1_DOWN_POS; i += 1) {
      servo1.write(i);
      delay(SERVO_PULSE_DELAY);
    }   
  delay(SERVO_SETTLE_DELAY);
  servo1Pos = SERVO1_DOWN_POS;
  
  servo1.detach();
  return 0;
}

int displayPellet() {
    
  servo1.attach(servo1Pin);

  // Lower arm to grab pellet.
  for (int i = servo1Pos; i <= SERVO1_DOWN_POS; i += 1) {
    servo1.write(i);
    delay(SERVO_PULSE_DELAY_UP);
  }   
  // Raise arm to display pellet
  delay(SERVO_PULSE_DELAY_DOWN);
  for (int i = SERVO1_DOWN_POS; i >= SERVO1_UP_POS; i -= 1) {
    servo1.write(i);
    delay(SERVO_PULSE_DELAY_DOWN);
  }
  delay(SERVO_SETTLE_DELAY);
  servo1Pos = SERVO1_UP_POS;
  servo1_up_flag = true;
  servo1.detach();
  return 0;
}

int moveStepper_both(int targetPos1, int targetPos2) {
  digitalWrite(step1_sleep, HIGH);
  digitalWrite(step2_sleep, HIGH);
  delay(100);
  int step1 = 0;
  int step2 = 0;
  
  if(targetPos1 > 0){step1 = -1; digitalWrite(step1_left, LOW);}
  else{step1 = 1; digitalWrite(step1_left, HIGH);}
  if(targetPos2 > 0){step2 = -1; digitalWrite(step2_left, LOW);}
  else{step2 = 1; digitalWrite(step2_left, HIGH);}
  
  int count1 = targetPos1 * stepsToMmRatio;
  int count2 = targetPos2 * stepsToMmRatio;
  
  while((count1 != 0) || (count2 != 0))
  {
    if(count1 != 0)
    {
      count1 += step1;
      digitalWrite(step1_right, HIGH);
    }
    if(count2 != 0)
    {
      count2 += step2;
      digitalWrite(step2_right, HIGH);
    }
    delayMicroseconds(500);
    if(count1 != 0)
    {
      digitalWrite(step1_right, LOW);
    }
    if(count2 != 0)
    {
      digitalWrite(step2_right, LOW);
    }
    delayMicroseconds(500);
      
  }
  digitalWrite(step1_sleep, LOW);
  digitalWrite(step2_sleep, LOW);
  return 0;
}



int zeroStepper_both(){

  int left = 0;
  int right = 0;
  
  digitalWrite(step1_sleep, HIGH);
  digitalWrite(step2_sleep, HIGH);
  delay(100);
  digitalWrite(step1_left, HIGH);
  digitalWrite(step2_left, HIGH);
  delay(100);
  while((!digitalRead(switchPin1)) || (!digitalRead(switchPin2))){
    digitalWrite(vibrationPin, HIGH);
    if (!digitalRead(switchPin1)){digitalWrite(step1_right, LOW);}
    if (!digitalRead(switchPin2)){digitalWrite(step2_right, LOW);}
    delayMicroseconds(500);
    if (!digitalRead(switchPin1)){digitalWrite(step1_right, HIGH);}
    if (!digitalRead(switchPin2)){digitalWrite(step2_right, HIGH);}
    delayMicroseconds(500);
  }
  digitalWrite(vibrationPin, LOW);
  digitalWrite(step1_sleep, LOW);
  digitalWrite(step2_sleep, LOW);
  return 0;
}


void setup() {

  // Open serial connection
  // Note: This takes a bit to connect so while(!Serial) keeps it waiting
  // until the connection is ready.
  Serial.begin(9600);
  while (!Serial) {
    delay(100);
  }
  pinMode(digitalSwitchPin, OUTPUT);
  digitalWrite(digitalSwitchPin, LOW);
  
  pinMode(vibrationPin, OUTPUT);
  digitalWrite(vibrationPin, LOW);
  zeroServos();
  
  pinMode(step1_sleep, OUTPUT);
  pinMode(step2_sleep, OUTPUT);
  
  pinMode(switchPin1, INPUT_PULLUP);
  switchState1 = digitalRead(switchPin1);
  attachInterrupt(digitalPinToInterrupt(switchPin1), handleSwitchChange1, CHANGE);

  pinMode(switchPin2, INPUT_PULLUP);
  switchState2 = digitalRead(switchPin2);
  attachInterrupt(digitalPinToInterrupt(switchPin2), handleSwitchChange2, CHANGE);

  pinMode(IRBreakerPin, INPUT_PULLUP);
  IRState = digitalRead(IRBreakerPin);
  attachInterrupt(digitalPinToInterrupt(IRBreakerPin), handleIRChange, HIGH);
  
  // Set LED control pin
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  Serial.write("READY\n");
}

bool listenForStartCommand() {
  char authByte;
  while(true) {
    if(Serial.available() > 0) {
      authByte = Serial.read();
    }
    else{return false;}
    if(authByte == 'A') {
      return true;
    }
    else if (authByte == 'Y' ) {
      digitalWrite(ledPin, HIGH);
      return false;
    }

  }
}

int startSession() {
  bool startedflag = false;
  while(!digitalRead(IRBreakerPin)) {
    startedflag = true;
    char cmd;
    char stepperDist1;
    char stepperDist2;
    int stepperDistInt1;
    int stepperDistInt2;
    if(Serial.available() > 0) {
      cmd = Serial.read();
      
      switch(cmd){
        
        case ('1'):
          displayPellet();
          break;
          
        case ('2'):
          displayPellet();
          break;
          
        case ('3'):

          // Give client a second to respond
          delay(200);   
          stepperDist1 = Serial.read();
            
          delay(200);
          
          stepperDist2 = Serial.read();

          if (isDigit(stepperDist1)){stepperDistInt1 = stepperDist1 - '0';}
          else{stepperDistInt1 = 10 + stepperDist1 - 'a';}
          if (isDigit(stepperDist2)){stepperDistInt2 = stepperDist2 - '0';}
          else{stepperDistInt2 = 10 + stepperDist2 - 'a';}
          moveStepper_both(stepperDistInt1, stepperDistInt2);
          break;
        case ('4'):
          displayPellet();
          break;
        default:
          break;
      }
    }
    
  }
  if(servo1_up_flag)
  {
    lowerServo1();
    servo1_up_flag = false;
  }
  
  return 0;
  
}

void test_switch(){
  while(!digitalRead(switchPin2)){
    digitalWrite(ledPin, HIGH);
  }
  digitalWrite(ledPin, LOW);
  delay(500);
}

void test_beambreaker(){
  while(!digitalRead(IRBreakerPin)){
    digitalWrite(ledPin, HIGH);
    }
  digitalWrite(ledPin, LOW);
  delay(500);
}

void test_servo(){
  displayPellet();
}

void test_stepper(){
  zeroStepper_both();
  moveStepper_both(15, 7);
}

void loop(){
  boolean DEBUG = false;
  if(DEBUG){
//    digitalWrite(digitalSwitchPin, HIGH);
    test_stepper();
//    digitalWrite(digitalSwitchPin, HIGH);
//    delay(1000);
//    digitalWrite(digitalSwitchPin, LOW);
//    delay(1000);
//    test_servo();
    while(1){delay(100);}
  }
  else{
    if(listenForStartCommand()){
    digitalWrite(digitalSwitchPin, HIGH);
    digitalWrite(ledPin, LOW);
    startSession();
    Serial.write("TERM\n");
    digitalWrite(digitalSwitchPin, LOW);
    zeroStepper_both();
    }
  }
  digitalWrite(ledPin, HIGH);  
}
