#!/usr/bin/python
'''
**********************************************************************
* Filename    : graphic-dronepi.py
* Description : A curses application run by the UW Fox Valley drone fitted 
*               with a Raspberry Pi 3B+. This script collects
*               measurable atmospheric data when the drone is in flight.
*               This supplemental script just ensures that the board
*               positively has no active current flowing through the
*               GPIO should the main script not execute in its entirety.
* Author      : Eric McDaniel - University of Wisconsin - Fox Valley
* E-mail      : McDanielES@gmail.com
* Website     : https://github.com/McDanielES/graphic-dronepi
* Version     : 2.1
* Updated     : 11/22/19
**********************************************************************
'''
import RPi.GPIO as GPIO

def main():
	GPIO.cleanup()

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	try:
		main()
	except Exception:
		destroy()
