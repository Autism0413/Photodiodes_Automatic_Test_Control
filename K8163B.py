# -*- codeing =utf-8 -*-
import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, strict_range
from pyvisa.errors import VisaIOError
from pymeasure.adapters import VISAAdapter

class Keysight8163B(Instrument):
    """Represents N7761A"""

    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "C2438",
            **kwargs
        )

    set_laserwav = Instrument.control(
        ":sour2:wav?", ":sour2:wav %sNM",
        """
            query or set sour1 laser wavelength
        """
    )
    set_laserpow = Instrument.control(
        ":sour1:pow?", ":sour1:pow %sdBm",
        """
            query or set sour1 laser power
        """
    )
    active_laser = Instrument.control(
        ":outp:chan1?", ":outp:chan1 %s",
        """
            on:1
            off:0
        """
    )