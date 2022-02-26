#! /usr/bin/env python

# quick script to create a disk image for the Z80-SBC2

# import os
import sys
from sys import argv

# 8Mb image size

disk_size = 8 * 1024 * 1024
dir_end = 0x4000
first_entry = b' UNLABELED  ' + b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def main():
  if len(argv) < 2:
    print("Usage: makedsk.py <image>")
    sys.exit(1)

  dskfile = argv[1]
  with open(dskfile, "wb") as out_dskfile:
    out_dskfile.write(first_entry)
    for i in range(len(first_entry), dir_end):
      out_dskfile.write(b'\xe5')
    for i in range(dir_end, disk_size):
      out_dskfile.write(b'\x00')
  out_dskfile.close()
  print("makedsk.py: wrote", dskfile)

if __name__=="__main__":
  main()
