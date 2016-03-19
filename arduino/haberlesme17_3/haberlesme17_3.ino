int var,x;

void setup (){
    Serial.begin (9600);
    pinMode (13, OUTPUT);
}
void loop(){
  if(raspRX()==20){
    raspTX (5); }
      
  while (true){
     if(Serial.available()>0){
       var = (int) Serial.read();
       if(var==15){
       digitalWrite(13,HIGH);    
           break; }  } 
     }
 }
   
     
int raspRX() {
  while (true){
  if(Serial.available()>0){
       var = (int) Serial.read();
       return(var);
       } } }
       
void raspTX(int z) {
  Serial.println (z); }
