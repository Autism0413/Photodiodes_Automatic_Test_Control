# -*- codeing =utf-8 -*-
import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, strict_range
from pyvisa.errors import VisaIOError
from pymeasure.adapters import VISAAdapter

class Ceyear2438(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "C2438",
            **kwargs
        )

    clear=id = Instrument.measurement(
        "*IDN?", """ clear the instrument  """
    )

    measure_show=Instrument.measurement(
        ":MEAS2?", "设置指定窗口为绝对功率测量，并关闭相对测量，返回测量值。",
    )

    freq= Instrument.control(
        ":FREQ?", ":FREQ %s",
        """ 000000000000
        查询或设置指定通道的频率
        """
    )

# c2438=Ceyear2438("GPIB0::13::INSTR")
# c2438.clear
# print(c2438.measure_show)