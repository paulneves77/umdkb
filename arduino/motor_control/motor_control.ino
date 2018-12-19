/*
  motor_control
*/

#include <stdbool.h>

#define PUL_PIN 11
#define DIR_PIN 12
#define PULSE_TIME 3

void setup() {
  pinMode(PUL_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(9600);
}

void rotate(int steps) {
  int dir = HIGH;
  if (steps < 0) {
    dir = LOW;
    steps = -steps;
  } 

  pinMode(DIR_PIN, dir);
  for (int i=0; i<steps; i++) {
    pinMode(PUL_PIN, HIGH);
    delay(PULSE_TIME);
    pinMode(PUL_PIN, LOW);
  }
}

void loop() {
  rotate(1000);
  delay(3000);
  rotate(-1000);
}
