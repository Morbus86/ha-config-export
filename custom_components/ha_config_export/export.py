"""HA Config Export - Vollständige Export-Logik."""
import os
import json
import zipfile
import datetime
import logging
import aiohttp

from .const import CONFIG_YAML_FILES, STORAGE_FILES, EXCLUDED_STORAGE

_LOGGER = logging.getLogger(__name__)


def _read_file_safe(path: str) -> str:
    """Dateiinhalt lesen, Fehler abfangen."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[LESEFEHLER: {e}]"


async def async_create_export(hass, config_path: str) -> tuple[str | None, str | None]:
    """Erstellt ZIP + lesbare Textdatei für Claude-Upload.
    
    Returns: (zip_path, txt_path) – beide oder None bei Fehler.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"ha_config_export_{timestamp}.zip"
    txt_filename = f"ha_export_for_claude_{timestamp}.txt"
    zip_path = os.path.join(config_path, zip_filename)
    txt_path = os.path.join(config_path, txt_filename)

    try:
        def _write_export():
            os.makedirs(config_path, exist_ok=True)
            sections = []
            added = []
            skipped = []

            def add_section(title: str, content: str):
                sections.append(f"\n{'='*60}\n## {title}\n{'='*60}\n{content}\n")

            # 1. YAML-Dateien
            for filename in CONFIG_YAML_FILES:
                full_path = os.path.join("/config", filename)
                if os.path.exists(full_path):
                    content = _read_file_safe(full_path)
                    add_section(f"YAML: {filename}", content)
                    added.append(filename)
                else:
                    skipped.append(filename)

            # 2. packages/ Ordner
            packages_dir = "/config/packages"
            if os.path.isdir(packages_dir):
                for root, _, files in os.walk(packages_dir):
                    for file in files:
                        if file.endswith(".yaml"):
                            fpath = os.path.join(root, file)
                            rel = os.path.relpath(fpath, "/config")
                            content = _read_file_safe(fpath)
                            add_section(f"YAML: packages/{file}", content)
                            added.append(rel)

            # 3. .storage Dateien
            storage_dir = "/config/.storage"
            if os.path.isdir(storage_dir):
                for filename in STORAGE_FILES:
                    full_path = os.path.join(storage_dir, filename)
                    if os.path.exists(full_path):
                        content = _read_file_safe(full_path)
                        try:
                            parsed = json.loads(content)
                            content = json.dumps(parsed, indent=2, ensure_ascii=False)
                        except Exception:
                            pass
                        add_section(f"STORAGE: {filename}", content)
                        added.append(f".storage/{filename}")

                # Alle lovelace.* Dashboards automatisch
                for entry in sorted(os.listdir(storage_dir)):
                    if entry.startswith("lovelace.") and entry not in EXCLUDED_STORAGE:
                        full_path = os.path.join(storage_dir, entry)
                        if os.path.isfile(full_path):
                            content = _read_file_safe(full_path)
                            try:
                                parsed = json.loads(content)
                                content = json.dumps(parsed, indent=2, ensure_ascii=False)
                            except Exception:
                                pass
                            add_section(f"STORAGE: {entry}", content)
                            added.append(f".storage/{entry}")

            # Zusammenfassung am Anfang
            header = (
                f"HA CONFIG EXPORT – {timestamp}\n"
                f"Exportiert: {len(added)} Dateien\n"
                f"Nicht gefunden (optional): {len(skipped)}\n"
                f"Zweck: Upload zu Claude für Analyse\n\n"
                f"Enthaltene Dateien:\n"
            )
            for f in added:
                header += f"  + {f}\n"
            if skipped:
                header += "\nNicht gefunden:\n"
                for f in skipped:
                    header += f"  - {f}\n"

            full_text = header + "".join(sections)

            # Textdatei schreiben
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            # ZIP schreiben
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("export_summary.txt", header)
                # YAML
                for filename in CONFIG_YAML_FILES:
                    full_path = os.path.join("/config", filename)
                    if os.path.exists(full_path):
                        zf.write(full_path, arcname=f"yaml/{filename}")
                # packages
                if os.path.isdir(packages_dir):
                    for root, _, files in os.walk(packages_dir):
                        for file in files:
                            if file.endswith(".yaml"):
                                fpath = os.path.join(root, file)
                                arcname = "yaml/packages/" + os.path.relpath(fpath, packages_dir)
                                zf.write(fpath, arcname=arcname)
                # .storage
                if os.path.isdir(storage_dir):
                    for filename in STORAGE_FILES:
                        full_path = os.path.join(storage_dir, filename)
                        if os.path.exists(full_path):
                            zf.write(full_path, arcname=f"storage/{filename}")
                    for entry in os.listdir(storage_dir):
                        if entry.startswith("lovelace.") and entry not in EXCLUDED_STORAGE:
                            full_path = os.path.join(storage_dir, entry)
                            if os.path.isfile(full_path):
                                zf.write(full_path, arcname=f"storage/{entry}")
                # Textdatei auch in ZIP
                zf.write(txt_path, arcname=txt_filename)

            _LOGGER.info("Export fertig: %d Dateien → %s", len(added), zip_path)

        await hass.async_add_executor_job(_write_export)
        return zip_path, txt_path

    except Exception as err:
        _LOGGER.error("Export fehlgeschlagen: %s", err)
        return None, None


async def async_send_telegram(token: str, chat_id: str, message: str, file_path: str = None):
    """Sendet Telegram-Nachricht mit optionalem Anhang."""
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
