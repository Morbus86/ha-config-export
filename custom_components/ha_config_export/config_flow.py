"""HA Config Export - Config Flow (Setup-Assistent)."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import aiohttp

from .const import (
    DOMAIN,
    CONF_EXPORT_PATH,
    CONF_TELEGRAM_TOKEN,
    CONF_TELEGRAM_CHAT_ID,
    CONF_INCLUDE_AUTOMATIONS,
    CONF_INCLUDE_SCRIPTS,
    CONF_INCLUDE_SCENES,
    CONF_INCLUDE_CUSTOMIZE,
    DEFAULT_EXPORT_PATH,
)


class HAConfigExportConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Schritt-für-Schritt Setup."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Schritt 1: Export-Pfad."""
        errors = {}
        if user_input is not None:
            self._export_path = user_input[CONF_EXPORT_PATH]
            return await self.async_step_files()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EXPORT_PATH, default=DEFAULT_EXPORT_PATH): str,
            }),
            description_placeholders={
                "info": "Pfad wo die ZIP-Datei gespeichert wird (z.B. /backup/ für OneDrive-Sync)"
            },
            errors=errors,
        )

    async def async_step_files(self, user_input=None):
        """Schritt 2: Welche Dateien exportieren?"""
        if user_input is not None:
            self._file_options = user_input
            return await self.async_step_telegram()

        return self.async_show_form(
            step_id="files",
            data_schema=vol.Schema({
                vol.Required(CONF_INCLUDE_AUTOMATIONS, default=True): bool,
                vol.Required(CONF_INCLUDE_SCRIPTS, default=True): bool,
                vol.Required(CONF_INCLUDE_SCENES, default=True): bool,
                vol.Required(CONF_INCLUDE_CUSTOMIZE, default=False): bool,
            }),
        )

    async def async_step_telegram(self, user_input=None):
        """Schritt 3: Telegram-Benachrichtigung (optional)."""
        errors = {}
        if user_input is not None:
            token = user_input.get(CONF_TELEGRAM_TOKEN, "").strip()
            chat_id = user_input.get(CONF_TELEGRAM_CHAT_ID, "").strip()

            if token and chat_id:
                valid = await self._test_telegram(token, chat_id)
                if not valid:
                    errors["base"] = "telegram_invalid"
                else:
                    return self._create_entry(token, chat_id)
            else:
                return self._create_entry("", "")

        return self.async_show_form(
            step_id="telegram",
            data_schema=vol.Schema({
                vol.Optional(CONF_TELEGRAM_TOKEN, default=""): str,
                vol.Optional(CONF_TELEGRAM_CHAT_ID, default=""): str,
            }),
            description_placeholders={
                "info": "Leer lassen um Telegram zu überspringen"
            },
            errors=errors,
        )

    def _create_entry(self, token, chat_id):
        data = {
            CONF_EXPORT_PATH: self._export_path,
            CONF_TELEGRAM_TOKEN: token,
            CONF_TELEGRAM_CHAT_ID: chat_id,
        }
        data.update(self._file_options)
        return self.async_create_entry(title="HA Config Export", data=data)

    async def _test_telegram(self, token: str, chat_id: str) -> bool:
        """Telegram-Verbindung testen."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/getMe"
                async with session.get(url) as resp:
                    return resp.status == 200
        except Exception:
            return False
