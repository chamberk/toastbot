import RPi.GPIO as GPIO
import time
import sys
import toast_request as toast

toastLoopBool = True

# FUNCTIONS !!
def toastLoop():
    loopcount = 0

    GPIO.setmode(GPIO.BCM)

    #Variables for pins
    TRIG = 20
    ECHO = 26

    #Pin setup for input and output
    # print("Distance Measurement in Progress")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)


    # Each shot works by sending a 10-microsecond pulse at around 40khz,
    # marking the time at which the pulse is sent and then,
    # subsequentially, when the reflected signal is detected.
    # To ensure accuracy, we must first settle the trigger and wait:
    GPIO.output(TRIG,False)
    print("Waiting for sensor to settle.")

    time.sleep(2)

    #Continuously checking for range
    while True:
     GPIO.output(TRIG, True)
    # print("inside checking range")
     time.sleep(0.1)
     GPIO.output(TRIG, False)



    # waiting the Echo
    # print("before pulse start")  # debug statement
     pulse_start = time.time()
     while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    # Pulse received
     while GPIO.input(ECHO)==1:
      pulse_end = time.time()
     #  print("after pulse")  # debug statement
      pulse_duration = pulse_end - pulse_start

    # Calculating distance
     distance = pulse_duration*17150
     distance = round(distance, 2)
     loopcount+=1

    #Publish distance to some other thing
     toastCount = 0
     if distance > 3000:
      toastCount+=1
      print("TOAST IS DONEEEEEEEE")
      toast.sendsms_task()
      print("SMS SENT")
      GPIO.cleanup()
      break;
     else:
      toastCount = 0

    # clean up and log out
    GPIO.cleanup()
    #sys.exit()

if __name__ == '__main__':
  while toastLoopBool:
    toastLoop()
