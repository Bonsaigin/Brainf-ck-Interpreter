# Author: Ian Gibson
# Last Change: 3/8/2015
# A basic Brainf*ck interpreter
# No optimization, just implementing control characters
# Tested using Python 2.7.6

import sys

class InputError(Exception):
	def __init__(self, value):
		self.value = value

#read file into string
infile = open(sys.argv[1], 'r')
program = infile.read()
infile.close()

#initialize variables
stack = []
data = [0]
dptr = 0
cptr = 0
bracketDepth = 0
skip = False

#execute program
while cptr < len(program):
	ch = program[cptr]
	if skip == False:
		if ch == '+':
			data[dptr] += 1
	        elif ch == '-':
			data[dptr] -= 1
		elif ch == '>':
			dptr += 1
                	if len(data) <= dptr:	#extend data list if needed
				data.append(0)
		elif ch == '<':
			try:
				dptr -= 1
				if dptr < 0:
					raise ValueError('Attemped to access data array at negative index', cptr + 1, ch)
			except ValueError as e:
				print 'Error occurred: %s at character %d (%s)' % (e.args)
				quit()
		elif ch == '.':
			sys.stdout.write(chr(data[dptr]))
		elif ch == ',':
			data[dptr] = ord(sys.stdin.read(1))
		elif ch == '[':
			#if the current data value is not 0, remember the location
			#otherwise skip this block
			if data[dptr]:
				stack.append(cptr)
			else:
				skip = True			
		elif ch == ']':
			#if the current data value is not 0, go back to the matching opening bracket
			#otherwise remove the bracket pair from the stack and continue
			if data[dptr]:
				cptr = stack[len(stack)-1]
			else:
				stack.pop()

	#skipping loop, check bracket levels
	else:
		if ch == '[':
			bracketDepth += 1
		elif ch == ']' and bracketDepth:
			bracketDepth -= 1
		elif ch == ']':
			skip = False

	#print data
	cptr += 1
