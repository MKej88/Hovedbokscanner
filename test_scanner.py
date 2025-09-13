import pytest

from scanner import (
    scan_all,
    scan_duplicate_voucher,
    scan_large_amounts,
    scan_missing_description,
    scan_weekend_entries,
)


def example_rows():
    return [
        {
            "Dato": "2024-01-01",
            "Beløp": 50_000,
            "Beskrivelse": "",
            "Bilagsnummer": 1,
        },
        {
            "Dato": "2024-01-06",
            "Beløp": 200_000,
            "Beskrivelse": "Kjøp",
            "Bilagsnummer": 2,
        },
        {
            "Dato": "2024-01-07",
            "Beløp": -150_000,
            "Beskrivelse": None,
            "Bilagsnummer": 2,
        },
        {
            "Dato": "2024-01-02",
            "Beløp": 1_000,
            "Beskrivelse": "Salg",
            "Bilagsnummer": 3,
        },
    ]


def test_scan_missing_description():
    rows = example_rows()
    result = scan_missing_description(rows)
    assert len(result) == 2


def test_scan_large_amounts():
    rows = example_rows()
    result = scan_large_amounts(rows, threshold=100_000)
    assert len(result) == 2


def test_scan_weekend_entries():
    rows = example_rows()
    result = scan_weekend_entries(rows)
    assert len(result) == 2


def test_scan_duplicate_voucher():
    rows = example_rows()
    result = scan_duplicate_voucher(rows)
    assert len(result) == 2


def test_scan_all_combines_results():
    rows = example_rows()
    result = scan_all(rows, threshold=100_000)
    assert {key: len(val) for key, val in result.items()} == {
        "Manglende beskrivelse": 2,
        "Store beløp": 2,
        "Helgeposter": 2,
        "Dupliserte bilagsnummer": 2,
    }
