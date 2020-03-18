import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import pytesseract
import pyttsx3

#some errors with installation 
try:
	from PIL import Image
except ImportError:
	import Image

button = 16 
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.1)
def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
def preprocess(image):
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	cv2.imwrite("output.jpg" ,gray_image)
#reading text
def convert():
	text = pytesseract.image_to_string(Image.open('output.jpg'))
	print(text)
	return text
#converting
def texttospeech(txt):
	engine = pyttsx3.init() 
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate-40)
	engine.say(txt)
	engine.runAndWait()
#combined calling and reading the document
def total_code():
	cap = cv2.VideoCapture(1)
	while True:
		ret, frame = cap.read()
		if (ret == False):
			print ("Error opening camera")
			continue
	image = cv2.imread(frame)
	preprocess(image)
	txt = convert()
	texttospeech(txt)

def loop():
        while True:
              button_state = GPIO.input(button)
              if  button_state == False:                  
                  print('Button Pressed...)
	total_code()
                  while GPIO.input(button) == False:
                    time.sleep(0.2)
              
def endprogram():
         GPIO.cleanup()

if __name__ == '__main__':          
          setup() 
          try:
                 loop()
          except KeyboardInterrupt:
                 print ('keyboard interrupt detected') 
                 endprogram()
