DATENBLATT ZU REGISTERN
=======================

**`NUTZER.CSV`**

| Index | Name          | Pflicht | Datentyp      | Typzusatz     | Kommentar |
|------:|:--------------|:-------:|:--------------|:--------------|:----------|
| **0**     | *Signatur*      | 1 | `Letter(str)` | Einzelner Großbuchstabe (`self.case == "upper"`). Vergabe fix. |
| **1**     | *Status*        | 1 | `str` | `reserviert`,`besetzt`,`frei` |
| **2**     | *Nutzer*        | 0 | `str` | - | optional  |
| **3**     | *Nutzerstatus*  | 0 | `str` | `"user"\|"admin"` | Administration *@atesta* |
| **4**     | *Route*         | 0 | `str` | - | optional |


**`ADRESSEN.CSV`**

| Index | Name | Pflicht | Typ | Datentyp      | Typzusatz     | Kommentar |
|------:|:-----|:-------:|:----|:---------:|:--------------|:----------|
| 0 | *Ortssignatur*  | 1 | Text | `str` | Pattern: `/#{0,1}[a-zA-Z0-9_]+/` | - |
| 1 | *Route* | 1 | Wort | `str` | Name oder Kürzel. Komplexer *string* in `"..."` | - | 
| 2 | *Nummer* | 1 | Nummer | `int\|str` | Zahl, alphabetische Zählung ab 2. Stelle | Routennummer |
| 3 | *Geburt* | 0 | Datum/Jahr | `int \| float\| datetime` | Format: `YYYY-MM-DD` | Fund- oder Benennungsdatum |
| 4 | *Entdecker* | 0 | Name | `str \| Letter` | Signatur, Handle, Name | optional | 
| 5 | *Laienadresse* | 0 | Text | `str` | `"..."` | Adresse nach Ortsüblichkeit geschrieben |
| 6 | *Grad:L* | 0 | geo. Grad | `int\|float` | - | Längengrad |
| 7 | *Grad:B* | 0 | geo. Grad | `int\|float` | - | Breitengrad |
