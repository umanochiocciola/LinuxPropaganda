# fancy new language!
# [language name] --> C code

from sys import argv
from os import system
import json


HEADER = '#include <stdio.h>\nint main(){'
AUTO_COMPILE = 0


def main():

	progr = parse_args()

	with open("repls.json", 'r') as f:
		repls = json.loads(f.read())

	while must_replace(repls, progr):
		for key in repls:
			progr = progr.replace(key, repls[key])


	output(progr)



def output(progr):

	with open("out.c", 'w') as f:
		f.write(HEADER + progr)

	if AUTO_COMPILE:
		system("gcc out.c -o out")



def must_replace(repls, progr):
	for key in repls:
		if key in progr:
			return 1

	return 0



def parse_args():
	global AUTO_COMPILE

	if '-c' in argv:
		argv.remove('-c')
		AUTO_COMPILE = 1

	if len(argv) < 2:
		print("unsufficient arguments")
		exit(1)

	try:
		with open(argv[1], 'r') as f:
			input_program = f.read()

	except FileNotFoundError:
		print("File not found:", argv[1])
		exit(1)

	return input_program


if __name__ == '__main__':
	main()