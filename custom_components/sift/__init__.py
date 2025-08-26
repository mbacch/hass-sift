"""Sift custom component for Home Assistant.

This custom component ingests Home Assistant data into Sift (https://www.siftstack.com)
"""
import logging
import aiohttp

from homeassistant.const import EVENT_STATE_CHANGED, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, State, Event, callback
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

from .const import CONF_API_KEY, CONF_API_URI, CONF_ASSET, DOMAIN, CONF_FILTER
from .schemas import CONFIG_SCHEMA, PAYLOAD_SCHEMA

_LOGGER = logging.getLogger(__name__)

async def send_to_rest_api(hass: HomeAssistant, timestamp: str, channel: str, value):
    """Setup payload and send to Sift schemaless REST API."""
    api_uri = hass.data[DOMAIN][CONF_API_URI]
    api_key = hass.data[DOMAIN][CONF_API_KEY]
    asset   = hass.data[DOMAIN][CONF_ASSET]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "asset_name": asset,
        "data": [
            {"timestamp": timestamp, "values": [{"channel": channel, "value": value}]}
        ],
    }

    validated_payload = PAYLOAD_SCHEMA(payload)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                api_uri, json=validated_payload, headers=headers
            ) as resp:
                body = await resp.text()
                if resp.status != 200:
                    _LOGGER.error(
                        "API error %s when sending %s: %s", resp.status, channel, body
                    )
                else:
                    _LOGGER.debug("Sent successfully: %s", payload)
                    _LOGGER.debug("Echoed back: %s", body)
        except Exception as exc:
            _LOGGER.exception("Error sending data to REST API: %s", exc)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup Sift component."""
    conf = config[DOMAIN]
    entity_filter = conf.get("filter", {})

    api_uri = conf[CONF_API_URI]
    api_key = conf[CONF_API_KEY]
    asset = conf[CONF_ASSET]

    hass.data[DOMAIN] = {
        CONF_API_URI: api_uri,
        CONF_API_KEY: api_key,
        CONF_ASSET: asset,
        CONF_FILTER: entity_filter
    }

    @callback
    def handle_event(event: Event) -> None:
        """Handle state change events."""
        new_state: State | None = event.data["new_state"]

        if (
            new_state is None
            or new_state.state in (STATE_UNKNOWN, "", STATE_UNAVAILABLE, None)
            or not entity_filter(new_state.entity_id)
        ):
            return

        event_timestamp = dt_util.utcnow().isoformat(timespec="milliseconds").replace("+00:00", "Z")
        event_channel = new_state.entity_id 
        event_value = new_state.state

        hass.async_create_task(
            send_to_rest_api(
                hass=hass, timestamp=event_timestamp, channel=event_channel, value=event_value
            )
        )
    
    hass.bus.async_listen(EVENT_STATE_CHANGED, handle_event)

    return True
