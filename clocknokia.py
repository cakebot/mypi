#!/usr/bin/env python

# clockmain.py

# AUTHOR: Jim Baur
# DATE CREATED: 10/26/14
# DESCRIPTION: My first attempt at creating my Raspberry Pi clock

import time
from time import strftime
import os
import RPi.GPIO as GPIO

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont

# Raspbery Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def setup_screen():
	# Hardware SPI usage:
	disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

	# Initialize library.
	disp.begin(contrast=60)

	# Clear display.
	disp.clear()
	disp.display()
	return disp	

def main():
	# initalize screen
	disp = setup_screen()
	# set up display
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	#draw a white canvas
	draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
	# show some boot up text
	defaultfont = ImageFont.load_default()
	#font = ImageFont.truetype('/home/pi/mypi/fonts/v5prophit_cell/V5PRC___.TTF', 16)
	draw.text((8,15), "Loading", font=defaultfont)
	disp.image(image)
	disp.display()
	location = 50
	for i in range(0,3):	
		draw.text((location, 15), ".", font=defaultfont)
		disp.image(image)
		disp.display()
		location += 5
		time.sleep(0.3)
	time.sleep(1)
	
	#set timezone to EST
	os.environ['TZ'] = 'US/Eastern'
	time.tzset()
	#clock loop
	while True:
		curtime = strftime("%I:%M:%S %p")
		weekday = strftime("%A")
		curdate = strftime("%b %d, %Y")
		disp.clear()
		draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
		draw.text((1, 0), curtime, font=defaultfont)
		draw.text((1, 8), weekday, font=defaultfont)
		draw.text((1, 16), curdate, font=defaultfont)
		disp.image(image)
		disp.display()
		# exits script if button is pressed
		if (GPIO.input(17) == False):
			kill_clock(disp, image, draw)


def kill_clock(disp, image, draw):
	# function to properly shut down the clock
	disp.clear()
	draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
	disp.display()
	exit(0)		
main()


