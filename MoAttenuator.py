
import time
import subprocess
import os
import sys
import argparse
import serial
import json


#
# MoAttenuator
#
# Uses pyserial to send a JSON string to the attenuator to set the attenuation.
# Json format:
#
# { "msg": "setAtten", "val": dB }
#
# Where dB is a floating point value between 0.0 and 31.25. This string
# is sent over the serial port to the attenuator and is terminated by
# a '\n' or '\r'
#
class MoAttenuator:
    def __init__(self, serialPort):
        self.parseState = "waiting"
        self.parseBuf = ""
        self.sp = serial.Serial( serialPort, baudrate=115200 )


    def close(self):
        self.sp.close()


    def digestChar(self, inChar):
        # wait for \n or \r and parse
        if ( (inChar == "\n") or (inChar == "\r")):
            result = self.parseJson()
            self.parseBuf = ""
            return result
        else:
            self.parseBuf += inChar
            return None


    def parseJson(self):
        # Don't parse if we don't have a good parse buffer
        if (len(self.parseBuf) < 5): return None
        
        try:
            j = json.loads( self.parseBuf )
            return j

        except Exception as e:
            print("Json parse error", e)
            return None


    def setAttenuation(self, atten):

        # send json command to set attenuation
        out = '{{"msg": "setAtten", "val": {0} }}\n'.format(atten)
        self.sp.write( out )
        time.sleep(0.25)

        out = None

        # Read Json response
        data = ''
        while self.sp.inWaiting() > 0:
          inChar = self.sp.read(1)
          data += inChar
          result = self.digestChar(inChar)
          if (result != None):
            out = result

        return out


    def getInfo(self):

        # send json command to get info
        out = '{{"msg": "info" }}\n'.format()
        self.sp.write( out )
        time.sleep(0.25)

        out = None

        # Read Json response
        data = ''
        while self.sp.inWaiting() > 0:
          inChar = self.sp.read(1)
          data += inChar
          result = self.digestChar(inChar)
          if (result != None):
            out = result

        return out



# Main script
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Serial port of moAttenuator.")
    parser.add_argument("db", help="db attenuation.")
    parser.add_argument("--info", help="Get info of attenuator.", action="store_true")
    args = parser.parse_args()

    # Create the moAttenuator Object
    moAttenuator = MoAttenuator(args.port)

    if (args.info):
        res = moAttenuator.getInfo()
        print res
    else:
        res = moAttenuator.setAttenuation( args.db )
        print(res)

    moAttenuator.close()


