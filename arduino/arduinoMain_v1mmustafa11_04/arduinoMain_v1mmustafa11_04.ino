
#include <PID_v1.h> 
///////define parts/////////
#define enablePin  52 
#define encoderRight  0
#define encoderLeft 1
#define controlLed 13
#define echoPin 30
#define trigPin 31

#define motorRFA 4  // sag motor sari pin//sag ileri aktif
#define motorRBA 5  // sag motor siyah pin
#define motorLBA 7  // sol motor kirmizi pin
#define motorLFA 6  // sol motor siyah pin
#define motorSpeed 125
volatile int hitsRight = 0;
volatile int hitsLeft = 0;
long distance;
int raspMessage,roundDirection,var, zot, temp1, temp2,projeStart; 
double SetPointStraight=0, SetPointRound=0;
double InputStraight, InputRound;
double  OutputStraight, OutputRound;
int encoderDifference,motorSpeedLast=motorSpeed; 
volatile unsigned long last_microsRight, last_microsLeft;
long debouncing_time =25;
PID myPIDStraight(&InputStraight, &OutputStraight, &SetPointStraight, 13, 0.2, 0.5, DIRECT);
PID myPIDRound(&InputRound, &OutputRound, &SetPointRound, 13, 0.2, 0.5, DIRECT);

void setup() {
  Serial.begin(9600);  
  /*pinMode(encoderRight, INPUT);	// analog read icin simdilik dursun!!
  pinMode(encoderLeft, INPUT);*/	// sistem basladiginda test edebilmek icin encoderleri	
  pinMode(controlLed, OUTPUT);
  attachInterrupt(4, countLeft, CHANGE);
  attachInterrupt(5, countRight, CHANGE); 
  pinMode(motorRFA, OUTPUT);
  pinMode(motorRBA, OUTPUT);
  pinMode(motorLBA, OUTPUT);
  pinMode(motorLFA, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  /*analogWrite(motorRFA, 0);
  analogWrite(motorRBA, 0);
  analogWrite(motorLBA, 0);
  analogWrite(motorLFA, 0);*/
  digitalWrite(controlLed, LOW);
  digitalWrite (trigPin,LOW);
 
  }

void loop() {
 
   while (true){
     if(raspRX()==1)
           break;     
  }
  while (true){
    projeStart=digitalRead(echoPin);
    if(projeStart==1){
      raspTX(2);
      break;}
  }
   
    while (true){
     
        switch (raspRX()){
        case 5:  roundAroundCW();
                  break;
        case 6:  roundAroundCCW();
                  break;
        case 7:  goStraight();
                  break;
        case 8:  incRightRasp();
                  break;
        case 9:  incLeftRasp();
                  break;
        case 10: returnHits();
                  break;
        }
     }
  
}
////////////Round CW///////////
void roundAroundCW (){ 
 myPIDRound.SetMode(AUTOMATIC);  
  raspTX(20);
  temp1=raspRX();   
  raspTX(21);  
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  InputRound = hitsLeft - hitsRight ;  
  analogWrite(motorRBA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var) &&  (hitsRight<var)){ 
    InputRound = hitsLeft - hitsRight ; 	
    myPIDRound.Compute();
    analogWrite(motorRBA, motorSpeed-OutputRound);  
  }
  analogWrite(motorRBA, 0);
  raspTX(3);
  digitalWrite(controlLed,LOW);
  analogWrite(motorLFA, 0);
}


  /////////round CCW/////////////////
  void roundAroundCCW (){
   myPIDRound.SetMode(AUTOMATIC); 
  raspTX(40);
  temp1=raspRX();   
  raspTX(41);  
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
  InputRound = hitsLeft - hitsRight ;  
  analogWrite(motorRFA, 125);
  analogWrite(motorLBA, 125);
  digitalWrite(controlLed,HIGH);
    while((hitsLeft<var) &&  (hitsRight<var)){ 
      InputRound = hitsLeft - hitsRight ; 	
      myPIDRound.Compute();
      analogWrite(motorRFA, motorSpeed-OutputRound);  
  }
  analogWrite(motorRFA, 0);
  raspTX(43);
  digitalWrite(controlLed,LOW);
  analogWrite(motorLBA, 0);
 }

 ////////////Go Straight//////////// 
void goStraight(){
  myPIDStraight.SetMode(AUTOMATIC); 
  raspTX(30);  
  temp1=raspRX();  
  raspTX(31);
  temp2=raspRX();
  var=temp1*250+temp2;
  hitsLeft=0;
  hitsRight=0;
   InputStraight = hitsLeft - hitsRight ;
  analogWrite(motorRFA, 125);
  analogWrite(motorLFA, 125);
  digitalWrite(controlLed,HIGH);
  while((hitsLeft<var)&&( hitsRight<var)){
    InputStraight = hitsLeft - hitsRight ;      
    myPIDStraight.Compute();
    analogWrite(motorRFA, motorSpeed-OutputStraight);    	
      }
    
    
      analogWrite(motorRFA, 0);
      digitalWrite(controlLed,LOW);
      raspTX(33);
      analogWrite(motorLFA, 0);
  }
///////////////Return Hits/////////  
  
void returnHits() {
  raspTX(2);
  delay(2);
  raspTX((hitsLeft+hitsRight)/500);
  delay(2);
  raspTX((hitsLeft+hitsRight)%250);

}
//////////incRightRasp//////////////
void incLeftRasp(){
  raspTX(2);
  temp1=raspRX();
  hitsLeft=hitsLeft+temp1;
  raspTX(3);
}
void incRightRasp(){
  raspTX(2);
  temp1=raspRX();
  hitsRight=hitsRight+temp1;
  raspTX(3);
}

////////arduino message protocol//////////
  
int raspRX() {
  while (true){
  if(Serial.available()>0){
       zot = (int) Serial.read();
       return(zot);
       } } }
       
void raspTX(int z) {  
  Serial.println (z); }
  
////////encoder interruppt part//////////

void countLeft()
{
  if((long)(micros()-last_microsLeft)>=debouncing_time*1000) {
  InterruptLeft();
  last_microsLeft=micros(); }
}
void InterruptLeft() {
   hitsLeft++; }

void countRight()
{
  if((long)(micros()-last_microsRight)>=debouncing_time*1000) {
  InterruptRight();
  last_microsRight=micros(); }
}
void InterruptRight() {
   hitsRight++; }


