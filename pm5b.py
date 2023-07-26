import time
import struct
import numpy as np
from usb import core
from pyftdi.ftdi import Ftdi

def toBits8(byte):
    # must be an unsiged byte < 255
    return format(byte, "#010b")[2:]

class PM5B:
    def __init__(self, queryDelay=3) -> None:
        # queryDelay: seconds between query command and data reading.
        self.queryDelay = queryDelay
        self.queryByte = "?"
        self.controlByte = "!"
        self.endByte = "\r"
        self.rangeMap = {"000": False, '001': 0.2, "010": 2, "011": 20, "100": 200}
        self.agg = {
            "avg": np.mean,
            "max": np.max,
            "min": np.min
        }
        
    def init_comm(self):
        self.dev = core.find()
        self.ftdi = Ftdi()
        self.ftdi.open_from_device(self.dev)

    def sendCMD(self, command='?D11111\r'):
        return self.ftdi.write_data(command)

    def getPower(self, agg=None):
        # agg method
        rawData = self.ftdi.read_data(1000)
        packs = rawData.split(b'D') 
        validMsgs = [msg for msg in packs if len(msg) == 5]
        if not validMsgs:
            print(f"warning, no valid message. pack: {packs}")
            return None
        powers = [self.parseMsg(msg) for msg in validMsgs]
        if agg:
            return self.agg[agg](powers)
        else:
            return powers

    def parseMsg(self, msg):
        rangeBits = msg[-1]
        curRange = self.rangeMap[toBits8(rangeBits)[:3]]
        # unpack the 2 data bytes to integer in 16 bits compliment manner
        countValue = struct.unpack('<h', msg[:2])[0] 
        # refer to manual page 15
        reading = countValue* 2 * curRange* 1e-3 / 59576
        return reading
    
    def query(self, queryType='oneshot', agg='avg'):
        """
        args:
            queryType: oneshot, stream
            agg: avg, min, max
        """
        self.init_comm()
        if queryType=='oneshot':
            self.sendCMD('?D11111\r')
        elif queryType=="stream":
            self.sendCMD('?D11111\r')
        else:
            raise ValueError(f"Invalid query type: {queryType}")
        time.sleep(self.queryDelay)
        power = self.getPower(agg=agg)
        self.reset()
        return power

    def reset(self):
        self.dev.reset()