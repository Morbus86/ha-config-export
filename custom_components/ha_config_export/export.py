"""HA Config Export - Core export logic."""
import os
import zipfile
import datetime
import logging
import aiohttp

from .const import BASE_FILES, OPTIONAL_FILES, EXCLUDED_FILES

_LOGGER = logging.getLogger(__name__)


async def async_create_export(hass, config_path: str, options: dict) -> str | None:
    """Create a ZIP of selected config files. Returns path to ZIP or None on error."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"ha_config_export_{timestamp}.zip"
    zip_path = os.path.join(config_path, zip_filename)

    files_to_add = list(BASE_FILES)
    for key, filename in OPTIONAL_FILES.items():
        if options.get(key, True):
            files_to_add.append(filename)

    try:
        def _write_zip():
            os.makedirs(config_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for filename in files_to_add:
                    full_path = os.path.join("/config", filename)
                    if os.path.exists(full_path):
                        zf.write(full_path, arcname=filename)
                        _LOGGER.debug("Added to ZIP: %s", filename)
                    else:
                        _LOGGER.warning("File not found, skipping: %s", filename)

                packages_dir = "/config/packages"
                if options.get("include_packages", False) and os.path.isdir(packages_dir):
                    for root, _, files in os.walk(packages_dir):
                        for file in files:
                            if file.endswith(".yaml"):
                                fpath = os.path.join(root, file)
                                arcname = os.path.relpath(fpath, "/config")
                                zf.write(fpath, arcname=arcname)

        await hass.async_add_executor_job(_write_zip)
        _LOGGER.info("Export ZIP created: %s", zip_path)
        return zip_path
    except Exception as err:
        _LOGGER.error("Failed to create export ZIP: %s", err)
        return None


async def async_send_telegram(token: str, chat_id: str, message: str, file_path: str = None):
    """Send Telegram message and optionally a document."""
    async with aiohttp.ClientSession() as session:
        try:
            if file_path and os.path.exists(file_path):
                url = f"https://api.telegram.org/bot{token}/sendDocument"
                with open(file_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("chat_id", chat_id)
                    data.add_field("caption", message)
                    data.add_field("document", f, filename=os.path.basename(file_path))
                    async with session.post(url, data=data) as resp:
                        if resp.status != 200:
                            _LOGGER.error("Telegram sendDocument failed: %s", await resp.text())
            else:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {"chat_id": chat_id, "text": message}
                async with session.post(url, json=payload) as resp:
                    if resp.status != 200:
                        _LOGGER.error("Telegram sendMessage failed: %s", await resp.text())
        except Exception as err:
            _LOGGER.error("Telegram error: %s", err)
