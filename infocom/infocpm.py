#! /usr/bin/python

# infocpm.py
# 
# Patch stock Infocom CP/M interpreter screen control codes
# By default, this uses ANSI/VT-100 codes.  Other terminal codes are commented
# below the default settings.

import os
import sys
from sys import argv

# These screen control codes are taken from the official Infocom patch utility,
# except for ANSI, which was found at
# https://www.vcfed.org/forum/forum/genres/cp-m-and-mp-m/58164-lost-treasures-of-infocom-on-cp-m

screen_codes = {
  # ANSI/VT-100
  'ansi': {
    'cpmcpl': 80,
    'cpmlpp': 24,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': chr(0x1b) + '[2J' + chr(0x1b) + '[25;1H',
    'treset': '',
    'bline': chr(0x1b) + '[H' + chr(0x1b) + '[7m',
    'eline': chr(0x1b) + '[0m' + chr(0x1b) + '[25;1H',
    'pinit': ''
  },
  # LEAR SIEGLER ADM3
  'lear': {
    'cpmcpl': 79,
    'cpmlpp': 23,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0x80,
    'tinit': chr(0x1e) + chr(0x1a) + chr(0x1b) + '=' + chr(55) + chr(32),
    'treset': '',
    'bline': chr(0x1b) + '=' + chr(32) + chr(32),
    'eline': chr(0x1b) + '=' + chr(55) + chr(32),
    'pinit': ''
  },
  # Default (dumb terminal)
  'dumb': {
    'cpmcpl': 63,
    'cpmlpp': 0,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': '',
    'treset': '',
    'bline': '',
    'eline': '',
    'pinit': ''
  },
  # ZENITH
  'zenith': {
    'cpmcpl': 79,
    'cpmlpp': 23,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': chr(27) + 'E' + chr(27) + 'Y' + chr(55) + chr(32),
    'treset': '',
    'bline': chr(27) + 'j' + chr(27) + 'Y' + chr(32) + chr(32) + chr(27) + 'p',
    'eline': chr(27) + 'k' + chr(27) + 'q',
    'pinit': ''
  },
  # XEROX 820
  'xerox': {
    'cpmcpl': 79,
    'cpmlpp': 23,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': chr(0x1e) + chr(0x1a) + chr(0x1b) + '=' + chr(23) + chr(0),
    'treset': '',
    'bline': chr(0x1b) + '=' + chr(0) + chr(0),
    'eline': chr(0x1b) + '=' + chr(23) + chr(0),
    'pinit': ''
  },
  # VECTOR
  'vector': {
    'cpmcpl': 79,
    'cpmlpp': 23,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': chr(0x1b) + chr(23) + chr(0),
    'treset': '',
    'bline': chr(0x1b) + chr(0) + chr(0) + chr(0x14),
    'eline': chr(0x1b) + chr(23) + chr(0) + chr(0x14),
    'pinit': ''
  },
  # INTERTEC COMPUSTAR & SUPERBRAIN
  'super': {
    'cpmcpl': 79,
    'cpmlpp': 23,
    'cpmclf': 1,
    'cpmllf': 1,
    'cpminv': 0,
    'tinit': chr(27) + '~k' + chr(27) + 'Y' + chr(55) + chr(32),
    'treset': '',
    'bline': chr(1),
    'eline': chr(27) + 'Y' + chr(55) + chr(32),
    'pinit': ''
  }
}

# offsets in the interpreter

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

def set_control_code(terp_buffer, start, string):
  terp_buffer[start] = len(string)
  offset = 1
  for value in string:
    terp_buffer[start + offset] = ord(value)
    offset += 1

def set_datfile(terp_buffer, datfile):
  # Blank out story.dat filename
  for offset in range(8):
    terp_buffer[CPMFN + offset] = ord(' ')
  # Copy story.dat filename
  terp_buffer[CPMFN:CPMFN+8]
  offset = 0
  for character in datfile[0:8]:
    terp_buffer[CPMFN + offset] = ord(character.upper())
    offset += 1

def main():
  if len(argv) < 2:
    print("Usage: infocpm.py <datfile> <terminal type>")
    sys.exit(1)

  datfile = argv[1]
  if len(argv) < 3:
    print("infocpm.py: terminal type: ANSI (default)")
    terminal_type = 'ansi'
  else:
    terminal_type = argv[2]
    print("infocpm.py: terminal type:", terminal_type.upper() )

  if not terminal_type in screen_codes:
    print("infocpm.py: invalid terminal type")
    print("  valid terminal types:")
    for key, value in sorted(screen_codes.items()):
      print("    ", key)
    sys.exit(-1)

  basename = os.path.basename(datfile)
  outfile = os.path.splitext(basename)[0][0:8].lower() + '.com'
  cpmdatfile = os.path.splitext(basename)[0][0:8].lower() + '.dat'

  print("            command file: ", outfile )
  print("            story file:   ", cpmdatfile )
  print("            source file:  ", datfile)

  with open('interpreter', 'rb') as binaryfile:
    terp_buffer = bytearray(binaryfile.read())
  binaryfile.close()

  set_datfile(terp_buffer, datfile)

  terp_buffer[CPMCPL] = screen_codes[terminal_type]['cpmcpl']
  terp_buffer[CPMLPP] = screen_codes[terminal_type]['cpmlpp']
  terp_buffer[CPMCLF] = screen_codes[terminal_type]['cpmclf']
  terp_buffer[CPMLLF] = screen_codes[terminal_type]['cpmllf']
  terp_buffer[CPMINV] = screen_codes[terminal_type]['cpminv']

  set_control_code(terp_buffer, TINIT, screen_codes[terminal_type]['tinit'])
  set_control_code(terp_buffer, TRESET, screen_codes[terminal_type]['treset'])
  set_control_code(terp_buffer, BLINE, screen_codes[terminal_type]['bline'])
  set_control_code(terp_buffer, ELINE, screen_codes[terminal_type]['eline'])
  set_control_code(terp_buffer, PINIT, screen_codes[terminal_type]['pinit'])

  with open(outfile, "wb") as out_terp:
    out_terp.write(terp_buffer)
  out_terp.close()
  print("infocpm.py: wrote", outfile)

  # Create story datfile, padding to page boundaries
  page = 256
  datfile_size = os.path.getsize(datfile)
  print("infocpm.py: story datfile", hex(datfile_size), "bytes")
  datfile_padded_size = (int ((datfile_size / page) + (datfile_size % page > 0))) * page

  with open(datfile, 'rb') as binaryfile:
    datfile_buffer = bytearray(binaryfile.read())
  binaryfile.close()
  
  datfile_buffer = datfile_buffer.ljust(datfile_padded_size, b'\x00')
  print("infocpm.py: padded datfile to", hex(len(datfile_buffer)), "bytes")

  with open(cpmdatfile, "wb") as out_datfile:
    out_datfile.write(datfile_buffer)
  out_datfile.close()
  print("infocpm.py: wrote", cpmdatfile)

if __name__=="__main__":
  main()
