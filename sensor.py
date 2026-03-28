from homeassistant.components.sensor import SensorEntity
class FFTSensor(SensorEntity):
    def __init__(self, source_entity, window_size, sampling_rate):
        self._source = source_entity
        self._buffer = deque(maxlen=window_size)
        self._sampling_rate = sampling_rate

        self._state = None
        self._amplitude = None
        self._freqs = None
        self._fft_vals = None

        self._attr_name = f"FFT {source_entity}"

    async def async_added_to_hass(self):
        async_track_state_change_event(
            self.hass, [self._source], self._state_changed
        )

    async def _state_changed(self, event):
        new_state = event.data.get("new_state")

        if new_state is None:
            return

        try:
            value = float(new_state.state)
        except ValueError:
            return

        self._buffer.append(value)

        if len(self._buffer) < self._buffer.maxlen:
            return

        try:
            freq, amp = dominant_frequency(
                list(self._buffer), self._sampling_rate
            )

            self._freqs, self._fft_vals = compute_fft(
                list(self._buffer), self._sampling_rate
            )

            self._state = round(freq, 4)
            self._amplitude = round(amp, 4)

            self.async_write_ha_state()

        except Exception as e:
            _LOGGER.error(f"FFT calculation error: {e}")

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "amplitude": self._amplitude,
            "samples": len(self._buffer),
            "sampling_rate": self._sampling_rate
        }
