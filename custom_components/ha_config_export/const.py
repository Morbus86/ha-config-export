DOMAIN = "ha_config_export"

CONF_EXPORT_PATH = "export_path"
CONF_TELEGRAM_TOKEN = "telegram_token"
CONF_TELEGRAM_CHAT_ID = "telegram_chat_id"

DEFAULT_EXPORT_PATH = "/backup/"

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

# .storage Dateien – alles was UI-Konfiguration enthält
STORAGE_FILES = [
    "core.config_entries",
    "core.entity_registry",
    "core.device_registry",
    "core.area_registry",
    "lovelace",
    "lovelace.dashboard_default",
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
    "automation",
    "script",
    "scene",
    "template",
    "helpers",
]

# NIEMALS exportieren
EXCLUDED_STORAGE = [
    "auth",
    "auth_provider.homeassistant",
    "onboarding",
    "cloud",
    "google_assistant",
]
