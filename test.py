from Pubnub import Pubnub
import RPi.GPIO as GPIO
import time
import sys


loopcount = 0

Publish_key = len(sys.argv) > 1 and sys.argv[1] or 'demo'
subscribe_key = len(sys.argv) > 2 and sys.argv[2] or 'demo'
secret_key = len(sys.argv) > 3 and sys.argv[3] or 'demo'
cipher_key = len(sys.argv) > 4 and sys.argv[4] or ''
ssl_on = len(sys.argv) > 5 and bool(sys.argv[5]) or False

pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key,secret_key=secret_key, cipher_key=cipher_key, ssl_on=ssl_on)
channel = 'Rangefinder'

TRIG = 20
ECHO = 26

print("Distance Measurement in Progess")
GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)
print("Waiting for sensor to settle.")

time.sleep(2)

while True:
   GPIO.output(TRIG, True)
   time.sleep(0.00001)
   GPIO.output(TRIG, False)

   print("before pulse start")  # debug statement
    pulse_start = time.time()
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

while GPIO.input(ECHO)==1:
    pulse_end = time.time()
print("after pulse")  # debug statement
pulse_duration = pulse_end - pulse_start


  distance = round(distance, 2)
  loopcount+=1

    print("Distance:",distance,"cm")
  print("Measured distance")
  message = {['distance', distance]}
  print pubnub.publish(channel, message)
  time.sleep(1)

  GPIO.cleanup()
sys.exit()
