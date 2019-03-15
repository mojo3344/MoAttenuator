
import time
import subprocess
import os
import sys
import argparse
import serial
import json
import pyping


parser = argparse.ArgumentParser()
parser.add_argument("port", help="Serial port of moAttenuator.")
args = parser.parse_args()

# Import and create the moAttenuator Object
from MoAttenuator import MoAttenuator
moAttenuator = MoAttenuator(args.port)

# Step through attenuation settings, increasing attenuation
# until we can't ping the DUT any longer.
att = 1.0
keepGoing = True

while (keepGoing):

  print("Attenuation 0")
  res = moAttenuator.setAttenuation( 0.0 )
  time.sleep(2)

  print("Attenuation {0}".format(att))
  res = moAttenuator.setAttenuation( att )

  # ping the DUT
  # res = pyping.ping('192.168.1.108') # 2.4 GHz
  res = pyping.ping('192.168.1.103')

  if res.ret_code == 0:
    print('Ping Success avg_rtt: {0}'.format(res.avg_rtt) ) 
  else:
    print('Ping Failed with {}'.format(res.ret_code))
    keepGoing = False

  att += 1.0


print("Attenuation 0")
res = moAttenuator.setAttenuation( 0.0 )

moAttenuator.close()

