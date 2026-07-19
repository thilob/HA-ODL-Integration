# ODL-Messwerte für Home Assistant

Eine inoffizielle Home-Assistant-Custom-Integration für die öffentliche ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz (BfS).

[![HACS öffnen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=thilob&repository=HA-ODL-Integration&category=integration)

## Funktionen

- lädt die vollständige Messstellenliste paginiert und speichert den Auswahlkatalog 48 Stunden persistent zwischen
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

1. Den Button **HACS öffnen** oben verwenden oder in HACS **Benutzerdefinierte Repositories** öffnen.
2. Falls das Repository manuell hinzugefügt wird, `https://github.com/thilob/HA-ODL-Integration` eintragen und als Kategorie **Integration** wählen.
3. Die Integration herunterladen.
4. Home Assistant vollständig neu starten.
5. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **ODL-Messwerte für Home Assistant** suchen und die gewünschten Messstellen auswählen.

## Aktualisierung

Updates werden in HACS angezeigt und können dort installiert werden. Nach jeder Aktualisierung der Integration muss Home Assistant neu gestartet werden. Änderungen an Messstellenauswahl und Abrufintervall sind anschließend über **Konfigurieren** möglich und lösen automatisch ein Neuladen mit sofortigem Datenabruf aus.

## Datenabruf

Basis-URL:

```text
https://www.imis.bfs.de/ogc/opendata/ows
```

Verwendeter WFS-Layer:

```text
opendata:odlinfo_odl_1h_latest
```

Da die Schnittstelle mehr als 1.000 Stationen liefern kann, wird der vollständige Messstellenkatalog bei Bedarf mit `maxFeatures=1000` und fortlaufendem `startIndex` geladen. Dieser Katalog enthält nur die für den Auswahldialog benötigten Bezeichnungen und wird 48 Stunden persistent im Home-Assistant-Storage zwischengespeichert. Der Cache übersteht damit Integrations-Reloads und Home-Assistant-Neustarts. Ist eine Aktualisierung vorübergehend nicht möglich, bleibt ein vorhandener älterer Katalog für die Konfiguration nutzbar.

Die regelmäßige Messwertaktualisierung verwendet den Katalogcache nicht. Sie fragt die aktuell ausgewählten Messstellen mit einem serverseitigen OGC-WFS-Filter direkt aus dem Layer `odlinfo_odl_1h_latest` ab. Dadurch bleiben die Messwerte aktuell, während pro Poll nur die benötigten Stationen übertragen werden.

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

## Entwicklungsprozess und Vibe Coding

Dieses Projekt wurde in einem KI-gestützten Entwicklungsprozess erstellt und weiterentwickelt, der auch als **Vibe Coding** bezeichnet wird. KI-Werkzeuge unterstützen dabei unter anderem Entwurf, Implementierung, Dokumentation und Tests. Die Verantwortung für veröffentlichte Änderungen, Lizenzangaben und den Betrieb des Projekts verbleibt beim Maintainer. Automatisierte HACS-, Hassfest- und Unit-Test-Prüfungen reduzieren Fehler, können eine vollständige fachliche oder sicherheitstechnische Prüfung jedoch nicht garantieren. Fehler und Verbesserungsvorschläge können über den [GitHub-Issue-Tracker](https://github.com/thilob/HA-ODL-Integration/issues) gemeldet werden.

## Entwicklung

Tests und Syntaxprüfung:

```bash
python -m unittest discover -s tests -v
python -m compileall custom_components/bfs_odl
```

Änderungen werden auf GitHub automatisch mit HACS, Hassfest und den Unit-Tests validiert. Veröffentlichte Änderungen sind im [`CHANGELOG.md`](CHANGELOG.md) dokumentiert.
