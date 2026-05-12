# HA Config Export

HACS-Integration zum Exportieren der Home Assistant Konfiguration als ZIP-Datei mit optionaler Telegram-Benachrichtigung.

## Features
- Ein-Klick Export via Button in der HA-Oberfläche
- Wähle welche YAML-Dateien exportiert werden
- Secrets werden **niemals** exportiert
- Telegram-Benachrichtigung mit ZIP-Anhang (optional)
- Kompatibel mit OneDrive-Backup Integrationen (Zielordner frei wählbar)

## Installation via HACS

1. HACS öffnen → Integrationen → ⋮ → Benutzerdefinierte Repositories
2. URL eintragen: `https://github.com/Morbus86/ha-config-export`
3. Kategorie: `Integration`
4. Hinzufügen klicken
5. Integration suchen: "HA Config Export" → Installieren

## Einrichtung

Nach der Installation: **Geräte & Dienste → Integration hinzufügen → HA Config Export**

Der Setup-Assistent führt durch 3 Schritte:

| Schritt | Was wird abgefragt |
|---------|-------------------|
| 1 | Zielordner für die ZIP (Standard: `/backup/`) |
| 2 | Welche YAML-Dateien sollen exportiert werden |
| 3 | Telegram Bot-Token + Chat-ID (optional) |

## Verwendung

Nach der Einrichtung erscheint ein neuer Button in HA:  
**"HA Config Export starten"**

Drücken → ZIP wird erstellt → Optional: Telegram-Nachricht mit ZIP-Anhang

## Sicherheit

- `secrets.yaml` wird grundsätzlich ausgeschlossen
- `.storage/` wird nicht exportiert
- Es werden nur YAML-Konfigurationsdateien exportiert

## Entwicklung

Erstellt mit [Claude](https://claude.ai) | Lizenz: MIT
