DOMAIN = "ha_config_export"

CONF_EXPORT_PATH = "export_path"
CONF_TELEGRAM_TOKEN = "telegram_token"
CONF_TELEGRAM_CHAT_ID = "telegram_chat_id"
CONF_INCLUDE_AUTOMATIONS = "include_automations"
CONF_INCLUDE_SCRIPTS = "include_scripts"
CONF_INCLUDE_SCENES = "include_scenes"
CONF_INCLUDE_CUSTOMIZE = "include_customize"

DEFAULT_EXPORT_PATH = "/backup/"

BASE_FILES = ["configuration.yaml"]

OPTIONAL_FILES = {
    CONF_INCLUDE_AUTOMATIONS: "automations.yaml",
    CONF_INCLUDE_SCRIPTS: "scripts.yaml",
    CONF_INCLUDE_SCENES: "scenes.yaml",
    CONF_INCLUDE_CUSTOMIZE: "customize.yaml",
}

EXCLUDED_FILES = ["secrets.yaml", ".storage", "auth"]
