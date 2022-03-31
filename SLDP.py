#Section 1: Setup
# Importing Packages---------------------------------------------------------
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import pyttsx3
import time

engine = pyttsx3.init()
start_time = time.time()

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
    red_lower = np.array([160, 70, 50])
    red_upper = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    result_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    #Orange Color Detection:
    orange_lower = np.array([10, 50, 20])
    orange_upper = np.array([23, 255, 255])
    #orange_lower = np.array([200, 190, 1])
    #orange_upper = np.array([255, 255, 18])
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
    result_orange = cv2.bitwise_and(frame, frame, mask=orange_mask)

    #Yellow Color Detection:
    yellow_lower = np.array([24, 70, 50])
    yellow_upper = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    result_yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    #Green Color Detection:   
    # INSERT CODE: Define green lower boundary
    green_lower = np.array([36, 40, 60])
    # INSERT CODE: Define green upper boundary
    green_upper = np.array([75, 255, 255])
    # INSERT CODE: Create green mask
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    # INSERT CODE: Use bitwise_and to isolate green color from the video
    result_green = cv2.bitwise_and(frame, frame, mask=green_mask)
    
    #Cyan Color Detection:
    cyan_lower = np.array([85, 50, 50])
    cyan_upper = np.array([99, 255, 255])
    #cyan_lower = np.array([125, 0, 255])
    #cyan_upper = np.array([0, 125, 255])
    cyan_mask = cv2.inRange(hsv, cyan_lower, cyan_upper)
    result_cyan = cv2.bitwise_and(frame, frame, mask=cyan_mask)
    
    #Blue Color Detection:
    blue_lower = np.array([100, 50, 50])
    blue_upper = np.array([130, 255, 255])
    #blue_lower = np.array([125, 0, 255])
    #blue_upper = np.array([0, 125, 255])
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    result_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    #magenta Color Detection:
    #magenta_lower = np.array([130, 50, 70])
    #magenta_upper = np.array([160, 255, 255])
    magenta_lower = np.array([140, 50, 75])
    magenta_upper = np.array([155, 255, 255])
    magenta_mask = cv2.inRange(hsv, magenta_lower, magenta_upper)
    result_magenta = cv2.bitwise_and(frame, frame, mask=magenta_mask)

    #Result:
    # INSERT CODE: Combine the results so both red and green colors are isolated from the video using bitwise_or
    result_red_and_green = cv2.bitwise_or(result_red, result_green)
    result_blue_and_orange = cv2.bitwise_or(result_blue, result_orange)
    result_yellow_and_magenta = cv2.bitwise_or(result_yellow, result_magenta)
    result_some_colors = cv2.bitwise_or(result_red_and_green, result_blue_and_orange)
    result_more_colors = cv2.bitwise_or(result_some_colors, result_cyan)
    result_colors = cv2.bitwise_or(result_more_colors, result_yellow_and_magenta)

    # INSERT CODE: Display the final result
    #cv2.imshow("Color Detection in Real-Time", result_red_and_green)
    #cv2.imshow("Color Detection in Real-Time", result_blue_and_orange)
    #cv2.imshow("Color Detection in Real-Time", result_yellow_and_magenta)
    cv2.imshow("Color Detection in Real-Time", result_colors)

    rawCapture.truncate(0) #Stop rawCapture to clear the stream in preparation for the next frame
  
    #SECTION 4: Servo Control with Color Detection----------------------------------------------------
    if cv2.waitKey(5) & 0xFF == ord('q'):
    #if (time.time() - start_time >= 3) and (cv2.waitKey(3)):
      camera.close()
      # RED
      if(cv2.countNonZero(red_mask)>cv2.countNonZero(green_mask) and cv2.countNonZero(red_mask)>cv2.countNonZero(orange_mask) and cv2.countNonZero(red_mask)>cv2.countNonZero(yellow_mask) and cv2.countNonZero(red_mask)>cv2.countNonZero(blue_mask) and cv2.countNonZero(red_mask)>cv2.countNonZero(magenta_mask)) and cv2.countNonZero(red_mask)>(0.25*pixels):
        print('Red detected')
        #INSERT CODE: Start clockwise rotation; dutycycle = 5
        pwm.start(5)
        engine.say('Red detected')
        time.sleep(3)
        print('Red matches with Orange')
        engine.say('Red matches with Orange')
        engine.runAndWait()
      # GREEN
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(green_mask) and cv2.countNonZero(orange_mask)<cv2.countNonZero(green_mask) and cv2.countNonZero(yellow_mask)<cv2.countNonZero(green_mask) and cv2.countNonZero(blue_mask)<cv2.countNonZero(green_mask) and cv2.countNonZero(magenta_mask)<cv2.countNonZero(green_mask)) and cv2.countNonZero(green_mask)>(0.25*pixels): #INSERT CONDITIONS HERE: (The frame should have more green pixels than red, and at least 25% of the pixels should be green):
        print('Green detected')
        #INSERT CODE: Start counterclockwise rotation; dutycycle = 55
        pwm.start(55)
        engine.say('Green detected')
        engine.runAndWait()
      # ORANGE
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(orange_mask) and cv2.countNonZero(green_mask)<cv2.countNonZero(orange_mask) and cv2.countNonZero(yellow_mask)<cv2.countNonZero(orange_mask) and cv2.countNonZero(blue_mask)<cv2.countNonZero(orange_mask) and cv2.countNonZero(magenta_mask)<cv2.countNonZero(orange_mask)) and cv2.countNonZero(orange_mask)>(0.25*pixels):
        print('Orange detected')
        
        pwm.start(5)
        engine.say('Orange detected')
        engine.runAndWait()
      # YELLOW
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(yellow_mask) and cv2.countNonZero(green_mask)<cv2.countNonZero(yellow_mask) and cv2.countNonZero(orange_mask)<cv2.countNonZero(yellow_mask) and cv2.countNonZero(blue_mask)<cv2.countNonZero(yellow_mask) and cv2.countNonZero(magenta_mask)<cv2.countNonZero(yellow_mask)) and cv2.countNonZero(yellow_mask)>(0.25*pixels):
        print('Yellow detected')
        
        pwm.start(5)
        engine.say('Yellow detected')
        engine.runAndWait()
      # BLUE
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(blue_mask) and cv2.countNonZero(green_mask)<cv2.countNonZero(blue_mask) and cv2.countNonZero(orange_mask)<cv2.countNonZero(blue_mask) and cv2.countNonZero(yellow_mask)<cv2.countNonZero(blue_mask) and cv2.countNonZero(magenta_mask)<cv2.countNonZero(blue_mask)) and cv2.countNonZero(blue_mask)>(0.25*pixels):
        print('Blue detected')
        
        pwm.start(5)
        engine.say('Blue detected')
        engine.runAndWait()
      # magenta
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(magenta_mask) and cv2.countNonZero(green_mask)<cv2.countNonZero(magenta_mask) and cv2.countNonZero(orange_mask)<cv2.countNonZero(magenta_mask) and cv2.countNonZero(yellow_mask)<cv2.countNonZero(magenta_mask) and cv2.countNonZero(blue_mask)<cv2.countNonZero(magenta_mask)) and cv2.countNonZero(magenta_mask)>(0.25*pixels):
        print('Magenta detected')
        
        pwm.start(5)
        engine.say('Magenta detected')
        engine.runAndWait()
      # cyan
      elif (cv2.countNonZero(red_mask)<cv2.countNonZero(cyan_mask) and cv2.countNonZero(green_mask)<cv2.countNonZero(cyan_mask) and cv2.countNonZero(orange_mask)<cv2.countNonZero(cyan_mask) and cv2.countNonZero(yellow_mask)<cv2.countNonZero(cyan_mask) and cv2.countNonZero(blue_mask)<cv2.countNonZero(cyan_mask)) and cv2.countNonZero(cyan_mask)>(0.25*pixels):
        print('Cyan detected')
        
        pwm.start(5)
        engine.say('Cyan detected')
        engine.runAndWait()
      # NO COLOR DETECTED (ELSE CASE)
      else:
        print('Color not detected')
        #INSERT CODE: Stop servo rotation
        pwm.stop()
        engine.say('Color not detected')
        engine.runAndWait()
      print('------------------------')
      break
      start_time = time.time()
  GPIO.cleanup()