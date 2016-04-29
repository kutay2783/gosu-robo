 void setup() {
  pinMode(30, OUTPUT);
  pinMode(32, OUTPUT);
  digitalWrite(30, HIGH);
  digitalWrite(32, HIGH);
  }
void loop() {
  digitalWrite(32, LOW);
  delay(100);
  digitalWrite(32, HIGH);
  delay(100);
  }  
