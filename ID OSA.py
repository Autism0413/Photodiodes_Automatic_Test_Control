
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument

class ID_OSA(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "OSA",
            **kwargs
        )

    Freq= Instrument.measurement(
        ":CALCulate:DATA:CWAVelengths?",
        "Reads the current power meter value.",
        )

    set_unitx_fr=Instrument.measurement(
        ":UNIT:x 1",
        "Queries the Wavelength of peaks found in WDM peak analysis; response in Frequency or Wavelength(hz)",
        )




OSA=ID_OSA("ASRL10::INSTR")

OSA.set_unitx_fr
print(OSA.Freq)