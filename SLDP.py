#Section 1: Setup
# Importing Packages---------------------------------------------------------
# INSERT CODE HERE
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setwarnings(False)

# INSERT CODE HERE - Set variable for servoPin
servoPin = 17
# INSERT CODE HERE - Set GPIO mode to GPIO.BCM

# INSERT CODE HERE - Set servoPin as GPIO.OUT
pwm = GPIO.PWM(servoPin, 100)


#Section 2: Pi Camera Setup---------------------------------------------------------
while(True):
  # INSERT CODE: Make a camera object
  # INSERT CODE: Set camera resolution
  # INSERT CODE: Set camera frame rate
  rawCapture = PiRGBArray(camera, size=(640,480))
  pixels = 640*480
    
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
    # INSERT CODE: Define green upper boundary
    # INSERT CODE: Create green mask
    # INSERT CODE: Use bitwise_and to isolate green color from the video

    #Result:
    # INSERT CODE: Combine the results so both red and green colors are isolated from the video using bitwise_or

    # INSERT CODE: Display the final result

    rawCapture.truncate(0) #Stop rawCapture to clear the stream in preparation for the next frame
  
    #SECTION 4: Servo Control with Color Detection----------------------------------------------------
    if cv2.waitKey(5) & 0xFF == ord('q'):
      camera.close()
      if(cv2.countNonZero(red_mask)>cv2.countNonZero(green_mask)) and cv2.countNonZero(red_mask)>(0.25*pixels):
        print('Red detected')
        #INSERT CODE: Start clockwise rotation; dutycycle = 5
        
      elif #INSERT CONDITIONS HERE: (The frame should have more green pixels than red, and at least 25% of the pixels should be green):
        print('Green detected')
        #INSERT CODE: Start counterclockwise rotation; dutycycle = 55
    
      else:
        print('Neither red nor green detected')
        #INSERT CODE: Stop servo rotation
        
      print('------------------------')
      break
GPIO.cleanup()
