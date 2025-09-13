# Hovedbokscanner

Et enkelt verktøy som analyserer en hovedbok i Excel-format og peker på
forhold som kan være interessante for en revisor.

## Installasjon

```bash
pip install -r requirements.txt
```

## Bruk

Kjør GUI-appen:

```bash
python app.py
```

Programmet bruker `pandas` til å lese Excel-filen. Resultatet viser antall
funn for hver kontroll, som manglende beskrivelser, store beløp og poster i
helger.

## Tester

```bash
pytest
```
