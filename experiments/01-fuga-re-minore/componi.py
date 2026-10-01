"""Genera la fuga: fuga_re_minore.musicxml (per MuseScore) e fuga_re_minore.mid.

Uso:  python componi.py
"""
from __future__ import annotations

from pathlib import Path

from fuga.forma import componi
from fuga.notazione import BATTUTA, durata_totale
from fuga.partitura import costruisci_partitura, esporta

CARTELLA = Path(__file__).resolve().parent
NOME = 'fuga_re_minore'


def main() -> None:
    fl1, fl2, sezioni = componi()
    print(f"Battute: {durata_totale(fl1) // BATTUTA}")
    for s in sezioni:
        print(f"  bb.{s.prima:>2}–{s.ultima:<2}  {s.nome:<24} {s.tonalita}")
    partitura = costruisci_partitura(fl1, fl2, sezioni)
    xml, mid = esporta(partitura, CARTELLA, NOME)
    print(f"Scritti: {xml.name}, {mid.name}")


if __name__ == '__main__':
    main()
