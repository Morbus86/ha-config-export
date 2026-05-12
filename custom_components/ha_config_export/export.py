"""HA Config Export - Vollständige Export-Logik."""
import os
import json
import zipfile
import datetime
import logging
import aiohttp

from .const import CONFIG_YAML_FILES, STORAGE_FILES, EXCLUDED_STORAGE, LOG_FILES

_LOGGER = logging.getLogger(__name__)

# Maximale Log-Größe pro Quelle (Bytes) - verhindert riesige Exporte
MAX_LOG_SIZE = 500_000  # 500 KB


def _read_file_safe(path: str, max_size: int = None) -> str:
    """Datei lesen, optional auf max_size beschränken (letzte N Bytes)."""
    try:
        size = os.path.getsize(path)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if max_size and size > max_size:
                f.seek(size - max_size)
                content = f.read()
                return f"[... gekürzt auf letzte {max_size} Bytes ...]\n{content}"
            return f.read()
    except Exception as e:
        return f"[LESEFEHLER: {e}]"


async def _supervisor_get(endpoint: str, as_json: bool = True) -> str:
    """Supervisor API Aufruf. Gibt JSON-Inhalt oder Text zurück."""
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        return "[Supervisor API nicht verfügbar – kein HAOS?]"
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"http://supervisor/{endpoint}"
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    if as_json:
                        return await resp.text()
                    else:
                        text = await resp.text()
                        # Logs auf MAX_LOG_SIZE kürzen
                        if len(text) > MAX_LOG_SIZE:
                            text = f"[... gekürzt auf letzte {MAX_LOG_SIZE} Bytes ...]\n" + text[-MAX_LOG_SIZE:]
                        return text
                else:
                    return f"[HTTP {resp.status} – {endpoint}]"
    except Exception as e:
        return f"[Supervisor API Fehler bei {endpoint}: {e}]"


