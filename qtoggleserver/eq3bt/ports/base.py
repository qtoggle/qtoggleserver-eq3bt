
import abc
import datetime

from typing import List, Optional

from qtoggleserver.lib import ble

from .exceptions import EQ3Exception


class EQ3BTPeripheral(ble.BLEPeripheral):
    WRITE_HANDLE = 0x0411
    NOTIFY_HANDLE = 0x0421

    STATUS_SEND_HEADER = 0x03
    STATUS_RECV_HEADER = 0x02
    STATUS_BOOST_MASK = 0x04

    STATUS_BITS_INDEX = 2
    STATUS_TEMP_INDEX = 5

    WRITE_TEMP_HEADER = 0x41
    WRITE_BOOST_HEADER = 0x45

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._temp = None
        self._boost = False

    async def set_temp(self, temp: float) -> None:
        self.debug('setting temperature to %.1f degrees', temp)

        await self.write(self.WRITE_HANDLE, bytes([self.WRITE_TEMP_HEADER, int(temp * 2)]))
        self.debug('successfully set temperature')
        self._temp = temp

    def get_temp(self) -> Optional[float]:
        self.check_poll_error()
        return self._temp

    async def set_boost(self, boost: bool) -> None:
        self.debug('%s boost', ['disabling', 'enabling'][boost])

        await self.write(self.WRITE_HANDLE, bytes([self.WRITE_BOOST_HEADER, int(boost)]))
        self.debug('successfully set boost')
        self._boost = boost

    def get_boost(self) -> Optional[bool]:
        self.check_poll_error()
        return self._boost

    async def poll(self) -> None:
        await self._read_config()

    async def _read_config(self) -> None:
        # Reset polled values so that, in case of error, old values aren't reused
        self._temp = None
        self._boost = None

        _, data = await self.write_notify(
            self.WRITE_HANDLE,
            self.NOTIFY_HANDLE,
            bytes([self.STATUS_SEND_HEADER] + self._make_status_value()),
            retry_count=0
        )

        if len(data) < 6:
            raise EQ3Exception(f'Notification data too short {self.pretty_data(data)}')

        if data[0] != self.STATUS_RECV_HEADER:
            raise EQ3Exception(f'Unexpected notification data header: {data[0]:02X}')

        self._boost = bool(data[self.STATUS_BITS_INDEX] & self.STATUS_BOOST_MASK)
        self._temp = data[self.STATUS_TEMP_INDEX] / 2.0

        self.debug('temperature is %.1f degrees', self._temp)
        self.debug('boost mode is %s', ['disabled', 'enabled'][self._boost])

    @staticmethod
    def _make_status_value() -> List[int]:
        now = datetime.datetime.now()

        return [
            now.year - 2000,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        ]


class EQ3BTPort(ble.BLEPort, metaclass=abc.ABCMeta):
    PERIPHERAL_CLASS = EQ3BTPeripheral
