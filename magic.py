#!/usr/bin/env python3

import socket
import sys
import argparse


# protocol description
# https://steve.zazeski.com/using-node-red-to-send-commands-to-wifi-led-controllers/


# examples
# https://www.jpelectron.com/sample/Electronics/WiFi%20LED%20control/


# status info
# https://github.com/vikstrous/zengge-lightcontrol

SET_COLOR=0x31
SET_POWER=0x71
SET_MODE=0x61

ON=0x23
OFF=0x24

# MODES
SEVEN_COLOR_FADE=0x25		# menu 1
RED_GRADUAL=0x26			# menu 2
GREEN_GRADUAL=0x27			# menu 3
BLUE_GRADUAL=0x28			# menu 4
#	0x29
#	0x2A
#	0x2B
WHITE_GRADUAL=0x2C			# menu 8
RED_GREEN_FADE=0x2D			# menu 9
RED_BLUE_FADE=0x2E			# menu 10
GREEN_BLUE_FADE=0x2F		# menu 11
SEVEN_COLOR_STROBE=0x30		# menu 12
RED_STROBE=0x31				# menu 13
GREEN_STROBE=0x32			# menu 14
BLUE_STROBE=0x33			# menu 15
#	0x34
#	0x35
#	0x36
WHITE_STROBE=0x37			# menu 19
SEVEN_COLOR_JUMP=0x38		# menu 20


SPEED_100=0x01
SPEED_50=0x10




# this will calculate the last byte of the payload
def checksumCalc(bytes):

	sum = 0
	for i in bytes:
		sum = (sum + i) & 0xFF

	#sum = sum

	return sum

# R, G, B must be between 0 and 255
def setColor(r, g, b):

	my_bytes = bytearray()
	my_bytes.append(SET_COLOR)
	my_bytes.append(r)
	my_bytes.append(g)
	my_bytes.append(b)
	my_bytes.append(0x00)
	my_bytes.append(0x0F)
	my_bytes.append(checksumCalc(my_bytes))

	return my_bytes

# status must be ON or OFF
def setPower(status):

	my_bytes = bytearray()
	my_bytes.append(SET_POWER)
	my_bytes.append(status)
	my_bytes.append(0x0F)
	my_bytes.append(checksumCalc(my_bytes))

	return my_bytes

# return byte array to send a mode
def definded_led_mode(mode, speed):
    my_bytes = bytearray()
    my_bytes.append(SET_MODE)
    my_bytes.append(mode)
    my_bytes.append(speed)
    my_bytes.append(0x0f)
    my_bytes.append(checksumCalc(my_bytes))

    return my_bytes


# send the status request message
def getStatus():
    my_bytes = bytearray()
    my_bytes.append(0x81)
    my_bytes.append(0x8A)
    my_bytes.append(0x8B)
    my_bytes.append(checksumCalc(my_bytes))

    return my_bytes

def parse_status(data, json):

	# data[0] = 0x81 always
	deviceType = data[1]
	isOn = data[2] == ON
	mode = data[3]
	#  data[4] = 0x23 always
	speed = data[5]
	red = data[6]
	green = data[7]
	blue = data[8]
	ww = data[9]
	wc = data[10]
	# data[11] = 0x00 always
	# data[12] = checksum

	if json == True:
		print('{"device_type": "', hex(deviceType), '", "is_on": ', str(isOn).lower(), ', "device_mode": "', hex(mode), '", "speed": "', speed, '","color": [', red, ', ', green, ', ', blue, ']}', sep="")
	else:
		print('Device type: 0x%X' % deviceType)
		print('Is on: %d' % isOn)
		print('Device mode: 0x%X' % mode )
		print('Speed: 0x%X' % speed )
		print('Color (r,g,b): ({0}, {1}, {2})'.format(red , green , blue))



# send the message to get the status of the LED conroler
def send_get_status(host, port, json):

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	#print('connecting to %s port %s' % server_address)
	sock.connect(server_address)

	try:
	    my_bytes = getStatus()

	    #print(bytes(my_bytes).hex())

	    # Send data
	    sock.sendall(my_bytes)

	    data = sock.recv(16)
	    amount_received = len(data)
	    #print(bytes(data).hex())
	    #print('received "%d"' % amount_received)
	    parse_status(data, json)

	finally:
	    #print('closing socket')
	    sock.close()

