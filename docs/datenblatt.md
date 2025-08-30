DATENBLATT ZU REGISTERN
=======================

> Legende:
> ✓, ✗, + = wahr, falsch, gewünscht/empfohlen.
> ✓/✗ = optional o. bedingt.

# Nutzer
> `NUTZER.CSV`

| Index | Name          | Pflichtfeld | Datentyp      | Typzusatz     | Kommentar |
|------:|:--------------|:-------:|:--------------|:--------------|:----------|
| **0**     | *Signatur*      | ✓ | `Letter(str)` | Einzelner Großbuchstabe (`self.case == "upper"`). Vergabe fix. |
| **1**     | *Status*        | ✗ | `str` | `reserviert`,`besetzt`,`frei` |
| **2**     | *Nutzer*        | ✗ | `str` | - | optional  |
| **3**     | *Nutzerstatus*  | ✗ | `str` | `"user"\|"admin"` | Administration *@atesta* |
| **4**     | *Route*         | ✗ | `str` | - | optional |


# Adressen (Bücherschränke)
> `ADRESSEN.CSV`

| Index | Name | Pflicht | Typ | Datentyp | Typzusatz | Kommentar |
|------:|:-----|:-------:|:----|:--------:|:----------|:----------|
| 0 | **Route** | ✓ | Text | `str` | `"..."` | *Name der Route für Eintrag* |
| 1 | **Nummer** | ✓ | Zahl | `int` | *Ziffernfolge* | *Nummer auf der Route. Aufsteigend mit Fund. Für Einschübe nutze* Nummernsuffix. |
| 2 | **Nummernsuffix** | ✗ | Alphanumerische Zählung | `str` | RegEx: `[a-z][0-9a-z]*` | *Zählung für Einschübe. Beispiel:* `1, 1a, 1a1, 1a1a, 1a2, 1b, 2` |
| 3 | **Land** | ✓/✗ | Name | `str` | · | *Land, Nation* |
| 4 | **Region** | ✓/✗ | Name | `str` | · | *Bezirk unter* Land, *über* Stadt. *Wie 'Bundesland' für Land "de" oder 'Staat' für Land "us".* |
| 5 | **PLZ** | ✓/✗ | Zahl | `int` | · | *Postleitzahl* |
| 6 | **Stadt** | ✓/✗ | Name | `str` | · | · |
| 7 | **Strasse** | ✓/✗ | Name/Name+Nummer | `str` | `Strasse`,`"Bla-Blup-Strasse"` | *Straße* |
| 8 | **Laengengrad** | ✓/✗ | Grad | `int\|float` | · | *Längengrad. Mit* Breitengrad *alternativ für* Land+Stadt+Strasse. |
| 9 | **Breitengrad** | ✓/✗ | Grad | `int\|float` | · | *Mit* Laengengrad *alternativ für* Land+Stadt+Strasse. |
| 10 | **Datum** | + | Jahr/Datum | `datetime\|int` | `2025`, `30-08-2025` | *Datum des Funds o. der Aufnahme in die Route.* |
| 11 | Entdecker | ✗ | Name | `str\|Letter` | · | *Name oder Signatur des Nutzers für Eintrag.* |
| 12 | Verweise | ✗ | Name/Kürzel | `str` | `Name`/`"Name1; Name2;..."`/`"Name1" "Name2"...` | *Verweise auf andere Route. Aufzählung oder Nennung von Routenkürzel oder -name.* |
