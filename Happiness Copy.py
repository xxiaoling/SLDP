#Section 1: Setup
# Importing Packages---------------------------------------------------------
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import pyttsx3

engine = pyttsx3.init()

# GPIO Setup
GPIO.setwarnings(False)

# INSERT CODE HERE - Set variable for servoPin
servoPin = 17

# INSERT CODE HERE - Set GPIO mode to GPIO.BCM
GPIO.setmode(GPIO.BCM)

# INSERT CODE HERE - Set servoPin as GPIO.OUT
GPIO.setup(servoPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 100)


#Section 2: Pi Camera Setup---------------------------------------------------------
while(True):
  # INSERT CODE: Make a camera object
  camera = PiCamera()
  # INSERT CODE: Set camera resolution
  camera.resolution = (640, 480)
  # INSERT CODE: Set camera frame rate
  rawCapture = PiRGBArray(camera, size=(640,480))
  pixels = 640*480
  camera.framerate = 30
    
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    #SECTION 3: Color Detection---------------------------------------------------------
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Red Color Detection:
    red_lower = np.array([160,70,50])
    red_upper = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    result_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    #Green Color Detection:   
    # INSERT CODE: Define green lower boundary
    green_lower = np.array([20, 40, 60])
    # INSERT CODE: Define green upper boundary
    green_upper = np.array([102, 255, 255])
    # INSERT CODE: Create green mask
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    # INSERT CODE: Use bitwise_and to isolate green color from the video
    result_green = cv2.bitwise_and(frame, frame, mask=green_mask)
    #Result:
    # INSERT CODE: Combine the results so both red and green colors are isolated from the video using bitwise_or
    result_red_and_green = cv2.bitwise_or(result_red, result_green)

    # INSERT CODE: Display the final result
    cv2.imshow("Red and Green Detection in Real-Time", result_red_and_green)

    rawCapture.truncate(0) #Stop rawCapture to clear the stream in preparation for the next frame
  
    #SECTION 4: Servo Control with Color Detection----------------------------------------------------
    if cv2.waitKey(5) & 0xFF == ord('q'):
      camera.close()
      if(cv2.countNonZero(red_mask)>cv2.countNonZero(green_mask)) and cv2.countNonZero(red_mask)>(0.25*pixels):
        print('Red detected')
        #INSERT CODE: Start clockwise rotation; dutycycle = 5
        pwm.start(5)
        engine.say('Red detected')
        engine.runAndWait()
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(green_mask)) and cv2.countNonZero(green_mask)>(0.25*pixels): #INSERT CONDITIONS HERE: (The frame should have more green pixels than red, and at least 25% of the pixels should be green):
        print('Green detected')
        #INSERT CODE: Start counterclockwise rotation; dutycycle = 55
        pwm.start(55)
        engine.say('Green detected')
        engine.runAndWait()
      else:
        print('Color not detected')
        #INSERT CODE: Stop servo rotation
        pwm.stop()
        engine.say('Color not detected')
        engine.runAndWait()
      print('------------------------')
      break
GPIO.cleanup()

