from homeassistant.components.sensor import SensorEntity
from collections import deque
from .fft import dominant_frequency

WINDOW_SIZE = 128  # aantal samples
SAMPLING_RATE = 1  # Hz (aanpassen!)

class FFTSensor(SensorEntity):
    def __init__(self, source_entity):
        self._source = source_entity
        self._buffer = deque(maxlen=WINDOW_SIZE)
        self._state = None
        self._amplitude = None

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.hass.helpers.event.async_track_state_change(
                self._source, self._state_changed
            )
        )

    async def _state_changed(self, entity_id, old_state, new_state):
        try:
            value = float(new_state.state)
            self._buffer.append(value)

            if len(self._buffer) == WINDOW_SIZE:
                freq, amp = dominant_frequency(
                    list(self._buffer),
                    SAMPLING_RATE
                )
                self._state = round(freq, 3)
                self._amplitude = round(amp, 3)
                self.async_write_ha_state()

        except Exception:
            pass

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "amplitude": self._amplitude,
            "samples": len(self._buffer)
        }
