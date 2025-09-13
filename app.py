"""En enkel GUI-applikasjon for å skanne en hovedbok.

GUI-et er bygget med PyQt5. Programmet forsøker å lese en Excel-fil ved hjelp
av pandas dersom biblioteket er tilgjengelig. Resultatet fra skanningen
presenteres som antall funn i et tekstfelt.
"""

from __future__ import annotations

import sys
from typing import List

from PyQt5 import QtWidgets  # type: ignore

try:  # pragma: no cover - valgfri avhengighet
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

from scanner import scan_all


class MainWindow(QtWidgets.QWidget):
    """Hovedvindu for programmet."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Hovedbokscanner")
        layout = QtWidgets.QVBoxLayout()

        self.button = QtWidgets.QPushButton("Åpne hovedbok")
        self.button.clicked.connect(self.open_file)
        layout.addWidget(self.button)

        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def open_file(self) -> None:
        """Åpne filvelger og analyser valgt fil."""
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Velg Excel-fil", "", "Excel filer (*.xlsx *.xlsm)"
        )
        if not path:
            return
        if pd is None:
            self.text.setPlainText("pandas er ikke installert.")
            return
        try:
            df = pd.read_excel(path)
        except Exception as exc:  # pragma: no cover - GUI feilhåndtering
            self.text.setPlainText(f"Kunne ikke lese filen: {exc}")
            return
        rows: List[dict] = df.to_dict(orient="records")
        results = scan_all(rows)
        lines = [f"{navn}: {len(funn)} funn" for navn, funn in results.items()]
        self.text.setPlainText("\n".join(lines))


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover - CLI inngang
    main()
