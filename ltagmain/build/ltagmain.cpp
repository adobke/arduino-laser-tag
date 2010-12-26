#include <WProgram.h>

int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

#line 1 "build/ltagmain.pde"
const int PACKETLEN = 6; //for serial
int gameState = 0;
bool infoset = false;

boolean debug = true;

const int sLed1 = 5;
const int sLed2 = 6;
const int sLed3 = 7;
const int irPin = 8;
const int irRec = 12;
const int trigger = 9;

const int startBit= 4800;
const int endBit = 2400;
const int bit0 = 600;
const int bit1 = 1200;

const int waitTime = 300;

const int pulseT = 18; 
const int pulseTd = 9; 

byte pNum = 0;
byte pTeam = 0;
byte pMod = 0;

const int arrayLen = 12;
int userArray[arrayLen];
int ret[3]; // things return when shot.


void setup() {
  pinMode(sLed1,OUTPUT);
  pinMode(sLed2,OUTPUT);
  pinMode(sLed3,OUTPUT);
  pinMode(irPin,OUTPUT);
  pinMode(irRec,INPUT);
  pinMode(trigger,INPUT);
      
  Serial.begin(57600);
    
}

void setupArrays(){
    for (int i=0; i<4; i++) {
        userArray[i] = pNum >>i & B1;
    }
    for (int i=4; i<8; i++) {
        userArray[i] = pTeam>>(i-4) & B1;
    }
    for (int i=8; i<11; i++) {
        userArray[i] = pMod>>(i-9) & B1;
    }
}


void pulse(int time) {
    for(int i = 0; i <= time/pulseT; i++) {
        digitalWrite(irPin, HIGH);
        delayMicroseconds(pulseTd);
        digitalWrite(irPin, LOW);
        delayMicroseconds(pulseTd);
    }
}


void sendIr() {
    pulse(startBit);
    // send separation bit
    digitalWrite(irPin, HIGH);
    delayMicroseconds(waitTime);

    for (int i=0; i<arrayLen; i++) {
        if (userArray[i] == 0) pulse(bit0);
        else pulse(bit1);
        // send separation bit
        digitalWrite(irPin, HIGH);
        delayMicroseconds(waitTime);
    }
    pulse(endBit);
    delay(5);
    digitalWrite(irPin, LOW);				    
}

int convert(int bits[]) {
  int result = 0;
  int seed   = 1;
  for(int i=3;i>=0;i--) {
    if(bits[i] == 1) {
      result += seed;
    }
    seed = seed * 2;
  }
  return result;
}

void readSensors() {
    int player[4];
    int team[4];
    int mod[4];
    int end;
    int start = pulseIn(irPin, LOW, 50);  
    if(start < startBit) {
        if(start>0)
        {
            if(debug) Serial.print("!!! ");
            if(debug) Serial.println(start);
        }
        ret[0] = -1;
        return;
    }
    player[0] = pulseIn(irPin, LOW);	 //Start measuring bits, I only want low pulses
    player[1] = pulseIn(irPin, LOW);
    player[2] = pulseIn(irPin, LOW);
    player[3] = pulseIn(irPin, LOW);
    team[0] = pulseIn(irPin, LOW);
    team[1] = pulseIn(irPin, LOW);
    team[2] = pulseIn(irPin, LOW);
    team[3] = pulseIn(irPin, LOW);
    mod[0] = pulseIn(irPin, LOW);
    mod[1] = pulseIn(irPin, LOW);
    mod[2] = pulseIn(irPin, LOW);
    mod[3] = pulseIn(irPin, LOW);
    end = pulseIn(irPin, LOW);

    if(end < endBit) {
        if(debug) Serial.print(end);
        if(debug) Serial.println(" : bad end bit");
        ret[0] = -1;
        return;
    }

    if(debug) Serial.println("---player---");
    for(int i=0;i<=3;i++) {
        if(debug) Serial.println(player[i]);
        if(player[i] > bit1) {
            player[i] = 1;
        } else if (player[i] > bit0) {
            player[i] = 0;
        } else {
            // Since the data is neither zero or one, we have an error
            if(debug) Serial.println("unknown player");
            ret[0] = -1;
            return;
        }
    }
    ret[0]=convert(player);
    if(debug) Serial.println(ret[0]);

    if(debug) Serial.println("---team---");
    for(int i=0;i<=3;i++) {
        if(debug) Serial.println(team[i]);
        if(team[i] > bit1) {
            team[i] = 1;
        } else if (team[i] > bit0) {
            team[i] = 0;
        } else {
            // Since the data is neither zero or one, we have an error
            if(debug) Serial.println("unknown action");
            ret[0] = -1;
            return;
        }
    }
    ret[1]=convert(team);
    if(debug) Serial.println(ret[1]);

    if(debug) Serial.println("---mod---");
    for(int i=0;i<=3;i++) {
        if(debug) Serial.println(mod[i]);
        if(mod[i] > bit1) {
            mod[i] = 1;
        } else if (mod[i] > bit0) {
            mod[i] = 0;
        } else {
            // Since the data is neither zero or one, we have an error
            if(debug) Serial.println("unknown action");
            ret[0] = -1;
            return;
        }
    }
    ret[2]=convert(mod);
    if(debug) Serial.println(ret[2]);
    return;
}

