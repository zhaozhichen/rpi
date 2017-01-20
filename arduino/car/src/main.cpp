#include "Arduino.h"
#include <Servo.h>

#define EN1  5//control right motor speed
#define EN2  6//control left motor speed
#define IN1  4//control right motor direction
#define IN2  7//control left motor direction
#define FORW 1//forward
#define BACK 0//backward
#define SPEED 255//0-255
#define SERVOANGLE 1
// #define DELAYSEC 10


Servo myservo;
int angle;

void MotorControl(int M1_DIR,int M1_EN,int M2_DIR,int M2_EN)
{
  //////////M1////////////////////////
  if(M1_DIR==FORW)//Motor 1 direction
    digitalWrite(IN1,HIGH);
  else
    digitalWrite(IN1,LOW);
  if(M1_EN==0)//Motor 1 speed
    analogWrite(EN1,LOW);//stop
  else
    analogWrite(EN1,M1_EN);//analog value of speed
  ///////////M2//////////////////////
  if(M2_DIR==FORW)
    digitalWrite(IN2,HIGH);
  else
    digitalWrite(IN2,LOW);
  if(M2_EN==0)
    analogWrite(EN2,LOW);
  else
    analogWrite(EN2,M2_EN);
}

void setup()
{
  Serial.begin(9600);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  myservo.attach(10);
}

void loop()
{
  char serIn = 0; 
  while(1){
  if (Serial.available() > 0) {
    serIn = Serial.read();
    switch(serIn){
      case 'H':
            MotorControl(FORW,0,FORW,0);
            break;     
      case 'F':
            MotorControl(FORW,SPEED,FORW,SPEED);
            break;
      case 'B':
            MotorControl(BACK,SPEED,BACK,SPEED);
            break;
      case 'L':
            MotorControl(BACK,SPEED,FORW,SPEED);
            break;
      case 'R':
            MotorControl(FORW,SPEED,BACK,SPEED);
            break;
      case 'U':
            angle = myservo.read();
            myservo.write(min(angle + SERVOANGLE,180));
            break;
      case 'D':
            angle = myservo.read();
            myservo.write(max(angle - SERVOANGLE,0));
            break;
      default:
            break;      
            }
    }
  }
}








