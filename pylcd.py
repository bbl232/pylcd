#!/usr/bin/env python
import math
import time
import datetime
import sys
import RPi.GPIO as GPIO
import threading
 
import Adafruit_CharLCD as LCD
from random import randint

lcd_rs        = 27
lcd_en        = 5
lcd_d4        = 6
lcd_d5        = 13
lcd_d6        = 19
lcd_d7        = 26
lcd_bl        = 22

exit=0
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_bl, enable_pwm=True)
lock = threading.RLock()

def scrolling_message(text, sltime):
  print("Scrolling message: " + text)
  lock.acquire()
  lcd.set_cursor(0,1)
  lcd.message("                ")
  lcd.set_cursor(0,1)
  lcd.message(text)
  lock.release()
  time.sleep(2.0)
  for i in range(0,len(text)-15):
    lock.acquire()
    lcd.set_cursor(0,1)
    lcd.message(text[i:i+16])
    lock.release()
    time.sleep(0.4)
  time.sleep(sltime)
  lock.acquire()
  lcd.set_cursor(0,1)
  lcd.message("                ")
  lock.release()

def message(text, sltime=2.0):
  if len(text) > 16:
    scrolling_message(text, sltime)
  else:
    print("Message: " + text)
    lock.acquire()
    lcd.set_cursor(0,1)
    lcd.message("                ")
    lcd.set_cursor(0,1)
    lcd.message(text)
    lock.release()
    time.sleep(sltime)
    lock.acquire()
    lcd.set_cursor(0,1)
    lcd.message("                ")
    lock.release()


def button_1(channel):
  print("Button 1 press detcted")
  message("HELLO THERE THIS IS A REALLY LONG MESSAGE USING A FUNCTION!")

def button_2(channel):
  print("Button 2 press detcted")
  message("BTN2 is Unmapped")

def button_3(channel):
  print("Button 3 press detcted")
  message("BTN3 Unmapped")

def button_4(channel):
  global exit
  print("Button 4 press detcted... shutting down")
  message("Looks like we're done here!")
  exit = 1

def main():
  global exit
  btn_1         = 23
  btn_2         = 24
  btn_3         = 25
  btn_4         = 12

  GPIO.setup([btn_1, btn_2, btn_3, btn_4], GPIO.IN)

  lcd.clear()
  lcd.set_backlight(0)

  GPIO.add_event_detect(btn_1, GPIO.RISING, callback=button_1, bouncetime=500)  
  GPIO.add_event_detect(btn_2, GPIO.RISING, callback=button_2, bouncetime=500)  
  GPIO.add_event_detect(btn_3, GPIO.RISING, callback=button_3, bouncetime=500)  
  GPIO.add_event_detect(btn_4, GPIO.RISING, callback=button_4, bouncetime=500)  

  while exit == 0:
    now = time.strftime("%m/%d %I:%M:%S%p")
    nows = time.strftime("%S")
    lock.acquire()
    lcd.set_cursor(0,0)
    lcd.message(now)
    lock.release()
    time.sleep(1)

  lcd.clear()

if __name__ == "__main__":
  main()
