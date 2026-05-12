"""HA Config Export - Button Entity."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import datetime
import logging

from .const import (
    DOMAIN,
    CONF_EXPORT_PATH,
    CONF_TELEGRAM_TOKEN,
    CONF_TELEGRAM_CHAT_ID,
    CONF_INCLUDE_AUTOMATIONS,
    CONF_INCLUDE_SCRIPTS,
    CONF_INCLUDE_SCENES,
    CONF_INCLUDE_CUSTOMIZE,
)
from .export import async_create_export, async_send_telegram

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HAConfigExportButton(hass, entry)])


class HAConfigExportButton(ButtonEntity):
    """Button zum Starten des Exports."""

    _attr_name = "HA Config Export starten"
    _attr_icon = "mdi:folder-zip-outline"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_export_button"

    async def async_press(self) -> None:
        """Wird ausgeführt wenn der Button gedrückt wird."""
        data = self._entry.data
        options = {
            CONF_INCLUDE_AUTOMATIONS: data.get(CONF_INCLUDE_AUTOMATIONS, True),
            CONF_INCLUDE_SCRIPTS: data.get(CONF_INCLUDE_SCRIPTS, True),
            CONF_INCLUDE_SCENES: data.get(CONF_INCLUDE_SCENES, True),
            CONF_INCLUDE_CUSTOMIZE: data.get(CONF_INCLUDE_CUSTOMIZE, False),
        }

        export_path = data.get(CONF_EXPORT_PATH, "/backup/")
        token = data.get(CONF_TELEGRAM_TOKEN, "")
        chat_id = data.get(CONF_TELEGRAM_CHAT_ID, "")

        zip_path = await async_create_export(self.hass, export_path, options)

        if zip_path:
            timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            message = f"✅ HA Config Export abgeschlossen\n📅 {timestamp}\n📦 Datei: {zip_path}"
            if token and chat_id:
                await async_send_telegram(token, chat_id, message, zip_path)
            _LOGGER.info("Export erfolgreich: %s", zip_path)
        else:
            message = "❌ HA Config Export fehlgeschlagen – Details im HA Log"
            if token and chat_id:
                await async_send_telegram(token, chat_id, message)
            _LOGGER.error("Export fehlgeschlagen")
