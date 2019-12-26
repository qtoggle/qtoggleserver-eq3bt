
from qtoggleserver.lib import ble

from .base import EQ3BTPort


class Temperature(EQ3BTPort):
    TYPE = 'number'
    WRITABLE = True
    MIN = 5
    MAX = 30
    STEP = 0.5
    UNIT = u'\xb0C'  # degrees celsius

    ID = 'temperature'

    async def read_value(self):
        return self.get_peripheral().get_temp()

    @ble.port_exceptions
    async def write_value(self, value):
        await self.get_peripheral().set_temp(value)
