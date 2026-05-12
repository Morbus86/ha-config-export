"""HA Config Export - Button Entity."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import datetime
import logging

from .const import DOMAIN, CONF_EXPORT_PATH, CONF_TELEGRAM_TOKEN, CONF_TELEGRAM_CHAT_ID
from .export import async_create_export, async_send_telegram

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HAConfigExportButton(hass, entry)])


class HAConfigExportButton(ButtonEntity):
    _attr_name = "HA Config Export starten"
    _attr_icon = "mdi:folder-zip-outline"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_export_button"

    async def async_press(self) -> None:
        data = self._entry.data
        export_path = data.get(CONF_EXPORT_PATH, "/backup/")
        token = data.get(CONF_TELEGRAM_TOKEN, "")
        chat_id = data.get(CONF_TELEGRAM_CHAT_ID, "")

        zip_path, txt_path = await async_create_export(self.hass, export_path)

        if zip_path:
            timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            message = (
                f"✅ HA Config Export abgeschlossen\n"
                f"📅 {timestamp}\n"
                f"📦 ZIP: {zip_path}\n"
                f"📄 Claude-Datei: {txt_path}\n"
                f"➡️ ha_export_for_claude_*.txt in Claude hochladen"
            )
            if token and chat_id:
                await async_send_telegram(token, chat_id, message, txt_path)
            _LOGGER.info("Export erfolgreich: %s", zip_path)
        else:
            message = "❌ HA Config Export fehlgeschlagen – Details im HA Log"
            if token and chat_id:
                await async_send_telegram(token, chat_id, message)
