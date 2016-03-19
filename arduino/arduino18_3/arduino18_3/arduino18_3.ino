#include <PID_v1.h>
 
#define motorPWM1 3  // sag motor kirmizi pin
#define motorPWM2 4  // sag motor siyah pin
#define motorPWM3 5  // sol motor kirmizi pin
#define motorPWM4 6  // sol motor siyah pin
#define enablePin  52 
#define encoderRight  18
#define encoderLeft 19
#define controlLed 13

volatile int hitsRight = 0;
volatile int hitsLeft = 0;
int raspMessage,dummyVar,roundDirection,var, zot; 
double SetPoint1, SetPoint2, SetPoint3, SetPoint4;
double Input1, Input2, Input3, Input4;
double  Output1, Output2, Output3, Output4;
int encoderDifference; 

PID myPIDStraight1(&Input1, &Output1, &SetPoint1, 15, 80, 40, DIRECT);
PID myPIDStraight2(&Input2, &Output2, &SetPoint2, 15, 80, 40, DIRECT);
PID myPIDround1(&Input3, &Output3, &SetPoint3, 15, 80, 40, DIRECT);
PID myPIDround2(&Input2, &Output2, &SetPoint4, 15, 80, 40, DIRECT);
void setup() {
  Serial.begin(9600);
  pinMode(encoderRight, INPUT);
  pinMode(encoderLeft, INPUT);
  pinMode(controlLed, OUTPUT);
  // put your setup code here, to run once:
  attachInterrupt(4, countLeft, CHANGE);
  attachInterrupt(5, countRight, CHANGE); 
  pinMode(motorPWM1, OUTPUT);
  pinMode(motorPWM2, OUTPUT);
  pinMode(motorPWM3, OUTPUT);
  pinMode(motorPWM4, OUTPUT);
  analogWrite(motorPWM1, 0);
  analogWrite(motorPWM2, 0);
  analogWrite(motorPWM3, 0);
  analogWrite(motorPWM4, 0);
  digitalWrite(controlLed, LOW);

  SetPoint1=1;  SetPoint2=1;  SetPoint3=1;  SetPoint4=1;
  myPIDStraight1.SetMode(AUTOMATIC); 
  myPIDStraight2.SetMode(AUTOMATIC); 
  myPIDround1.SetMode(AUTOMATIC); 
  myPIDround2.SetMode(AUTOMATIC);
   
  }


void loop() {
   while (true){
     if(Serial.available()>0){
       var = (int) Serial.read();
       if(var==20)
           break;     
     }  
  }
   Serial.println (5); 
   while (true){
   if(Serial.available ()>0){
      raspMessage = (int) Serial.read();
      switch (raspMessage){
        case 49: {
          
          dummyVar= (int) Serial.read();
          if(raspRX()==10)
             digitalWrite(controlLed,HIGH); 
          //roundDirection= (int) Serial.read();
          //dummyVar= dummyVar-48;          
          roundAround(zot);
          Serial.println(2);
         }
        case 50: {
            analogWrite(motorPWM1, 0);
            analogWrite(motorPWM4, 0);
          dummyVar= (int) Serial.read();
          //goStraight (dummyVar);
          Serial.print(2);
          }        
        }
    } 
  }
}
void roundAround (int var){
  hitsLeft=0;
  hitsRight=0;
  Input1 = hitsLeft - hitsRight ;
  Input2 = hitsRight - hitsLeft ;  
  analogWrite(motorPWM1, 125);//sag kirmizi
  analogWrite(motorPWM3, 125);//sol siyah
  while(hitsLeft<1000 || hitsRight<1000){    
  if (hitsLeft > hitsRight){
    myPIDround1.Compute();
    analogWrite(motorPWM1, Output3);
    analogWrite(motorPWM3, 125);}
  if (hitsRight > hitsLeft){
    myPIDround2.Compute();
    analogWrite(motorPWM1, 125);
    analogWrite(motorPWM3, Output4);}
  if (hitsLeft == hitsRight){
    analogWrite(motorPWM1, Output3);
    analogWrite(motorPWM3, Output4);}
  Serial.print('(');
  Serial.print(hitsRight);
  Serial.print(',');
  //Serial.print(", Hits2=");
  Serial.print(hitsLeft);
  Serial.println(')');
    }
 
  }
void goStraight(int var){
  hitsLeft=0;
  hitsRight=0;
  Input3 = hitsLeft - hitsRight ;
  Input4 = hitsRight - hitsLeft ; 
  analogWrite(motorPWM1, 125);
  analogWrite(motorPWM4, 125);
  while(hitsLeft<var){    
  if (hitsLeft > hitsRight){
    myPIDStraight1.Compute();
    analogWrite(motorPWM1, Output3);
    analogWrite(motorPWM4, 125);}
  if (hitsRight > hitsLeft){
    myPIDStraight2.Compute();
    analogWrite(motorPWM1, 125);
    analogWrite(motorPWM4, Output4);}
  if (hitsLeft == hitsRight){
    analogWrite(motorPWM1, Output3);
    analogWrite(motorPWM4, Output4);}
    }  
  }

void countLeft()
{
 hitsLeft++;
}

void countRight()
{
 hitsRight++;
}

int raspRX() {
  while (true){
  if(Serial.available()>0){
       zot = (int) Serial.read();
       return(zot);
       } } }
       
void raspTX(int z) {
  Serial.println (z); }



