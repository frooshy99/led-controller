#!/usr/bin/env python3

import socket
import sys
import argparse

from lifxlan import Light, LifxLAN
import json

# python interface
# https://github.com/mclarkk/lifxlan


ON=65535
OFF=0




def get_status(light, isjson):

	label = light.get_label()
	power = "off" if light.get_power() == 0 else "on"
	version = light.get_version_tuple()
	color = light.get_color()
	wifi = light.get_wifi_info_tuple()


	status = {
		"device_vendor": version[0],
		"device_productr": version[1],
		"device_version": version[2],
		"device_label": label,
		"device_power": power,
		"brightness": color[2],
		"temp": color[3]
	}

	if isjson == True:
		print(json.dumps(status))
	else:
		print('Device vendor: ', version[0])
		print('Device product: ', version[1])
		print('Device version: ', version[2])
		print('Device power: ', power)
		print('Device label: "', label, '"')

		print('Device brightness: ', color[2])
		print('Device temp: ', color[3])



def int_bright_range(val):

	if val.isnumeric() == False:
		msg = "%r is not a an integer" % val
		raise argparse.ArgumentTypeError(msg)

	value = int(val)

	if value > 65535 or value < 0:
		msg = "%r is not in the range 0..65535" % val
		raise argparse.ArgumentTypeError(msg)

	return value

def int_temp_range(val):

	if val.isnumeric() == False:
		msg = "%r is not a an integer" % val
		raise argparse.ArgumentTypeError(msg)

	value = int(val)

	if value > 9000 or value < 2500:
		msg = "%r is not in the range 2500..9000" % val
		raise argparse.ArgumentTypeError(msg)

	return value


def main():

	parser = argparse.ArgumentParser(description='CLI for the Lifx Light bulb')
	parser.add_argument('-H', '--host', metavar='host', required=True,
                    help='the IP address of the Light')
	parser.add_argument('-M', '--mac', metavar='mac', required=True,
                    help='the mac address of the Light')

	subparsers = parser.add_subparsers(title='command', dest='command')
	parser_color = subparsers.add_parser('color', help='set the Lights brightness and temperature')
	parser_color.add_argument('brightness', type=int_bright_range, help='brightness of the light 0..65535')
	parser_color.add_argument('temp', type=int_temp_range, help='kelvin temperature of the light 2500..9000')


	parser_status = subparsers.add_parser('status', help='get the Light information')
	parser_status.add_argument('--json', action='store_const', const=True, help='output the status in JSON form')

	parser_on = subparsers.add_parser('on', help='turn the light on')
	parser_off = subparsers.add_parser('off', help='turn the light off')

	args = parser.parse_args()
	#print(args)

	light = Light(args.mac, args.host)

	if args.command == "on":
		light.set_power(ON)
	elif args.command == "off":
		light.set_power(OFF)
	elif args.command == "color":
		color = (0, 0, args.brightness, args.temp)
		light.set_color(color)
	elif args.command == "status":
		get_status(light, args.json)



if __name__ == '__main__':
	main()

