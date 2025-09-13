"""Funksjoner for å analysere en hovedbok.

Dette modul inneholder grunnleggende søk som typisk kan være nyttige for
en revisor. Hovedboken forventes representert som en liste med ordbøker
med minst følgende nøkler:

* ``Dato`` – ISO-formatert dato ``YYYY-MM-DD``.
* ``Beløp`` – numerisk beløp.
* ``Beskrivelse`` – tekstlig forklaring.
* ``Bilagsnummer`` – identifikator for bilaget.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

Entry = Dict[str, Any]
Ledger = List[Entry]


def scan_missing_description(rows: Ledger) -> Ledger:
    """Returner alle rader uten beskrivelse."""
    result: Ledger = []
    for r in rows:
        value = r.get("Beskrivelse")
        if value is None or not str(value).strip():
            result.append(r)
    return result


def scan_large_amounts(rows: Ledger, threshold: float = 100_000) -> Ledger:
    """Returner rader der absoluttbeløpet er større enn eller lik terskelen."""
    result: Ledger = []
    for r in rows:
        try:
            amount = float(r.get("Beløp", 0))
        except (TypeError, ValueError):
            continue
        if abs(amount) >= threshold:
            result.append(r)
    return result


def scan_weekend_entries(rows: Ledger) -> Ledger:
    """Finn rader som er bokført i helger."""
    result: Ledger = []
    for r in rows:
        date_value = r.get("Dato")
        if not date_value:
            continue
        try:
            dt = datetime.fromisoformat(str(date_value))
        except ValueError:
            continue
        if dt.weekday() >= 5:  # 5=lørdag, 6=søndag
            result.append(r)
    return result


def scan_duplicate_voucher(rows: Ledger) -> Ledger:
    """Identifiser dupliserte bilagsnummer."""
    seen: Dict[Any, Entry] = {}
    duplicates: Ledger = []
    for r in rows:
        key = r.get("Bilagsnummer")
        if key in seen:
            duplicates.append(r)
            first = seen[key]
            if first is not None:
                duplicates.append(first)
                seen[key] = None  # marker at første allerede lagt til
        else:
            seen[key] = r
    return duplicates


def scan_all(rows: Ledger, threshold: float = 100_000) -> Dict[str, Ledger]:
    """Kjør alle kontroller og returner et resultatsett."""
    return {
        "Manglende beskrivelse": scan_missing_description(rows),
        "Store beløp": scan_large_amounts(rows, threshold),
        "Helgeposter": scan_weekend_entries(rows),
        "Dupliserte bilagsnummer": scan_duplicate_voucher(rows),
    }
