#! /usr/bin/env python

# quick script to create a boot disk image for the Z80-SBC2

# import os
import sys
from sys import argv

# 8Mb image size

disk_size = 8 * 1024 * 1024

def main():
  if len(argv) < 2:
    print("Usage: makebootdsk.py <image>")
    sys.exit(1)

  with open('cpm22.bin', "rb") as binaryfile:
    cpm22_bin = bytearray(binaryfile.read())
  binaryfile.close()

  disk_image = bytearray (b'\xe5') * disk_size
  print(len(disk_image))
  disk_image[0x0000:len(cpm22_bin) - 0x20] = cpm22_bin[0x0020:len(cpm22_bin)]
  print(len(disk_image))

  dskfile = argv[1]
  with open(dskfile, "wb") as out_dskfile:
    out_dskfile.write(disk_image)
  out_dskfile.close()
  print("makebootdsk.py: wrote", dskfile)

if __name__=="__main__":
  main()
