import pymeasure
from pymeasure.instruments import Instrument, RangeException
import K8163B

k8 = K8163B.Keysight8163B("GPIB0::20::INSTR")  # 连接仪
k8.set_laserwav=1550
for i in range(0, 20):
    k8.set_laserwav = 1550+i