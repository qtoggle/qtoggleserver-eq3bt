
from qtoggleserver.core import ports
from qtoggleserver.lib import ble

from .base import EQ3BTPort


class Boost(EQ3BTPort):
    TYPE = ports.TYPE_BOOLEAN
    WRITABLE = True

    ID = 'boost'

    async def read_value(self):
        return self.get_peripheral().get_boost()

    @ble.port_exceptions
    async def write_value(self, value):
        await self.get_peripheral().set_boost(value)
