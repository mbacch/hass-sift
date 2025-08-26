import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entityfilter import FILTER_SCHEMA
from .const import DOMAIN, CONF_API_URI, CONF_API_KEY, CONF_ASSET, CONF_FILTER


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_API_URI): cv.string,
                vol.Required(CONF_API_KEY): cv.string,
                vol.Required(CONF_ASSET): cv.string,
                vol.Optional(CONF_FILTER, default={}): FILTER_SCHEMA,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

STATE_VALUE_SCHEMA = vol.Any(
    vol.All(vol.Coerce(float), lambda v: round(v, 2)), 
            vol.Coerce(str), 
            vol.Coerce(bool)
)

PAYLOAD_SCHEMA = vol.Schema(
    {
        vol.Required("asset_name"): str,
        vol.Required("data"): [
            {
                vol.Required("timestamp"): str,
                vol.Required("values"): [
                    {
                        vol.Required("channel"): str,
                        vol.Required("value"): STATE_VALUE_SCHEMA,
                    }
                ],
            }
        ],
    }
)