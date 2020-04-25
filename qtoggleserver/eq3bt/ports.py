
import abc

from typing import cast, Optional

from qtoggleserver.core import ports
from qtoggleserver.lib import ble

from .eq3btthermostat import EQ3BTThermostat


class EQ3BTPort(ble.BLEPort, metaclass=abc.ABCMeta):
    WRITE_VALUE_QUEUE_SIZE = 1


class Boost(EQ3BTPort):
    TYPE = ports.TYPE_BOOLEAN
    WRITABLE = True

    ID = 'boost'

    async def read_value(self) -> Optional[bool]:
        return cast(EQ3BTThermostat, self.get_peripheral()).get_boost()

    @ble.port_exceptions
    async def write_value(self, value: bool) -> None:
        await cast(EQ3BTThermostat, self.get_peripheral()).set_boost(value)


class Temperature(EQ3BTPort):
    TYPE = 'number'
    WRITABLE = True
    MIN = 5
    MAX = 30
    STEP = 0.5
    UNIT = u'\xb0C'  # Degrees celsius

    ID = 'temperature'

    async def read_value(self) -> Optional[float]:
        return cast(EQ3BTThermostat, self.get_peripheral()).get_temp()

    @ble.port_exceptions
    async def write_value(self, value: float) -> None:
        await cast(EQ3BTThermostat, self.get_peripheral()).set_temp(value)
