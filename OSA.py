import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument


class OSA(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "AV3672",
            **kwargs
        )

    Chan1_sel=Instrument.measurement(
        ":LINS0:CALC:DATA:CHAN:SEL 001",
        """ 
        选择第1个通道
        """
    )

    Chan2_sel = Instrument.measurement(
        ":LINS0:CALC:DATA:CHAN:SEL 002",
        """ 
        选择第2个通道
        """
    )

    wav=Instrument.measurement(
        ":LINS0:CALC:WDM:DATA:CHAN:CPEA:WAV?",
        """ 
        返回通道 1 所选测量上光标 3 的 X 轴坐标值
        """
    )
    wav2 = Instrument.measurement(
        ":LINS0:CALC:WDM:DATA:CHAN2:CPEA:WAV?",
        """ 
        返回通道 2 所选测量上光标 3 的 X 轴坐标值
        """
    )