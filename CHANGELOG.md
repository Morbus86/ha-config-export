# Changelog

## v1.2.0 (2026-05-12)
### Neu – Dokumentation
- **Vollständige Installationsanleitung als HTML** unter `docs/installation.html`
  - Mit eingebetteten Screenshots (selbst-enthaltene Datei)
  - Schritt-für-Schritt von HACS-Setup bis Button-Druck
  - Per Mail teilbar oder direkt aus dem Repo aufrufbar
- **README.md überarbeitet** – Feature-Liste, Kurzanleitung, Voraussetzungen

---

## v1.1.5 (2026-05-12)
### Behoben
- **Blocking-Call-Warnung im HA-Core-Log entfernt**: Telegram-Datei wird jetzt im Executor-Thread gelesen statt in der Event Loop. Verhindert die `homeassistant.util.loop` Warnung bei jedem Export.

---

## v1.1.4 (2026-05-12)
### Neu – Kritische Logs für Diagnose
- **HA Core Log** via Supervisor API (`/core/logs`)
- **Host/Kernel Log** via Supervisor API (`/host/logs`) – wichtig für Hardware-/Netzwerk-Probleme
- **Supervisor Log** via Supervisor API (`/supervisor/logs`)
- **DNS Log** via Supervisor API (`/dns/logs`) – wichtig für Erreichbarkeitsprobleme
### Neu – System-Diagnose-Infos
- Host Info (CPU, RAM, Disk)
- OS Info (HAOS Version, Updates)
- Network Info (Adapter, IPs, DNS-Server)
- Core Info (HA-Version, Konfiguration)
### Neu – Storage
- `.storage/hacs.*` (alle HACS-Dateien automatisch)
- `.storage/lovelace.resources` (Frontend-Ressourcen)
### Geändert
- Logs auf 500KB pro Quelle gekürzt (verhindert riesige Exports)
- Lokale Log-Datei als Fallback wenn Supervisor API nicht verfügbar

---

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
