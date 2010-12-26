
const int PACKETLEN = 6;
int gameState = 0;
bool infoset = false;

const int sLed1 = 5;
const int sLed2 = 6;
const int sLed3 = 7;
int pNum = 0;
int pTeam = 0;

void setup() {
  pinMode(sLed1,OUTPUT);
  pinMode(sLed2,OUTPUT);
  pinMode(sLed3,OUTPUT);
  Serial.begin(57600);
  String test = "On3";
  Serial.println(4);
  randomSeed(analogRead(0));
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
        randomShots();
        delay(2500);
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

    