async def async_create_export(hass, config_path: str) -> tuple[str | None, str | None]:
    """Erstellt ZIP + lesbare Textdatei für Claude-Upload."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"ha_config_export_{timestamp}.zip"
    txt_filename = f"ha_export_for_claude_{timestamp}.txt"
    zip_path = os.path.join(config_path, zip_filename)
    txt_path = os.path.join(config_path, txt_filename)

    # Alle Supervisor-Daten async sammeln
    _LOGGER.info("Sammle Supervisor-Daten...")
    supervisor_data = {
        "addons": await _supervisor_get("addons"),
        "info": await _supervisor_get("info"),
        "host_info": await _supervisor_get("host/info"),
        "os_info": await _supervisor_get("os/info"),
        "network_info": await _supervisor_get("network/info"),
        "core_info": await _supervisor_get("core/info"),
        "core_log": await _supervisor_get("core/logs", as_json=False),
        "host_log": await _supervisor_get("host/logs", as_json=False),
        "supervisor_log": await _supervisor_get("supervisor/logs", as_json=False),
        "dns_log": await _supervisor_get("dns/logs", as_json=False),
    }

    try:
        def _write_export():
            os.makedirs(config_path, exist_ok=True)
            sections = []
            added = []
            skipped = []

            def add_section(title: str, content: str):
                sections.append(f"\n{'='*60}\n## {title}\n{'='*60}\n{content}\n")

            # 0. Supervisor / System
            add_section("SUPERVISOR: Add-ons", supervisor_data["addons"])
            add_section("SUPERVISOR: System Info", supervisor_data["info"])
            add_section("SUPERVISOR: Host Info (CPU, RAM, Disk)", supervisor_data["host_info"])
            add_section("SUPERVISOR: OS Info (HAOS Version, Updates)", supervisor_data["os_info"])
            add_section("SUPERVISOR: Network Info (Adapter, IPs, DNS)", supervisor_data["network_info"])
            add_section("SUPERVISOR: Core Info (HA Version)", supervisor_data["core_info"])
            added.extend([
                "supervisor/addons", "supervisor/info", "supervisor/host_info",
                "supervisor/os_info", "supervisor/network_info", "supervisor/core_info"
            ])

            # 1. KRITISCHE LOGS (für Diagnose)
            add_section("LOG: HA Core (letzte 500KB)", supervisor_data["core_log"])
            add_section("LOG: Host/Kernel (letzte 500KB)", supervisor_data["host_log"])
            add_section("LOG: Supervisor (letzte 500KB)", supervisor_data["supervisor_log"])
            add_section("LOG: DNS (letzte 500KB)", supervisor_data["dns_log"])
            added.extend([
                "log/ha_core", "log/host_kernel", "log/supervisor", "log/dns"
            ])

            # 2. YAML-Dateien
            for filename in CONFIG_YAML_FILES:
                full_path = os.path.join("/config", filename)
                if os.path.exists(full_path):
                    add_section(f"YAML: {filename}", _read_file_safe(full_path))
                    added.append(filename)
                else:
                    skipped.append(filename)

            # 3. packages/ Ordner
            packages_dir = "/config/packages"
            if os.path.isdir(packages_dir):
                for root, _, files in os.walk(packages_dir):
                    for file in sorted(files):
                        if file.endswith(".yaml"):
                            fpath = os.path.join(root, file)
                            rel = os.path.relpath(fpath, "/config")
                            add_section(f"YAML: packages/{file}", _read_file_safe(fpath))
                            added.append(rel)

            # 4. .storage Dateien
            storage_dir = "/config/.storage"
            if os.path.isdir(storage_dir):
                for filename in STORAGE_FILES:
                    full_path = os.path.join(storage_dir, filename)
                    if os.path.exists(full_path):
                        content = _read_file_safe(full_path)
                        try:
                            content = json.dumps(json.loads(content), indent=2, ensure_ascii=False)
                        except Exception:
                            pass
                        add_section(f"STORAGE: {filename}", content)
                        added.append(f".storage/{filename}")

                # lovelace.* + hacs.* Dashboards/Daten automatisch
                for entry in sorted(os.listdir(storage_dir)):
                    if entry in EXCLUDED_STORAGE:
                        continue
                    if entry.startswith("lovelace.") or entry.startswith("hacs."):
                        full_path = os.path.join(storage_dir, entry)
                        if os.path.isfile(full_path) and f".storage/{entry}" not in added:
                            content = _read_file_safe(full_path)
                            try:
                                content = json.dumps(json.loads(content), indent=2, ensure_ascii=False)
                            except Exception:
                                pass
                            add_section(f"STORAGE: {entry}", content)
                            added.append(f".storage/{entry}")

            # 5. Fallback: Lokale Log-Dateien (falls Supervisor API nicht klappt)
            for log_path in LOG_FILES:
                if os.path.exists(log_path):
                    add_section(
                        f"LOG: {os.path.basename(log_path)} (Datei-Fallback)",
                        _read_file_safe(log_path, max_size=MAX_LOG_SIZE)
                    )
                    added.append(f"file:{os.path.basename(log_path)}")
                    break

            # Header
            header = (
                f"HA CONFIG EXPORT – {timestamp}\n"
                f"Exportiert: {len(added)} Sektionen\n"
                f"Nicht gefunden (optional): {len(skipped)}\n"
                f"Zweck: Vollständige HA-Diagnose inkl. System/Kernel/Netzwerk-Logs\n\n"
                f"Inhalt:\n"
            )
            for f in added:
                header += f"  + {f}\n"
            if skipped:
                header += "\nNicht gefunden (optional):\n"
                for f in skipped:
                    header += f"  - {f}\n"

            full_text = header + "".join(sections)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            # ZIP
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("export_summary.txt", header)
                # Supervisor Daten als einzelne Dateien
                for key, content in supervisor_data.items():
                    zf.writestr(f"supervisor/{key}.txt", content)
                # YAML
                for filename in CONFIG_YAML_FILES:
                    fp = os.path.join("/config", filename)
                    if os.path.exists(fp):
                        zf.write(fp, arcname=f"yaml/{filename}")
                if os.path.isdir(packages_dir):
                    for root, _, files in os.walk(packages_dir):
                        for file in files:
                            if file.endswith(".yaml"):
                                fpath = os.path.join(root, file)
                                zf.write(fpath, arcname="yaml/packages/" + os.path.relpath(fpath, packages_dir))
                # Storage
                if os.path.isdir(storage_dir):
                    for filename in STORAGE_FILES:
                        fp = os.path.join(storage_dir, filename)
                        if os.path.exists(fp):
                            zf.write(fp, arcname=f"storage/{filename}")
                    for entry in os.listdir(storage_dir):
                        if entry in EXCLUDED_STORAGE:
                            continue
                        if entry.startswith("lovelace.") or entry.startswith("hacs."):
                            fp = os.path.join(storage_dir, entry)
                            if os.path.isfile(fp):
                                zf.write(fp, arcname=f"storage/{entry}")
                # Textdatei mit rein
                zf.write(txt_path, arcname=txt_filename)

            _LOGGER.info("Export fertig: %d Sektionen → %s", len(added), zip_path)

        await hass.async_add_executor_job(_write_export)
        return zip_path, txt_path

    except Exception as err:
        _LOGGER.error("Export fehlgeschlagen: %s", err)
        return None, None


async def async_send_telegram(token: str, chat_id: str, message: str, file_path: str = None):
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
                async with session.post(url, json={"chat_id": chat_id, "text": message}) as resp:
                    if resp.status != 200:
                        _LOGGER.error("Telegram sendMessage failed: %s", await resp.text())
        except Exception as err:
            _LOGGER.error("Telegram error: %s", err)
