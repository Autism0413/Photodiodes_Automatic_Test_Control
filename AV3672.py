# -*- codeing =utf-8 -*-
import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, strict_range
from pyvisa.errors import VisaIOError
from pymeasure.adapters import VISAAdapter

class CeyearAV3672(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "AV3672",
            **kwargs
        )

    Trigger_mode = Instrument.control(
        ":SENSe:SWEep:MODE?", ":SENSe:SWEep:MODE  %s",
        """ 
        查询或设置指定通道的频率 Hold、s、c
        """
    )

    IF_Bandwidth= Instrument.control(
        ":SENS:BWID?", ":SENS:BWID  %s",
        """ 
        设置测量时的中频滤波器带宽。
        """
    )

    Test_select=Instrument.control(
        ":CALCulate1:PARameter:MNUMber:SEL?", ":CALCulate1:PARameter:MNUMber:SEL %d",
        """ 
        设置或查询指定通道上选择的测量
        """
    )

    Marker_func=Instrument.control(
        ":CALCulate1:MARKer:FUNCtion:SEL?",":CALCulate1:MARKer:FUNCtion:SEL %s",
        """ 
        立即执行指定的搜索功能。
        MAXimum - 最大值
        MINimum - 最小值
        RPEak - 右峰值
        LPEak - 左峰值
        NPEak - 下一个峰值
        TARGet - 目标
        LTARget - 左目标
        RTARget - 右目标
        """
    )

    Open_Marker=Instrument.control(
        ":CALCulate1:MARKer1:STATe?", ":CALCulate1:MARKer1:STATe %s",
        """ 
        打开或关闭指定的光标。
        """
    )



    Func_trac=Instrument.control(
        ":CALCulate1:MARKer:FUNCtion:TRACking?", ":CALCulate1:MARKer:FUNCtion:TRACking %s",
        """ 
        设置指定光标的跟踪功能，跟踪功能使光标在每次扫描时都执行搜索功能
        """
    )

    MarkerX_read=Instrument.control(
        ":CALCulate1:MARKer1:X?", ":CALCulate1:MARKer1:X %d",
        """ 
        返回通道 1 所选测量上光标 3 的 X 轴坐标值
        """
    )

    Span_Frequency=Instrument.control(
        "SENS:FREQ:SPAN?", ":SENS:FREQ:SPAN %d",
        """ 
         设置分析仪的频率跨度hz。
        """
    )

    Center_Frequency=Instrument.control(
        ":SENS:FREQ:CENT?", ":SENS:FREQ:CENT %d",
        """ 
         设置分析仪的中心频率hz
        """
    )