"""Trasformazioni contrappuntistiche: trasposizione diatonica, cambio di tonalità, inversione.

Tutte lavorano per *lettere* (gradi) e non per semitoni, così le alterazioni
caratteristiche (sesto abbassato, sensibile) vengono ricalcolate nella nuova tonalità.
"""
from __future__ import annotations

from dataclasses import dataclass

from .notazione import Altezza, Evento, LETTERE, SEMITONI_LETTERA, Voce

SCALE = {
    'maggiore': (0, 2, 4, 5, 7, 9, 11),
    'minore': (0, 2, 3, 5, 7, 8, 11),  # armonica: riferimento per sesto e settimo grado
    'naturale': (0, 2, 3, 5, 7, 8, 10),  # minore naturale: utile per le progressioni
}


@dataclass(frozen=True)
class Tonalita:
    tonica: str  # 'D', 'F', 'Bb'...
    modo: str  # 'minore' | 'maggiore'

    @property
    def lettera(self) -> int:
        return LETTERE.index(self.tonica[0])

    @property
    def pc(self) -> int:
        alt = self.tonica.count('#') - self.tonica.count('b')
        return (SEMITONI_LETTERA[self.lettera] + alt) % 12

    def nome_italiano(self) -> str:
        return nome_tonalita(self.tonica, self.modo)


NOMI_ITALIANI = {'C': 'Do', 'D': 'Re', 'E': 'Mi', 'F': 'Fa', 'G': 'Sol', 'A': 'La', 'B': 'Si'}


def nome_tonalita(tonica: str, modo: str) -> str:
    segno = {'#': '♯', 'b': '♭'}.get(tonica[1:2], '')
    return f"{NOMI_ITALIANI[tonica[0]]}{segno} {modo}"


RE_MINORE = Tonalita('D', 'minore')
FA_MAGGIORE = Tonalita('F', 'maggiore')
LA_MINORE = Tonalita('A', 'minore')
SOL_MINORE = Tonalita('G', 'minore')


def _centra(x: int) -> int:
    """Riporta una differenza di semitoni nell'intervallo [-6, 5]."""
    return (x + 6) % 12 - 6


def _grado_e_scarto(alt: Altezza, ton: Tonalita, scala: tuple[int, ...]) -> tuple[int, int]:
    grado = (alt.lettera - ton.lettera) % 7
    atteso = (ton.pc + scala[grado]) % 12
    return grado, _centra(alt.midi - atteso)


def _realizza(lettera_assoluta: int, ton: Tonalita, scala: tuple[int, ...], scarto: int) -> str:
    grado = (lettera_assoluta % 7 - ton.lettera) % 7
    pc = (ton.pc + scala[grado] + scarto) % 12
    naturale = Altezza(lettera_assoluta, 0)
    alt = _centra(pc - naturale.midi % 12)
    return Altezza.da_lettera_e_midi(lettera_assoluta, naturale.midi + alt).nome


def _mappa(voce: Voce, funzione) -> Voce:
    return [ev if ev.pausa else ev.con(altezza=funzione(Altezza.da_nome(ev.altezza))) for ev in voce]


def trasponi_diatonico(voce: Voce, passi: int, tonalita: Tonalita, scala: str = 'naturale') -> Voce:
    """Sposta ogni nota di `passi` gradi dentro la stessa tonalità (marce armoniche).

    Le note estranee alla scala mantengono la loro alterazione relativa.
    """
    sc = SCALE[scala]

    def f(alt: Altezza) -> str:
        _, scarto = _grado_e_scarto(alt, tonalita, sc)
        return _realizza(alt.lettera_assoluta + passi, tonalita, sc, scarto)

    return _mappa(voce, f)


def cambia_tonalita(voce: Voce, da: Tonalita, a: Tonalita, inizio: str | None = None,
                    *, ancora: tuple[str, str] | None = None) -> Voce:
    """Riscrive un tema da una tonalità a un'altra (anche cambiando modo).

    Il registro si fissa con `inizio` (la nota su cui deve cadere il primo suono)
    oppure con `ancora=(nota_originale, nota_nuova)`, ad esempio la tonica del modello.
    In minore il riferimento è la scala armonica, quindi sesto abbassato e
    sensibile restano tali; passando al maggiore diventano sesto e settimo grado naturali.
    """
    if ancora is None:
        prima = next(ev.altezza for ev in voce if not ev.pausa)
        ancora = (prima, inizio)
    passi = Altezza.da_nome(ancora[1]).lettera_assoluta - Altezza.da_nome(ancora[0]).lettera_assoluta
    if (da.lettera + passi) % 7 != a.lettera:
        raise ValueError(f"l'ancora {ancora} non porta da {da} a {a}")
    sc_da, sc_a = SCALE[da.modo], SCALE[a.modo]

    def f(alt: Altezza) -> str:
        _, scarto = _grado_e_scarto(alt, da, sc_da)
        return _realizza(alt.lettera_assoluta + passi, a, sc_a, scarto)

    risultato = _mappa(voce, f)
    if inizio is not None and next(ev.altezza for ev in risultato if not ev.pausa) != inizio:
        raise ValueError(f"il tema in {a} non comincia su {inizio}")
    return risultato


def inverti(voce: Voce, asse: str, tonalita: Tonalita) -> Voce:
    """Inversione diatonica intorno alla nota `asse` (specchio dei gradi).

    Con asse sul terzo grado di una tonalità minore: 1↔5, 2↔4, 3↔3, ♭6↔♯7.
    """
    sc = SCALE[tonalita.modo]
    centro = Altezza.da_nome(asse).lettera_assoluta

    def f(alt: Altezza) -> str:
        _, scarto = _grado_e_scarto(alt, tonalita, sc)
        return _realizza(2 * centro - alt.lettera_assoluta, tonalita, sc, -scarto)

    return _mappa(voce, f)


def ottava(voce: Voce, n: int) -> Voce:
    return _mappa(voce, lambda alt: Altezza(alt.lettera_assoluta + 7 * n, alt.alterazione).nome)


def con_prima_nota(voce: Voce, altezza: str | None) -> Voce:
    """Sostituisce il primo evento (tipicamente la pausa iniziale del controsoggetto)
    con una nota d'arrivo della cadenza precedente, o viceversa con una pausa."""
    return [voce[0].con(altezza=altezza)] + list(voce[1:])


def taglia(voce: Voce, durata: int) -> Voce:
    """Restituisce i primi `durata` sedicesimi della voce (l'ultima nota viene accorciata)."""
    out, t = [], 0
    for ev in voce:
        if t >= durata:
            break
        resto = durata - t
        out.append(ev if ev.durata <= resto else ev.con(durata=resto, legatura=False))
        t += ev.durata
    return out


def annota(voce: Voce, indice: int, **attributi) -> Voce:
    """Aggiunge dinamiche, legature o didascalie all'evento numero `indice`."""
    voce = list(voce)
    voce[indice] = voce[indice].con(**attributi)
    return voce


def arco(voce: Voce, da: int, a: int) -> Voce:
    """Legatura di frase dall'evento `da` all'evento `a` (inclusi)."""
    return annota(annota(voce, da, arco_inizio=True), a, arco_fine=True)


__all__ = [
    'Tonalita', 'RE_MINORE', 'FA_MAGGIORE', 'LA_MINORE', 'SOL_MINORE', 'SCALE',
    'trasponi_diatonico', 'cambia_tonalita', 'inverti', 'ottava', 'con_prima_nota',
    'taglia', 'annota', 'arco', 'nome_tonalita', 'Evento',
]
