# MoAttenuator

The MoAttenuator is recognized over USB as a serial port automatically in Windows, Mac and Linux. It accepts a JSON string command to set its attenuation.

Json strings are sent over the serial port and are terminated by a \n or \r. The format is as follows:

    { "msg": "setAtten", "val": dB }\n

Where dB is a floating point value between 0.0 and 31.25.

It will respond with with this json message back:

    { "msg": "setAtten", "type": "resp", val": dB }\n

The MoAttenuator.py file provides a helper class to accomplish this communication. You tell it what serial port to use and then you can call it to send this message over the serial port:

    from MoAttenuator import MoAttenuator
    moAttenuator = MoAttenuator("/dev/tty.usbmodem123456")
    moAttenuator.setAttenuation( 15.0 )
    ...
    moAttenuator.close()

You can also use this from the command line:

    python MoAttenuator.py /dev/tty.usbmodem123456 15.0

