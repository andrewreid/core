"""Config flow for Coronavirus integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries

from . import get_coordinator
from .const import DOMAIN, OPTION_WORLDWIDE  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coronavirus."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    _options = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if self._options is None:
            self._options = {OPTION_WORLDWIDE: "Worldwide"}
            coordinator = await get_coordinator(self.hass)
            for case_id in sorted(coordinator.data):
                self._options[case_id] = coordinator.data[case_id].country

        if user_input is not None:
            return self.async_create_entry(
                title=self._options[user_input["country"]], data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("country"): vol.In(self._options)}),
            errors=errors,
        )
