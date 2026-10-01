"""Genera la fuga: fuga_re_minore.musicxml (per MuseScore), fuga_re_minore.mid
e l'anteprima HTML fuga-in-re-minore-ars-algo.html (partitura, ascolto, forma).

Uso:  python componi.py
"""
from __future__ import annotations

from pathlib import Path

from fuga.anteprima import scrivi_anteprima
from fuga.forma import componi
from fuga.notazione import BATTUTA, durata_totale
from fuga.partitura import costruisci_partitura, esporta

CARTELLA = Path(__file__).resolve().parent
NOME = 'fuga_re_minore'
ANTEPRIMA = 'fuga-in-re-minore-ars-algo.html'


def main() -> None:
    fl1, fl2, sezioni = componi()
    print(f"Battute: {durata_totale(fl1) // BATTUTA}")
    for s in sezioni:
        print(f"  bb.{s.prima:>2}-{s.ultima:<2}  {s.nome:<24} {s.tonalita}")
    partitura = costruisci_partitura(fl1, fl2, sezioni)
    xml, mid = esporta(partitura, CARTELLA, NOME)
    html = scrivi_anteprima(CARTELLA, NOME, sezioni, ANTEPRIMA)
    print(f"Scritti: {xml.name}, {mid.name}, {html.name}")


if __name__ == '__main__':
    main()
