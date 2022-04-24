# Import packages
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import pyttsx3
import time

# Initial variables
engine = pyttsx3.init()
start_time = time.time()

# GPIO Setup
GPIO.setwarnings(False)

# Set variable for servoPin
servoPin = 17

# Set GPIO mode to GPIO.BCM
GPIO.setmode(GPIO.BCM)

# Set servoPin as GPIO.OUT
GPIO.setup(servoPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 100)

def detect_color(color, match):
	global engine
	global pwm
	
	print(color, "detected")
	pwm.start(5)
	engine.say("huh" + color + "detected")
	time.sleep(3)
	print(color, "matches with", match)
	engine.say(color + " matches with " + match)
	engine.runAndWait()

# Pi Camera Setup
while (True):
	# Make a camera object
	camera = PiCamera()

	# Set camera resolution
	camera.resolution = (640, 480)

	# Set camera frame rate
	rawCapture = PiRGBArray(camera, size = (640, 480))
	pixels = 640 * 480
	camera.framerate = 30

	for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
		frame = frame.array

		# Color Detection
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Red Color Detection:
		# Define lower boundary
		red_lower = np.array([160, 70, 50])
		# Define upper boundary
		red_upper = np.array([180, 255, 255])
		# Create mask
		red_mask = cv2.inRange(hsv, red_lower, red_upper)
		# Use bitwise_and to isolate color from the video
		result_red = cv2.bitwise_and(frame, frame, mask = red_mask)

		# Orange Color Detection:
		# orange_lower = np.array([200, 190, 1])
		# orange_upper = np.array([255, 255, 18])
		orange_lower = np.array([10, 70, 50])
		orange_upper = np.array([23, 179, 179])
		orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)
		result_orange = cv2.bitwise_and(frame, frame, mask = orange_mask)

		# Yellow Color Detection:
		yellow_lower = np.array([24, 70, 50])
		yellow_upper = np.array([35, 255, 255])
		yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
		result_yellow = cv2.bitwise_and(frame, frame, mask = yellow_mask)

		# Green Color Detection:   
		green_lower = np.array([36, 40, 60])
		green_upper = np.array([75, 255, 255])
		green_mask = cv2.inRange(hsv, green_lower, green_upper)
		result_green = cv2.bitwise_and(frame, frame, mask = green_mask)

		# Cyan Color Detection:
		# cyan_lower = np.array([125, 0, 255])
		# cyan_upper = np.array([0, 125, 255])
		cyan_lower = np.array([85, 50, 50])
		cyan_upper = np.array([99, 255, 255])
		cyan_mask = cv2.inRange(hsv, cyan_lower, cyan_upper)
		result_cyan = cv2.bitwise_and(frame, frame, mask = cyan_mask)

		# Blue Color Detection:
		# blue_lower = np.array([125, 0, 255])
		# blue_upper = np.array([0, 125, 255])
		blue_lower = np.array([100, 50, 50])
		blue_upper = np.array([130, 255, 255])
		blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
		result_blue = cv2.bitwise_and(frame, frame, mask = blue_mask)

		# Magenta Color Detection:
		# magenta_lower = np.array([130, 50, 70])
		# magenta_upper = np.array([160, 255, 255])
		magenta_lower = np.array([140, 156, 156])
		magenta_upper = np.array([155, 255, 255])
		magenta_mask = cv2.inRange(hsv, magenta_lower, magenta_upper)
		result_magenta = cv2.bitwise_and(frame, frame, mask = magenta_mask)

		# Pink Color Detection:
		pink_lower = np.array([140, 10, 10])
		pink_upper = np.array([180, 105, 255])
		pink_mask = cv2.inRange(hsv, pink_lower, pink_upper)
		result_pink = cv2.bitwise_and(frame, frame, mask=pink_mask)
		
		# Brown Color Detection:
		brown_lower = np.array([10, 180, 180])
		brown_upper = np.array([42, 255, 255])
		brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)
		result_brown = cv2.bitwise_and(frame, frame, mask=brown_mask)
		
		# Gray Color Detection:
		gray_lower = np.array([120, 120, 120])
		gray_upper = np.array([255, 255, 255])
		gray_mask = cv2.inRange(hsv, gray_lower, gray_upper)
		result_gray = cv2.bitwise_and(frame, frame, mask=gray_mask)

		# Result:
		# Combine the results so all colors are isolated from the video using bitwise_or
		result_red_and_green = cv2.bitwise_or(result_red, result_green)
		result_blue_and_orange = cv2.bitwise_or(result_blue, result_orange)
		result_yellow_and_magenta = cv2.bitwise_or(result_yellow, result_magenta)
		result_cyan_and_pink = cv2.bitwise_or(result_cyan, result_pink)
		result_brown_and_gray = cv2.bitwise_or(result_brown, result_gray)
		result_some_colors = cv2.bitwise_or(result_red_and_green, result_blue_and_orange)
		result_more_colors = cv2.bitwise_or(result_some_colors, result_cyan_and_pink)
		result_even_more_colors = cv2.bitwise_or(result_more_colors, result_brown_and_gray)
		result_colors = cv2.bitwise_or(result_more_colors, result_yellow_and_magenta)

		# Display the final result
		cv2.imshow("Color Detection in Real-Time", result_colors)

		rawCapture.truncate(0) # Stop rawCapture to clear the stream in preparation for the next frame

		# Servo Control with Color Detection
		if (cv2.waitKey(5) & 0xFF == ord('q')):
		# if (time.time() - start_time >= 3) and (cv2.waitKey(3)):
			camera.close()

			red = cv2.countNonZero(red_mask)
			green = cv2.countNonZero(green_mask)
			orange = cv2.countNonZero(orange_mask)
			yellow = cv2.countNonZero(yellow_mask)
			blue = cv2.countNonZero(blue_mask)
			magenta = cv2.countNonZero(magenta_mask)
			cyan = cv2.countNonZero(cyan_mask)
			pink = cv2.countNonZero(pink_mask)
			brown = cv2.countNonZero(brown_mask)
			gray = cv2.countNonZero(gray_mask)

			percent = 0.08

			# RED
			if (red > percent * pixels) and (red > green and red > orange and red > yellow and red > blue and red > magenta and red > cyan and red > pink and red > brown and red > gray):
				detect_color("Red", "Orange")

			# GREEN
			elif (green > percent * pixels) and (green > red and green > orange and green > yellow and green > blue and green > magenta and green > cyan and green > pink and green > brown and green > gray):
				detect_color("Green", "Orange")

			# ORANGE
			elif (orange > percent * pixels) and (orange > red and orange > green and orange > yellow and orange > blue and orange > magenta and orange > cyan and orange > pink and orange > brown and orange > gray):
				detect_color("Orange", "Red")

			# YELLOW
			elif (yellow > percent * pixels) and (yellow > red and yellow > green and yellow > orange and yellow > blue and yellow > magenta and yellow > cyan and yellow > pink and yellow > brown and yellow > gray):
				detect_color("Yellow", "Orange")

			# BLUE
			elif (blue > percent * pixels) and (blue > red and blue > green and blue > orange and blue > yellow and blue > magenta and blue > cyan and blue > pink and blue > brown and blue > gray):
				detect_color("Blue", "Orange")

			# MAGENTA
			elif (magenta > percent * pixels) and (magenta > red and magenta > green and magenta > orange and magenta > yellow and magenta > blue and magenta > cyan and magenta > pink and magenta > brown and magenta > gray):
				detect_color("Magenta", "Orange")

			# CYAN
			elif (cyan > percent * pixels) and (cyan > red and cyan > green and cyan > orange and cyan > yellow and cyan > blue and cyan > magenta and cyan > pink and cyan > brown and cyan > gray):
				detect_color("Cyan", "Orange")

			# PINK
			elif (pink > percent * pixels) and (pink > red and pink > green and pink > orange and pink > yellow and pink > blue and pink > magenta and pink > cyan and pink > brown and pink > gray):
				detect_color("Pink", "Orange")

			# BROWN
			elif (brown > percent * pixels) and (brown > red and brown > green and brown > orange and brown > yellow and brown > blue and brown > magenta and brown > cyan and brown > pink and brown > gray):
				detect_color("Brown", "Orange")

			# GRAY
			elif (gray > percent * pixels) and (gray > red and gray > green and gray > orange and gray > yellow and gray > blue and gray > magenta and gray > cyan and gray > pink and gray > brown):
				detect_color("Gray", "Orange")

			# NO COLOR DETECTED
			else:
				print("Color not detected")
				# Stop servo rotation
				pwm.stop()
				engine.say("huh Color not detected")
				engine.runAndWait()

			print("------------------------")
			break
			start_time = time.time()

	GPIO.cleanup()
