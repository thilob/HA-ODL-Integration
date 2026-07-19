# ODL-Messwerte für Home Assistant

Eine inoffizielle Home-Assistant-Custom-Integration für die öffentliche ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz (BfS).

## Funktionen

- lädt die vollständige Messstellenliste paginiert aus dem Layer `odlinfo_odl_1h_latest`
- Auswahl einer oder mehrerer Messstellen im Home-Assistant-Konfigurationsdialog
- Änderung der Auswahl über **Konfigurieren** ohne YAML
- gemeinsamer, ressourcenschonender Datenabruf über einen `DataUpdateCoordinator`
- konfigurierbares Abrufintervall von 10 bis 180 Minuten, Standard 30 Minuten
- pro Messstelle ein Home-Assistant-Gerät mit folgenden Entitäten:
  - Ortsdosisleistung
  - kosmischer Anteil
  - terrestrischer Anteil
  - Messzeitpunkt
  - Stationsstatus
  - Prüfstatus
- Koordinaten, Höhe, Postleitzahl, Messstellenkennung und weitere Metadaten als Attribute
- Quellen-, Lizenz- und Schnittstellenhinweise als Attribute jeder Entität

## Installation zum Testen

1. Das Verzeichnis `custom_components/bfs_odl` nach `/config/custom_components/bfs_odl` kopieren.
2. Home Assistant neu starten.
3. **Einstellungen → Geräte & Dienste → Integration hinzufügen** öffnen.
4. Nach **ODL-Messwerte für Home Assistant** suchen.
5. Messstellen auswählen und speichern.

## Installation über HACS als benutzerdefiniertes Repository

1. In HACS **Benutzerdefinierte Repositories** öffnen.
2. `https://github.com/thilob/HA-ODL-Integration` eintragen und als Kategorie **Integration** wählen.
3. Integration herunterladen, Home Assistant neu starten und anschließend über **Geräte & Dienste** einrichten.

## Datenabruf

Basis-URL:

```text
https://www.imis.bfs.de/ogc/opendata/ows
```

Verwendeter WFS-Layer:

```text
opendata:odlinfo_odl_1h_latest
```

Da die Schnittstelle mehr als 1.000 Stationen liefern kann, ruft die Integration die Daten mit `maxFeatures=1000` und fortlaufendem `startIndex` ab. Die ausgewählten Stationen werden anschließend lokal herausgefiltert. Dadurch entstehen unabhängig von der Zahl ausgewählter Stationen nur wenige Sammelabfragen pro Aktualisierung.

## Datenquelle und Datenlizenz

**Datenbereitsteller:** Bundesamt für Strahlenschutz (BfS)  
**Datenquelle:** ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz  
**Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`)

- Lizenztext: https://www.govdata.de/dl-de/by-2-0
- Beschreibung der Datenschnittstelle: https://odlinfo.bfs.de/ODL/DE/service/datenschnittstelle/datenschnittstelle_node.html
- Technischer WFS-Dienst: https://www.imis.bfs.de/ogc/opendata/ows

Die Integration übernimmt die von der Schnittstelle gelieferten Messwerte und Einheiten ohne fachliche Bewertung oder inhaltliche Korrektur. Sie führt lediglich eine technische Auswahl und Darstellung in Home Assistant durch. Weitere Einzelheiten stehen in [`DATA_LICENSE.md`](DATA_LICENSE.md).

## Softwarelizenz und Abgrenzung

Der selbst geschriebene Programmcode und die selbst erstellte Dokumentation dieses Repositorys stehen unter der MIT-Lizenz; siehe [`LICENSE`](LICENSE). Die MIT-Lizenz gilt **nicht** für die vom BfS abgerufenen Mess- und Metadaten. Diese unterliegen ausschließlich der oben genannten Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`). Eine kompakte Übersicht der Lizenzabgrenzung enthält [`NOTICE.md`](NOTICE.md).

Dieses Projekt ist nicht mit dem Bundesamt für Strahlenschutz verbunden, wird nicht vom BfS herausgegeben oder unterstützt und verwendet keine offiziellen BfS-Logos.

## Hinweise

- Die Werte können geprüft oder ungeprüft sein; der Prüfstatus wird als eigene Entität bereitgestellt.
- Die Integration interpretiert oder bewertet die Strahlenwerte nicht.
- Bei einem vorübergehenden Ausfall der Schnittstelle markiert Home Assistant die Entitäten als nicht verfügbar und versucht den Abruf später erneut.

## Entwicklung

Syntaxprüfung:

```bash
python -m compileall custom_components/bfs_odl
```

Für ein öffentliches HACS-Repository sollten zusätzlich die HACS- und Hassfest-GitHub-Actions aktiviert werden.
