# -*- codeing =utf-8 -*-

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, strict_range
from pyvisa.errors import VisaIOError
from pymeasure.adapters import VISAAdapter


class KeysightN7761A(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "N7761A",
            **kwargs
        )

    id = Instrument.measurement(
        "*IDN?", """ Reads the instrument identification """
    )

    #Pset
    output_power = Instrument.control(
        ":OUTP1:POW?", ":OUTP1:POW %g",
        """ A floating point property that controls the voltage
        in Volts. This property can be set.
        """
    )

    #αset
    at_factor=Instrument.control(
        ":INP1:ATT?", ":INP1:ATT %g",
        """ 
        Sets the attenuation factor (a) for the slot.
        """
    )
    wavelength=Instrument.control(
        ":INP1:WAV?", ":INP1:WAV %g",
        """ 
        Sets the attenuation factor (a) for the slot.
        """
    )
    current_power = Instrument.measurement(
        ":read1:pow?",
        "Reads the current power meter value.",
        )
    ZERO = Instrument.control(
        ":OUTP1:CORR:COLL:ZERO", ":INP1:WAV %g",
        """ 
        Sets the attenuation factor (a) for the slot.
        """
    )

    output_on=Instrument.control(
        ":outp1?", "outp1 %s",
        """ 
        Sets the attenuation factor (a) for the slot.
        """
    )
