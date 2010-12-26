int ir_pin = 5;				 //Sensor pin 1 wired through a 220 ohm resistor
int led_pin = 6;				   //"Ready to Receive" flag, not needed but nice
int debug = 0;				   //Serial connection must be started to debug
int start_bit = 4800;			 //Start bit threshold (Microseconds)
int bin_1 = 1200;				   //Binary 1 threshold (Microseconds)
int bin_0 = 600;				     //Binary 0 threshold (Microseconds)
int dataOut = 0;
int guardTime = 300;
int end_bit = 2400;

byte pNum = 4;
byte pTeam = 2;
byte pMod = 0;

void setup() {
    pinMode(led_pin, OUTPUT);		 //This shows when we're ready to recieve
    pinMode(ir_pin, OUTPUT);
    digitalWrite(led_pin, LOW);	 //not ready yet
    digitalWrite(ir_pin, LOW);	  //not ready yet
    Serial.begin(57600);
}

void oscillationWrite(int pin, int time) {
    for(int i = 0; i <= time/18; i++) {
        digitalWrite(pin, HIGH);
        delayMicroseconds(9);
        digitalWrite(pin, LOW);
        delayMicroseconds(9);
    }
}

int sendIR() {
    int encoded[10];
    for (int i=0; i<4; i++) {

        encoded[i] = pNum >>i & B1;
    }
    for (int i=4; i<7; i++) {
      encoded[i] = pTeam>>(i-4) & B1;
     Serial.println(encoded[i]); 
    }
    for (int i=7; i<10; i++) {
        encoded[i] = pMod>>(i-7) & B1;
    }
    
    oscillationWrite(ir_pin, start_bit);
    // send separation bit
    digitalWrite(ir_pin, HIGH);
    delayMicroseconds(guardTime);

    for (int i=0; i<=9; i++) {
        if (encoded[i] == 0) oscillationWrite(ir_pin, bin_0);
        else oscillationWrite(ir_pin, bin_1);
        // send separation bit
        digitalWrite(ir_pin, HIGH);
        delayMicroseconds(guardTime);
    }
    oscillationWrite(ir_pin, end_bit);
    delay(5);
    digitalWrite(ir_pin, LOW);				    //Return key number
}


void loop() {
    sendIR();		 //Fetch the key
    Serial.println("Key Sent: ");
    delay(1000);
}





