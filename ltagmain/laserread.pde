int ir_pin = 12;				 //Sensor pin 1 wired through a 220 ohm resistor
int led_pin = 13;
int start_bit = 4000;			 //Start bit threshold (Microseconds)
int bin_1 = 1000;				   //Binary 1 threshold (Microseconds)
int bin_0 = 400;				     //Binary 0 threshold (Microseconds)
int debug =1 ;
int end_bit = 2000;
int ret[3];

void setup() {
 pinMode(led_pin, OUTPUT);		 //This shows when we're ready to receive
 pinMode(ir_pin, INPUT);
 digitalWrite(led_pin, LOW);	 //not ready yet
 Serial.begin(57600);
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

void getIR() {
 int player[4];
 int team[3];
 int mod[3];
 int end;
 int start =pulseIn(ir_pin, LOW, 50);  
 if(start < start_bit) {
    if(start>0)
    {
    Serial.print("!!! ");
    Serial.println(start);
    }
    ret[0] = -1;
    return;
 }
 digitalWrite(led_pin, HIGH);     //Ok, i'm ready to recieve
 player[0] = pulseIn(ir_pin, LOW);	 //Start measuring bits, I only want low pulses
 player[1] = pulseIn(ir_pin, LOW);
 player[2] = pulseIn(ir_pin, LOW);
 player[3] = pulseIn(ir_pin, LOW);
 team[0] = pulseIn(ir_pin, LOW);
 team[1] = pulseIn(ir_pin, LOW);
 team[2] = pulseIn(ir_pin, LOW);
 mod[0] = pulseIn(ir_pin, LOW);
 mod[1] = pulseIn(ir_pin, LOW);
 mod[2] = pulseIn(ir_pin, LOW);
 end = pulseIn(ir_pin, LOW);

 if(end < end_bit) {
     Serial.print(end);
     Serial.println(" : bad end bit");
     ret[0] = -1;
     return;
 }

Serial.println("---player---");
 for(int i=0;i<=3;i++) {
     Serial.println(player[i]);
     if(player[i] > bin_1) {
         player[i] = 1;
     } else if (player[i] > bin_0) {
         player[i] = 0;
     } else {
         // Since the data is neither zero or one, we have an error
         Serial.println("unknown player");
         ret[0] = -1;
         return;
     }
 }
  ret[0]=convert(player);
  Serial.println(ret[0]);

  Serial.println("---team---");
  for(int i=0;i<=2;i++) {
    Serial.println(team[i]);
    if(team[i] > bin_1) {
      team[i] = 1;
    } else if (team[i] > bin_0) {
      team[i] = 0;
    } else {
      // Since the data is neither zero or one, we have an error
      Serial.println("unknown action");
      ret[0] = -1;
      return;
    }
  }
  ret[1]=convert(team);
  Serial.println(ret[1]);

  Serial.println("---mod---");
  for(int i=0;i<=2;i++) {
    Serial.println(mod[i]);
    if(mod[i] > bin_1) {
      mod[i] = 1;
    } else if (mod[i] > bin_0) {
      mod[i] = 0;
    } else {
      // Since the data is neither zero or one, we have an error
      Serial.println("unknown action");
      ret[0] = -1;
      return;
    }
  }
  ret[2]=convert(mod);
  Serial.println(ret[2]);
  return;
 }

void loop() {
    getIR();
    if (ret[0] != -1) {
        Serial.print("Who: ");
        Serial.print(ret[0]);
        Serial.print(" What: ");
        Serial.println(ret[1]);
        }
}

