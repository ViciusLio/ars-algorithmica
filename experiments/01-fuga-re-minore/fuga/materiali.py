"""Materiali tematici della fuga: soggetto, risposta, controsoggetto, inverso e motivi.

I temi sono scritti una volta sola nella loro forma di riferimento; tutte le
entrate si ottengono con le funzioni di `trasformazioni`.
"""
from __future__ import annotations

from .notazione import Altezza, Voce, leggi
from .trasformazioni import (LA_MINORE, RE_MINORE, Tonalita, cambia_tonalita, inverti,
                             trasponi_diatonico)

# Soggetto in Re minore, 3 battute (vedi PIANO.md §2).
SOGGETTO_TESTO = """
    D5:q A5:q F5:e E5:e D5:q |
    C#5:e E5:e G5:e Bb5:e A5:q G5:e F5:e |
    E5:s( D5:s E5:s F5:s) G5:e E5:e F5:e D5:e E5:q |
"""

# Controsoggetto scritto contro la risposta (esposizione, La minore, sopra).
CS_RISPOSTA_TESTO = """
    F5:e A5:s( G5:s F5:s E5:s F5:s G5:s) A5:q C6:s( B5:s A5:s C6:s) |
    B5:q. D6:e~ D6:e C6:e B5:e A5:e |
    G#5:h A5:e C6:e B5:e A5:s( G#5:s) |
"""

# Testa del controsoggetto quando accompagna il soggetto: pausa (respiro) e volta 3-2-3-♯7.
# Scritta in La minore come il corpo, a cui si aggancia dal terzo quarto.
CS_TESTA_SOGGETTO_TESTO = "r:q C6:s( B5:s C6:s G#5:s)"

LUNGHEZZA_TEMA = 48  # 3 battute in sedicesimi


def soggetto(tonalita: Tonalita = RE_MINORE, inizio: str = 'D5') -> Voce:
    """Il soggetto nella tonalità e nel registro richiesti (forma reale)."""
    s = leggi(SOGGETTO_TESTO)
    return s if (tonalita, inizio) == (RE_MINORE, 'D5') else cambia_tonalita(s, RE_MINORE, tonalita, inizio)


def risposta(inizio: str = 'A4') -> Voce:
    """Risposta tonale: trasposizione alla dominante con mutazione della testa.

    Nella testa (prima della sensibile) ogni nota che nel soggetto è dominante
    viene risposta con la tonica: Re-La diventa La-Re invece di La-Mi.
    """
    s = soggetto()
    reale = soggetto(LA_MINORE, inizio)
    out = []
    in_testa = True
    for ev_s, ev_r in zip(s, reale):
        if ev_s.pausa:
            out.append(ev_r)
            continue
        alt = Altezza.da_nome(ev_s.altezza)
        if (alt.lettera - RE_MINORE.lettera) % 7 == 6:  # sensibile: fine della testa
            in_testa = False
        if in_testa and (alt.lettera - RE_MINORE.lettera) % 7 == 4:  # dominante
            ev_r = trasponi_diatonico([ev_r], -1, LA_MINORE, 'minore')[0]
        out.append(ev_r)
    return out


def inverso(tonalita: Tonalita = RE_MINORE, inizio: str = 'A5') -> Voce:
    """Inversione diatonica del soggetto con asse sul terzo grado (1↔5, ♭6↔♯7)."""
    inv = inverti(soggetto(), asse='F5', tonalita=RE_MINORE)
    return inv if (tonalita, inizio) == (RE_MINORE, 'A5') else cambia_tonalita(inv, RE_MINORE, tonalita, inizio)


def controsoggetto(tonalita: Tonalita, tonica: str, contro: str = 'soggetto') -> Voce:
    """Controsoggetto nella tonalità data.

    `tonica` è la nota del corpo che cade sul terzo quarto della prima battuta
    (La5 nella forma originale): fissa il registro, sopra o sotto il tema.
    `contro` = 'soggetto' usa la testa con pausa, 'risposta' quella dell'esposizione.
    """
    corpo = leggi(CS_RISPOSTA_TESTO)
    if contro == 'soggetto':
        cs = leggi(CS_TESTA_SOGGETTO_TESTO, controlla_battute=False) + corpo[7:]
    elif contro == 'risposta':
        cs = corpo
    else:
        raise ValueError(contro)
    return cambia_tonalita(cs, LA_MINORE, tonalita, ancora=('A5', tonica))


# --- motivi per gli episodi -------------------------------------------------

def testa(tonalita: Tonalita = RE_MINORE, inizio: str = 'D5') -> Voce:
    """Motivo a+b: salto di quinta e discesa per grado (prima battuta del soggetto)."""
    return soggetto(tonalita, inizio)[:5]


def coda(tonalita: Tonalita = RE_MINORE, inizio: str = 'D5') -> Voce:
    """Motivo d: volta di semicrome e terze discendenti (terza battuta)."""
    return soggetto(tonalita, inizio)[12:]
