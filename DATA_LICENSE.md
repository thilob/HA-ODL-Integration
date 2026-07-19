# Datenquelle und Datenlizenz

Diese Integration ruft Mess- und Metadaten aus der öffentlichen ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz (BfS) ab.

**Datenbereitsteller:** Bundesamt für Strahlenschutz (BfS)  
**Datenquelle:** ODL-Datenschnittstelle des Bundesamtes für Strahlenschutz  
**Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0  
**Lizenzkennung:** `dl-de/by-2-0`

- Lizenztext: https://www.govdata.de/dl-de/by-2-0
- Beschreibung der Datenschnittstelle: https://odlinfo.bfs.de/ODL/DE/service/datenschnittstelle/datenschnittstelle_node.html
- Technischer WFS-Dienst: https://www.imis.bfs.de/ogc/opendata/ows

## Verarbeitung durch die Integration

Die Integration wählt die vom Benutzer konfigurierten Messstellen aus der BfS-Schnittstelle aus und stellt deren Mess- und Metadaten als Home-Assistant-Entitäten dar. Sie nimmt keine fachliche Bewertung der Strahlenmesswerte vor.

Soweit Einheiten oder Werte künftig umgerechnet, korrigiert oder anderweitig inhaltlich verändert werden, muss diese Bearbeitung gemäß den Bedingungen der Datenlizenz kenntlich gemacht werden. Der aktuelle Stand übernimmt die von der Schnittstelle gelieferten Werte und Einheiten ohne inhaltliche Umrechnung.

## Abgrenzung zur Softwarelizenz

Die MIT-Lizenz in der Datei `LICENSE` gilt für den selbst geschriebenen Programmcode und die selbst erstellte Dokumentation dieses Repositorys. Sie gilt nicht für die vom BfS abgerufenen Mess- und Metadaten. Diese Daten unterliegen ausschließlich der oben genannten Datenlizenz Deutschland – Namensnennung – Version 2.0 (`dl-de/by-2-0`).

Dieses Projekt ist eine inoffizielle Home-Assistant-Integration. Es ist nicht mit dem Bundesamt für Strahlenschutz verbunden und wird nicht vom BfS herausgegeben oder unterstützt. Offizielle Logos oder sonstige geschützte Kennzeichen des BfS werden nicht verwendet.