# color is a tuple (r,g,b)
def send_set_color(host, port, color):

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	print('connecting to %s port %s' % server_address)
	sock.connect(server_address)

	try:
	    my_bytes = setColor(color[0], color[1], color[2])

	    print(bytes(my_bytes).hex())

	    # Send data
	    sock.sendall(my_bytes)

	finally:
	    print('closing socket')
	    sock.close()

# mode is the mode to set and speed is its speed of color transition
def send_set_mode(host, port, mode, speed):

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	print('connecting to %s port %s' % server_address)
	sock.connect(server_address)

	try:
	    my_bytes = definded_led_mode(mode, speed)

	    print(bytes(my_bytes).hex())

	    # Send data
	    sock.sendall(my_bytes)

	finally:
	    print('closing socket')
	    sock.close()

# power is either ON or OFF
def send_set_power(host, port, power):

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	print('connecting to %s port %s' % server_address)
	sock.connect(server_address)

	try:
	    my_bytes = setPower(power)

	    print(bytes(my_bytes).hex())

	    # Send data
	    sock.sendall(my_bytes)

	finally:
	    print('closing socket')
	    sock.close()


def int_color_range(val):

	if val.isnumeric() == False:
		msg = "%r is not a an integer" % val
		raise argparse.ArgumentTypeError(msg)

	value = int(val)

	if value > 256 or value < 0:
		msg = "%r is not in the range 0..256" % val
		raise argparse.ArgumentTypeError(msg)

	return value

def int_port_range(val):

	if val.isnumeric() == False:
		msg = "%r is not a an integer" % val
		raise argparse.ArgumentTypeError(msg)

	value = int(val)

	if value > 65535 or value < 0:
		msg = "%r is not in the range 0..65535" % val
		raise argparse.ArgumentTypeError(msg)

	return value


def hex_string(val):

	try:
		value = int(val, 16)
	except ValueError as e:
		msg = "%r is not a an hex string" % val
		raise argparse.ArgumentTypeError(msg)

	return value

def main():

	parser = argparse.ArgumentParser(description='CLI for the RGB LED controller')
	parser.add_argument('-H', '--host', metavar='host', required=True,
                    help='the hostname or IP address of the LED controller')
	parser.add_argument('-p', '--port', metavar='port', default=5577, type=int_port_range,
                    help='the port number for the LED controller (default: 5577)')

	subparsers = parser.add_subparsers(title='command', dest='command')
	parser_color = subparsers.add_parser('color', help='Set the LED\'s to one solid color')
	parser_color.add_argument('red', type=int_color_range, help='red value in the range of 0..256')
	parser_color.add_argument('green', type=int_color_range, help='green value in the range of 0..256')
	parser_color.add_argument('blue', type=int_color_range, help='blue value in the range of 0..256')

	parser_mode = subparsers.add_parser('mode', help='Set the LED\'s to one of the built in default modes')
	parser_mode.add_argument('mode', type=hex_string, help='the built in mode')
	parser_mode.add_argument('speed', type=hex_string, help='the speed of the animation')

	parser_status = subparsers.add_parser('status', help='Get the LED controller information')
	parser_status.add_argument('--json', action='store_const', const=True, help='output the status in JSON form')

	parser_on = subparsers.add_parser('on', help='Get the LED controller information')
	parser_off = subparsers.add_parser('off', help='Get the LED controller information')

	args = parser.parse_args()
	#print(args)

	if args.command == "on":
		send_set_power(args.host, args.port, ON)
	elif args.command == "off":
		send_set_power(args.host, args.port, OFF)
	elif args.command == "color":
		send_set_color(args.host, args.port, (args.red, args.green, args.blue))
	elif args.command == "mode":
		send_set_mode(args.host, args.port, args.mode, args.speed)
	elif args.command == "status":
		send_get_status(args.host, args.port, args.json)



if __name__ == '__main__':
	main()
