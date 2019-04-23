'''
**********************************************************************
* Filename: atmosphere-sensing.py
* Description : A script run by UW Fox Valley drone fitted with a
*   Raspberry Pi 3B+. This script collects measurable
*   atmospheric data when the drone is in flight.
* Author  : Eric McDaniel - University of Wisconsin - Fox Valley
* E-mail  : mcdae6861@students.uwc.edu
* Website : https://github.com/McDanielES/atmosphere-sensing
* Version : 1.3
* Update  : 2/25/19
**********************************************************************
'''

import RPi.GPIO as GPIO
import time
from time import localtime, strftime
import os.path
import sys,os
import curses

DHT   = 17  # BCM: 17 (Board: 11)
LED_1 = 27  # BCM: 27 (Board: 13)
LED_2 = 22  # BCM: 22 (Board: 15)
PUD   = 23  # BCM: 23 (Board: 16)

MAX_UNCHANGE_COUNT = 100
STATE_INIT_PULL_DOWN   = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN   = 5

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_1, GPIO.OUT)
	GPIO.output(LED_1, GPIO.LOW)
	GPIO.setup(LED_2, GPIO.OUT)
	GPIO.output(LED_2, GPIO.LOW)
	GPIO.setup(PUD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_dht11_dat(currentTime):
	GPIO.setup(DHT, GPIO.OUT)
	GPIO.output(DHT, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHT, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHT, GPIO.IN, GPIO.PUD_UP)
	
	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHT)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		# print("\tCorrupt Data\t\t   Time: %s Seconds" % (currentTime))
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up  = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		# print ("\tCorrupt Data\t\tTime: %s Seconds" % (currentTime))
		return False

	return the_bytes[0], the_bytes[2]

def draw_menu(stdscr):
	min_temp = 20
	max_temp = 40

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()
	height, width = stdscr.getmaxyx()

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	# Concatenate the parent/child directories with file name
	currentDir = os.path.dirname(os.path.realpath(__file__))
	originPath = os.path.join(currentDir, "flight-test-data")
	filename = "HumidityTemp_" + strftime("%m-%d-%Y_%H:%M:%S_%p", localtime()) + ".txt"
	filepath = os.path.join(originPath, filename)

	# Create child directory if none exists
	if not os.path.exists(originPath):
		os.mkdir(os.path.join(originPath))

	# Open this file as append mode
	textfile = open(filepath, "a")

	# Script is loaded, file is opened. Illuminate LED to notify user that
	# drone is ready, don't start until the switch is activated
	GPIO.output(LED_1, GPIO.HIGH)
	if GPIO.input(23) == GPIO.HIGH:
		ready = True
	else:
		warning_message = "Please flip switch to begin data collection."
		stdscr.attron(curses.color_pair(2))
		stdscr.attron(curses.A_BOLD)
		stdscr.addstr(int(height // 2), int((width // 2) - (len(warning_message) // 2) - len(warning_message) % 2), warning_message)
		stdscr.attroff(curses.color_pair(2))
		stdscr.attroff(curses.A_BOLD)
		stdscr.refresh()
		ready = False

	while not ready:
		if GPIO.input(23) == GPIO.HIGH:
			ready = True
		time.sleep(0.25)

	currentTime = 0
	stdscr.clear()
	stdscr.refresh()

	while (currentTime < 600) and (GPIO.input(23) == GPIO.HIGH):
		stdscr.clear()
		currentTime += 1
		result = read_dht11_dat(currentTime)

		while (result == False):
			result = read_dht11_dat(currentTime)
			time.sleep(0.01)

		if result:
			humidity, temperature, = result
			# print("Humidity: %s%%,  Temperature: %s. C, Time: %s Seconds" % (humidity, temperature, currentTime))
			textfile.write("%s, %s, %s\n" % (humidity, temperature, currentTime))
		else:
			textfile.write("-1, -1, %s\n" % (currentTime))

		# Declaration of strings
		title = "Atmospheric Sensing"[:width-1]
		subtitle = "Collecting Atmospheric Pollution and Emission Data Utilizing a Raspberry Pi computer on a Hexacopter Drone"[:width-1]
		developers = "Written by: Eric McDaniel -  University of Wisconsin - Fox Valley"[:width-1]
		statusbarstr = "Press 'Ctrl - C' to exit"

		# Centering calculations
		start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
		start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
		start_x_developers = int((width // 2) - (len(developers) // 2) - len(developers) % 2)
		start_y_graphs = int((height) - 5)
		end_y_graphs = int(10)
		barlength = start_y_graphs - end_y_graphs
		temp_bar_height = ((temperature - min_temp) * barlength) / (max_temp - min_temp)
		humid_bar_height = (humidity * barlength) / 100

		# Render status bar
		stdscr.attron(curses.color_pair(3))
		stdscr.addstr(height-1, 0, statusbarstr)
		stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
		stdscr.attroff(curses.color_pair(3))

		# Turning on attributes for title
		stdscr.attron(curses.color_pair(2))
		stdscr.attron(curses.A_BOLD)

		# Rendering title
		stdscr.addstr(1, start_x_title, title)
		stdscr.addstr(start_y_graphs - 4 - temp_bar_height, int(width // 3) , "{} Degrees".format(temperature))
		stdscr.addstr(start_y_graphs - 4 - humid_bar_height, int(width // 3) * 2 , "{} Percent".format(humidity))

		# Turning off attributes for title
		stdscr.attroff(curses.color_pair(2))
		stdscr.attroff(curses.A_BOLD)

		# Print rest of title
		stdscr.addstr(2, start_x_subtitle, subtitle)
		stdscr.addstr(3, start_x_developers, developers)

		stdscr.addstr(start_y_graphs, int(width // 3), "Temperature")
		stdscr.addstr(start_y_graphs - 2, int(width // 3) - 12, "{} degrees".format(min_temp))
		stdscr.addstr(end_y_graphs, int(width // 3) - 12, "{} degrees".format(max_temp))
		stdscr.addstr(start_y_graphs, int(width // 3) * 2 + 1, "Humidity")
		stdscr.addstr(start_y_graphs - 2, int(width // 3) * 2 - 4, "0%")
		stdscr.addstr(end_y_graphs, int(width // 3) * 2 - 5, "100%")
		timer = "Progression: {} seconds".format(currentTime)
		stdscr.addstr(6, int((width // 2) - (len(timer) // 2) - len(timer) % 2), timer)

		for x in range(0, barlength - 3):
			stdscr.addstr(start_y_graphs - 3 - x, int(width // 3) - 7, "|")
		for x in range(0, barlength - 3):
			stdscr.addstr(start_y_graphs - 3 - x, int(width // 3) * 2 - 4, "|")

		# Design bar graph
		stdscr.attron(curses.color_pair(3))
		for x in range(0, temp_bar_height):
			stdscr.addstr(start_y_graphs - 3 - x, int(width // 3), "           ")
		for x in range(0, humid_bar_height):
			stdscr.addstr(start_y_graphs - 3 - x, int(width // 3) * 2, "           ")

		stdscr.attroff(curses.color_pair(3))		

		stdscr.move(0, 0)
	
		# Oscillate the LED on/off to indicate each file write
		GPIO.output(LED_2, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(LED_2, GPIO.LOW)
		time.sleep(0.45)
		# stdscr.clear()
		stdscr.refresh()
	textfile.close()

def main():
	setup()
	curses.wrapper(draw_menu)

	print("Done. Normal Termination.\n")

	# Cleanup GPIO, turn off LEDs.
	destroy()

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("Done. Normal Termination.\n")
		destroy()