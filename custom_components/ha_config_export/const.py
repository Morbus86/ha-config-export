DOMAIN = "ha_config_export"

CONF_EXPORT_PATH = "export_path"
CONF_TELEGRAM_TOKEN = "telegram_token"
CONF_TELEGRAM_CHAT_ID = "telegram_chat_id"

DEFAULT_EXPORT_PATH = "/backup/"

# Vorausgefüllte Standardwerte (Gregor's HA Claude Bridge Bot)
DEFAULT_TELEGRAM_TOKEN = "8720209745:AAHSj6nu-hmmwyHkcg8vezHsaQZ9FioFI_k"
DEFAULT_TELEGRAM_CHAT_ID = "67511843"

# YAML-Dateien aus /config/
CONFIG_YAML_FILES = [
    "configuration.yaml",
    "automations.yaml",
    "scripts.yaml",
    "scenes.yaml",
    "customize.yaml",
    "groups.yaml",
    "input_boolean.yaml",
    "input_number.yaml",
    "input_text.yaml",
    "input_select.yaml",
    "input_datetime.yaml",
    "template.yaml",
    "switch.yaml",
    "sensor.yaml",
    "binary_sensor.yaml",
    "alert.yaml",
    "rest_command.yaml",
    "shell_command.yaml",
]

# .storage Dateien
STORAGE_FILES = [
    # Kern-System
    "core.config_entries",
    "core.entity_registry",
    "core.device_registry",
    "core.area_registry",
    "core.homeassistant",
    # Helfer
    "input_boolean",
    "input_number",
    "input_text",
    "input_select",
    "input_datetime",
    "counter",
    "timer",
    "schedule",
    "person",
    "zone",
    # UI-Konfigurationen
    "lovelace",
    "lovelace.resources",
    "energy",
    # Automationen & Skripte (UI-erstellt)
    "automation",
    "script",
    "scene",
    "template",
    "helpers",
    # HACS
    "hacs",
    "hacs.repositories",
]

# Log-Dateien (HAOS + andere Installationstypen)
LOG_FILES = [
    "/homeassistant/home-assistant.log",
    "/homeassistant/home-assistant.log.1",
    "/config/home-assistant.log",
    "/config/home-assistant.log.1",
]

# NIEMALS exportieren
EXCLUDED_STORAGE = [
    "auth",
    "auth_provider.homeassistant",
    "onboarding",
    "cloud",
    "google_assistant",
]
