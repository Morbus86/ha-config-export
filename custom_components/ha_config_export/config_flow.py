"""HA Config Export - Config Flow (vereinfacht)."""
import voluptuous as vol
from homeassistant import config_entries
import aiohttp

from .const import (
    DOMAIN,
    CONF_EXPORT_PATH,
    CONF_TELEGRAM_TOKEN,
    CONF_TELEGRAM_CHAT_ID,
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
            return await self.async_step_telegram()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EXPORT_PATH, default=DEFAULT_EXPORT_PATH): str,
            }),
            errors=errors,
        )

    async def async_step_telegram(self, user_input=None):
        """Schritt 2: Telegram-Benachrichtigung."""
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
            errors=errors,
        )

    def _create_entry(self, token, chat_id):
        return self.async_create_entry(
            title="HA Config Export",
            data={
                CONF_EXPORT_PATH: self._export_path,
                CONF_TELEGRAM_TOKEN: token,
                CONF_TELEGRAM_CHAT_ID: chat_id,
            }
        )

    async def _test_telegram(self, token: str, chat_id: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/getMe"
                async with session.get(url) as resp:
                    return resp.status == 200
        except Exception:
            return False