void readCommand(char* command) {
  delay(1);
  byte nextByte;
  int i = 0;
  while( Serial.available() ) {
    delay(1);
    nextByte = Serial.read();  
    if(nextByte == '>')
    {
      return; 
    }
    command[i++] = nextByte;

    if(i>PACKETLEN-1)
    {
      return;
    }
  }
}

void process(char* command)
{
  if(command[0]=='a')
  {
    Serial.println(gameState);
  }
  
  if(command[0]=='a' && command[1]=='i')
  {
    Serial.print("pnum: ");
    Serial.println(pNum);
    Serial.print("pTeam: ");
    Serial.println(pTeam);
  }

  if(command[0]=='s')
  {
    gameState = 3;
  }
  
  if(command[0]=='i')
  {
    byte pNumtemp = command[1];
    byte pTeamtemp = command[2];
    char parr[] = {pNumtemp,'\0'};
    pNum = atoi(parr);
    parr[0] = pTeamtemp;
    pTeam = atoi(parr);
    setupArrays(); 
    infoset = true;
  }

  if(command[0]=='p')
  {
    gameState = 2;
  }
}

void readSerial()
{
  char command[PACKETLEN];
  if(Serial.available())
  {
    byte nextByte = Serial.read();
    if(nextByte == '<') 
    {
      readCommand(command);
      process(command);
    }
  }
}

void writeSerial(String data)
{
  Serial.println("<" + data + ">");
}


void randomShots()
{
  long p1 = random(16);
  int pp1 = (byte) p1;
  delay(50);
  long p2 = random(16);
  int pp2 = (byte) p2;
  Serial.print("<k ");
  Serial.print(pp1);
  Serial.print(" ");
  Serial.print(pp2);
  Serial.println(">");
}

void wasShot()
{
  Serial.print("<k ");
  Serial.print(ret[0]);
  Serial.print(" ");
  Serial.print(pNum);
  Serial.print(" ");
  Serial.print(ret[2]);
  Serial.println(">");
}

void fastblink()
{
  digitalWrite(sLed1,HIGH);
  digitalWrite(sLed2,HIGH);
  digitalWrite(sLed3,HIGH); 
  delay(50);
  digitalWrite(sLed1,LOW);
  digitalWrite(sLed2,LOW);
  digitalWrite(sLed3,LOW); 
  delay(50);
}

void slowblink()
{
  digitalWrite(sLed1,HIGH);
  digitalWrite(sLed2,HIGH);
  digitalWrite(sLed3,HIGH); 
  delay(150);
  digitalWrite(sLed1,LOW);
  digitalWrite(sLed2,LOW);
  digitalWrite(sLed3,LOW); 
  delay(150);
}

void loop() {
    readSerial();
    switch (gameState) {
      case 0:
      //staging
        digitalWrite(sLed1,HIGH);
        digitalWrite(sLed2,HIGH);
        digitalWrite(sLed3,HIGH);
        if(infoset)
        {
         gameState=1; 
        }
        break;
      case 1:
      // loaded. game not started
        slowblink();
        break;
      case 2:
      // paused
        fastblink();
        break;
      case 3:
      // playing
        if(digitalRead(trigger) == HIGH)
        {
            sendIr();
        }
        readSensors();
        if (ret[0] != -1) {
            if(debug) Serial.print("Who: ");
            if(debug) Serial.print(ret[0]);
            if(debug) Serial.print(" Team: ");
            if(debug) Serial.println(ret[1]);
            if(debug) Serial.print(" Mod: ");
            if(debug) Serial.println(ret[2]);
            wasShot();
        }
        //randomShots();
        //delay(2500);
        
        
        digitalWrite(sLed1,LOW);
        digitalWrite(sLed2,HIGH);
        digitalWrite(sLed3,LOW);
        break;
      default:
        digitalWrite(sLed1,LOW);
        digitalWrite(sLed2,LOW);
        digitalWrite(sLed3,HIGH);
        break;
    }
}

    






