#include "Arduino.h"
#include <Servo.h>
#include <IrReceiverSampler.h>
#include <Nec1Decoder.h>

#define EN1  5//control right motor speed
#define EN2  6//control left motor speed
#define IN1  4//control right motor direction
#define IN2  7//control left motor direction
#define SERVO_PIN 10
#define IR_PIN 8
#define BUFFERSIZE 200U
#define FORW 1//forward
#define BACK 0//backward
#define SPEED 255//0-255
#define SERVOANGLE 5

#define KEY_REPEAT "NEC1 ditto"
#define KEY_POWER "NEC1 0 69"
#define KEY_MODE "NEC1 0 70"
#define KEY_MUTE "NEC1 0 71"
#define KEY_PLAY "NEC1 0 68"
#define KEY_BACK "NEC1 0 64"
#define KEY_FWD "NEC1 0 67"
#define KEY_EQ "NEC1 0 7"
#define KEY_MINUS "NEC1 0 21"
#define KEY_PLUS "NEC1 0 9"
#define KEY_ZERO "NEC1 0 22"
#define KEY_SHUFFLE "NEC1 0 25"
#define KEY_USD "NEC1 0 13"
#define KEY_ONE "NEC1 0 12"
#define KEY_TWO "NEC1 0 24"
#define KEY_THREE "NEC1 0 94"
#define KEY_FOUR "NEC1 0 8"
#define KEY_FIVE "NEC1 0 28"
#define KEY_SIX "NEC1 0 90"
#define KEY_SEVEN "NEC1 0 66"
#define KEY_EIGHT "NEC1 0 82"
#define KEY_NINE "NEC1 0 74"

Servo myservo;
int angle;

void MotorControl(int M1_DIR,int M1_EN,int M2_DIR,int M2_EN)
{
  //M1
  if(M1_DIR==FORW)//Motor 1 direction
    digitalWrite(IN1,HIGH);
  else
    digitalWrite(IN1,LOW);
  if(M1_EN==0)//Motor 1 speed
    analogWrite(EN1,LOW);//stop
  else
    analogWrite(EN1,M1_EN);//analog value of speed
  //M2
  if(M2_DIR==FORW)
    digitalWrite(IN2,HIGH);
  else
    digitalWrite(IN2,LOW);
  if(M2_EN==0)
    analogWrite(EN2,LOW);
  else
    analogWrite(EN2,M2_EN);
}

IrReceiver *receiver;
const char *lastKey;

void setup()
{
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  myservo.attach(SERVO_PIN);
  receiver = IrReceiverSampler::newIrReceiverSampler
      (BUFFERSIZE, IR_PIN, false, 50, 500);
}

void loop()
{
    receiver->receive();
    if (receiver->isEmpty())
        MotorControl(FORW,0,FORW,0);
    else {
        Nec1Decoder decoder(*receiver);
        const char * thisKey = decoder.getDecode();
        if (!strcmp(thisKey,KEY_REPEAT))
            thisKey = lastKey;
        else if (!strcmp(thisKey,KEY_BACK))
            MotorControl(FORW,0,FORW,0);
        else if (!strcmp(thisKey,KEY_MODE))
            MotorControl(FORW,SPEED,FORW,SPEED);
        else if (!strcmp(thisKey,KEY_MINUS))
            MotorControl(BACK,SPEED,BACK,SPEED);
        else if (!strcmp(thisKey,KEY_PLAY))
            MotorControl(BACK,SPEED,FORW,SPEED);
        else if (!strcmp(thisKey,KEY_FWD))
            MotorControl(FORW,SPEED,BACK,SPEED);
        else if (!strcmp(thisKey,KEY_POWER)){
            angle = myservo.read();
            myservo.write(min(angle + SERVOANGLE,180));
        }
        else if (!strcmp(thisKey,KEY_MUTE)){
            angle = myservo.read();
            myservo.write(max(angle - SERVOANGLE,0));
        }
        lastKey = thisKey;
    }
  }
