# HA Config Export

HACS-Integration für Home Assistant, die mit einem Button-Druck eine vollständige Übersicht deines HA-Systems als Textdatei exportiert – für Diagnose und Optimierung durch Claude AI.

## 📦 Was wird exportiert?

- **YAML-Konfigurationen** – `configuration.yaml`, `automations.yaml`, `scripts.yaml`, `scenes.yaml`, `customize.yaml`, `packages/`
- **`.storage` Dateien** – Helfer, Dashboards, Integrationen, Geräte, Entitäten, Bereiche, HACS-Konfiguration
- **System-Diagnose** – HA-Version, Host-Info (CPU/RAM/Disk), OS-Info, Network-Info
- **Add-ons** – Liste aller installierten Add-ons mit Version und Status
- **Logs (letzte 500KB je Quelle):**
  - HA Core Log
  - Host/Kernel Log (wichtig für Hardware-/Netzwerk-Probleme)
  - Supervisor Log
  - DNS Log (wichtig für Erreichbarkeitsprobleme)

**Niemals exportiert:** Passwörter, Auth-Tokens, Cloud-Credentials, sensible Auth-Dateien.

## 🚀 Installation

📖 **[Vollständige Installationsanleitung mit Screenshots (HTML)](docs/installation.html)**

### Kurzversion:

1. **HACS → Benutzerdefinierte Repositories** → URL `https://github.com/Morbus86/ha-config-export` → Kategorie `Integration`
2. **HACS → Integrationen** → „HA Config Export" suchen → **Herunterladen** → HA neu starten
3. **Einstellungen → Geräte & Dienste → Integration hinzufügen** → „HA Config Export"
4. Setup-Assistent durchklicken (Telegram-Daten sind vorausgefüllt)

## 📲 Verwendung

Nach der Einrichtung erscheint der Button **„HA Config Export starten"**.

Beim Drücken:
1. Vollständige Konfiguration wird zusammengestellt
2. Als `ha_export_for_claude_*.txt` in `/backup/` gespeichert
3. Per Telegram an den konfigurierten Empfänger gesendet
4. Empfänger lädt die Datei in einen Claude-Chat hoch für vollständige Analyse

## 🔧 Voraussetzungen

- Home Assistant OS, Container oder Supervised (für vollständige Diagnose mit Supervisor-Logs)
- HACS installiert
- Optional: OneDrive-Backup-Integration (Datei wird dort automatisch synchronisiert)
- Optional: Telegram-Bot (vorausgefüllt mit Standard-Empfänger)

## 📋 Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)

## 🛠️ Entwicklung

Erstellt mit [Claude](https://claude.ai) | Lizenz: MIT
