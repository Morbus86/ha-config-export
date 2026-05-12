# Changelog

## v1.1.3 (2026-05-12)
### Neu
- Supervisor Add-ons Liste via Supervisor API (Name, Version, Status, Slug)
- `.storage/core.homeassistant` – HA-Version, Standort, Zeitzone
- `.storage/hacs` + `hacs.repositories` – installierte HACS-Pakete
- `.storage/lovelace.resources` – geladene Frontend-Ressourcen
- `.storage/energy` – Energie-Dashboard Konfiguration
### Behoben
- Log-Duplikate verhindert (break nach erster gefundener Log-Datei)

---

## v1.1.2 (2026-05-12)
### Behoben
- Log-Pfad korrigiert: HAOS speichert Log unter `/homeassistant/` nicht `/config/`
- Fallback auf `/config/home-assistant.log` für andere Installationstypen

---

## v1.1.1 (2026-05-12)
### Neu
- Fehlerprotokolle (`home-assistant.log` + `.log.1`) werden exportiert
- Telegram vorausgefüllt – Bruder muss nur noch bestätigen
- Export-Textdatei enthält jetzt vollständiges HA-Abbild für Claude-Analyse

### Geändert
- Config Flow: Dateiauswahl entfernt – Export immer vollständig
- Telegram jetzt vollständig optional (Felder leer lassen = kein Telegram)

---

## v1.1.0 (2026-05-12)
### Neu
- Vollständiger Export: YAML + `.storage` + Dashboards + Helfer + Integrationen
- `ha_export_for_claude_*.txt` – einzelne Textdatei für direkten Claude-Upload
- ZIP enthält Textdatei automatisch mit

### Geändert
- Dateiauswahl im Setup-Assistenten entfernt (alles Relevante wird automatisch exportiert)

---

## v1.0.1 (2026-05-12)
### Behoben
- Zielverzeichnis wird automatisch erstellt falls nicht vorhanden (`os.makedirs`)

---

## v1.0.0 (2026-05-12)
### Erstveröffentlichung
- Button-Entity zum Auslösen des Exports
- YAML-Dateien exportierbar (konfigurierbar)
- Telegram-Benachrichtigung mit ZIP-Anhang
- 3-stufiger Setup-Assistent
