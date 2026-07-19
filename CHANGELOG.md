# Changelog

Alle relevanten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), und das Projekt verwendet [Semantic Versioning](https://semver.org/lang/de/).

## [0.2.6] - 2026-07-19

### Hinzugefügt

- persistenter 48-Stunden-Cache für den vollständigen Messstellen-Auswahlkatalog
- serverseitiger OGC-WFS-Filter für aktuelle Messwerte der ausgewählten Stationen
- Rückgriff auf einen vorhandenen älteren Katalog bei vorübergehenden Schnittstellenfehlern

### Geändert

- regelmäßige Aktualisierungen übertragen nur noch die ausgewählten Stationen statt des vollständigen Messnetzes

## [0.2.5] - 2026-07-19

### Hinzugefügt

- transparenter Dokumentationshinweis zum KI-gestützten Entwicklungsprozess („Vibe Coding“)

## [0.2.4] - 2026-07-19

### Geändert

- Zeitpunkt der täglichen Repository-Validierung angepasst
- Beschreibung des eigenständig erstellten Brand-Motivs präzisiert

## [0.2.3] - 2026-07-19

### Geändert

- interne Produkt- und Codebezeichnungen auf die neutrale Form „ODL-Integration“ vereinheitlicht
- sachliche BfS-Nennung auf Datenquelle, Datenbereitsteller und Lizenzhinweise beschränkt
- unzutreffende Verwendung des Datenbereitstellers als Gerätehersteller entfernt

## [0.2.2] - 2026-07-19

### Geändert

- Brand-Icons aus einer im Repository dokumentierten, selbst erstellten SVG-Vorlage neu erzeugt
- Deutschland (`DE`) als unterstütztes Land in den HACS-Metadaten ergänzt

## [0.2.1] - 2026-07-19

### Hinzugefügt

- Home-Assistant-Konfigurationsdialog zur Auswahl mehrerer ODL-Messstellen
- Sensoren für Ortsdosisleistung, kosmischen und terrestrischen Anteil, Messzeitpunkt, Stationsstatus und Prüfstatus
- konfigurierbares Abrufintervall und sofortiger Datenabruf beim Einrichten oder Ändern der Auswahl
- paginierter Abruf der öffentlichen BfS-ODL-WFS-Schnittstelle
- deutsche und englische Übersetzungen
- HACS-Metadaten, lokale Brand-Icons sowie HACS- und Hassfest-Validierung
- automatisierte Tests für die Verarbeitung der GeoJSON-Messstellendaten

[0.2.1]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.1
[0.2.2]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.2
[0.2.3]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.3
[0.2.4]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.4
[0.2.5]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.5
[0.2.6]: https://github.com/thilob/HA-ODL-Integration/releases/tag/v0.2.6
