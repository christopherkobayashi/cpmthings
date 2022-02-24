#! /usr/bin/python

# infocpm.py
# 
# Patch stock Infocom CP/M interpreter to use ANSI/VT-100 screen control codes

import os
import sys
import subprocess
from sys import argv

if len(argv) < 2:
  print("Usage: infocpm.py <datfile>")
  sys.exit(1)

datfile = argv[1]

basename = os.path.basename(datfile)
outfile = os.path.splitext(basename)[0][0:8].lower() + '.com'
cpmdatfile = os.path.splitext(basename)[0][0:8].lower() + '.dat'

print("infocpm.py: creating", outfile, "and", cpmdatfile, "from", datfile)

with open('interpreter', 'rb') as binaryfile:
  terp_buffer = bytearray(binaryfile.read())
binaryfile.close()

size = len(terp_buffer)

# offsets in the interpreter
# https://www.vcfed.org/forum/forum/genres/cp-m-and-mp-m/58164-lost-treasures-of-infocom-on-cp-m

CPMCPL = 0x03
CPMLPP = 0x04
CPMFN = 0x05
CPMCLF = 0x0d
CPMLLF = 0x0e
CPMINV = 0x0f
TINIT = 0x10
TRESET = 0x31
BLINE = 0x52
ELINE = 0x73
PINIT = 0x94


columns = 80		# Characters/line (132 maximum)
rows = 24		# Lines/screen (NOT including status line)
screen_lf = 1		# 1 if LF should print after CR on screen
printer_lf = 1		# 1 if LF should print after CR on printer
inverse_add = 0		# Number to add to ASCII value of characters
			# to have them print in inverse video.
			# This is not applicable on many terminals.

# Initialize the terminal.  
# Should position the cursor at the lower left corner of the screen.
# On terminals with the facility, a scrolling region should be established
# to include all but the top line on the screen.  Also, clearing the screen
# is desirable.
tinit = chr(0x1b) + '[2J' + chr(0x1b) + '[25;1H'

# Reset the terminal at end of game.
# For example, if a scrolling region was established, reset it to include the
# entire screen.  Clearing the screen is NOT desirable.
treset = ''

# Begin status line.
# Should move the cursor to the upper left corner of the screen.  If at all
# possible, should go into inverse video.
bline = chr(0x1b) + '[H' + chr(0x1b) + '[7m'

# End status line.
# Should move the cursor to the lower left corner of the screen.  If status
# line uses inverse video, this state should be cleared.
eline = chr(0x1b) + '[0m' + chr(0x1b) + '[25;1H'

# Printer initialization.
# If any setup is required prior to using scripting.
pinit = ''

def multi(start, string):
  terp_buffer[start] = len(string)
  offset = 1
  for value in string:
    terp_buffer[start + offset] = ord(value)
    offset += 1

terp_buffer[CPMCPL] = columns
terp_buffer[CPMLPP] = rows
terp_buffer[CPMCLF] = screen_lf
terp_buffer[CPMLLF] = printer_lf
terp_buffer[CPMINV] = inverse_add

# Blank out story.dat filename
for offset in range(8):
  terp_buffer[CPMFN + offset] = ord(' ')

# Copy story.dat filename
terp_buffer[CPMFN:CPMFN+8]
offset = 0
for character in datfile[0:8]:
  terp_buffer[CPMFN + offset] = ord(character.upper())
  offset += 1

multi(TINIT, tinit)
multi(TRESET, treset)
multi(BLINE, bline)
multi(ELINE, eline)
multi(PINIT, pinit)

with open(outfile, "wb") as out_terp:
  out_terp.write(terp_buffer)
out_terp.close()

# Create story datfile, padding to page boundaries

subprocess.run(["dd", "if="+datfile, "of="+cpmdatfile, "bs=256", "conv=sync"])
