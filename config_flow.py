import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

class FFTSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="FFT Sensor", data=user_input)

        schema = vol.Schema({
            vol.Required("source"): str,
            vol.Optional("sampling_rate", default=1.0): float,
            vol.Optional("window_size", default=128): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema)
