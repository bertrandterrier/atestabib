ALFRED TESTA BIBLIOTHEK
=======================

> `#atestabib`
> Bibliothek mit *fuzzy contingency*

- [Entwicklung](#entwicklung)
    - [TestaPP](#testapp)
    - [Verzeichnisse](#verzeichnisse)
- [Kontakt](#kontakt)
- [Lizenz](#lizenz)

# Entwicklung
## TestaPP
Eine App für die *Alfred Testa Bibliothek* ist unter dem Namen *TestaPP* in Entwicklung.

## Beitragende Repositories
- [atestabib](https://github.com/bertrandterrier/atestabib)

## Nutzungsinformationen
### Signaturen
Eine schematische Erläuterung der Signaturenschlüsselsyntax können sie dem Dokument `atestabib/docs/signatur.ebnf` entnehmen. Das Schema folgt den Regeln der [erweiterten Backur-Naur-Form](https://de.wikipedia.org/wiki/Erweiterte_Backus-Naur-Form).

## Verzeichnisse
Alle notwendigen Verzeichnisse finden Sie im Ordner `atestabib/docs/`. Wirkliche Verzeichnisse sind durchgängig großgeschrieben. Bei anderen Dateien handelt es sich um Informationsdokumente.

### `NUTZER.CSV`
Nutzerverzeichnis.

Das hinterlegen von Namen oder persönlichen Daten ist **nicht** nötig. Eine besetzte Signatur benötigt alleinig den *Nutzerstatus* als `user`/`admin`. Ein leeres Nutzerfeld ist funktionsgleich mit dem Nutzerfeldeintrag `ANON`.

> **WICHTIG!**
> Signaturvergaben müssen durch die Administration akkreditiert werden.

Das Feld *Route* ist optional. Es sollte der vollständige Name der Route eingetragen werden. Wenn Sonder- oder Leerzeichen verwendet werden, sollte der Eintrag durch `"..."` umschlossen sein. Mehrfachrouten werden durch `;` getrennt innerhalb der Umschließung getrennt.

## `ROUTEN.LOG`
Routenverzeichnis.

Die Syntaxregeln sind:

1. Pro Zeile `1` Eintrag. Zeilenende kann zur Sicherheit durch `;` markiert werden.
2. Pro Eintrag min. `2`, max. `3` Spalten. Spalten sind durch `{...}` umschlossen.
3. Inhalt der Spalten ist: `{KÜRZEL}{VOLLNAME}{NUTZERSIGNATUR}`. Die Nutzersignatur ist optional.
4. Es wird empfohlen den *Vollnamen* durch `"..."` zu umschließen, um automatisierte Weiterverarbeitung zu erlauben. Dies erlaubt Mehrfacheinträge:

```ROUTEN.LOG
{#eab}{"Eintrag als Beispiel" "Beispieleintrag"}{ANON};
```

5. Die 3. Spalte (Index `2`) kann ausgelassen werden oder (funktionsgleich) leer bleiben oder mit `ANON` ausgefüllt.



# Kontakt
Bei Fragen und für Akkreditierungsanträge wenden Sie sich bitte an die [Administration](https://atestabib.blogspot.com)


# Lizenz
Die *Alfred Testa Bibliothek* ist ein *open source* Projekt.

Desweiteren s. [LICENSE](https://github.com/bertrandterrier/atestabib/LICENSE)
