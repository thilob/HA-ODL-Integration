# Brand-Assets

Die Brand-Icons der Integration wurden für dieses Projekt eigenständig erstellt. Die bearbeitbare Quelle ist [`custom_components/bfs_odl/brand/icon.svg`](custom_components/bfs_odl/brand/icon.svg). `icon.png` und `icon@2x.png` werden ausschließlich aus dieser SVG-Datei gerendert.

Das Motiv ist eine eigene, stilisierte Darstellung eines Strahlenwarnzeichens. Es verwendet kein Logo, Wappen oder sonstiges Markenzeichen des Bundesamtes für Strahlenschutz, der Bundesrepublik Deutschland, der Internationalen Atomenergie-Organisation oder der Internationalen Organisation für Normung.

Die SVG-Datei und die daraus erzeugten PNG-Dateien stehen wie der übrige selbst erstellte Projektcode unter der MIT-Lizenz; siehe [`LICENSE`](LICENSE).

## Reproduzierbare Erzeugung

Mit ImageMagick können die PNG-Dateien aus der SVG-Quelle neu erzeugt werden:

```bash
magick -background none custom_components/bfs_odl/brand/icon.svg -resize 256x256 custom_components/bfs_odl/brand/icon.png
magick -background none custom_components/bfs_odl/brand/icon.svg -resize 512x512 custom_components/bfs_odl/brand/icon@2x.png
```
