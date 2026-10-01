"""Strumenti per gli episodi: marce armoniche (progressioni) e pedale."""
from __future__ import annotations

from .notazione import BATTUTA, Evento, Voce, durata_totale
from .trasformazioni import Tonalita, trasponi_diatonico


def marcia(modello_alto: Voce, modello_basso: Voce, ripetizioni: int, passo: int,
           tonalita: Tonalita, scala: str = 'naturale') -> tuple[Voce, Voce]:
    """Marcia armonica: il modello a due voci ripetuto, ogni volta spostato di `passo` gradi.

    `passo` negativo = progressione discendente. La trasposizione è diatonica
    nella `tonalita` data, come nelle progressioni barocche.
    """
    if durata_totale(modello_alto) != durata_totale(modello_basso):
        raise ValueError("le due voci del modello hanno durate diverse")
    alto, basso = [], []
    for i in range(ripetizioni):
        alto += trasponi_diatonico(modello_alto, passo * i, tonalita, scala)
        basso += trasponi_diatonico(modello_basso, passo * i, tonalita, scala)
    return alto, basso


def pedale(altezza: str, battute: int, riattacco: int = 2) -> Voce:
    """Nota tenuta per `battute` battute, riattaccata ogni `riattacco` battute
    con una pausa di croma prima di ogni ripresa, così il flautista respira."""
    voce: Voce = []
    restanti = battute
    while restanti > 0:
        blocco = min(riattacco, restanti)
        durata = blocco * BATTUTA
        ultimo = restanti == blocco
        if not ultimo:
            durata -= 2
        # note legate battuta per battuta (la notazione resta leggibile)
        while durata > 0:
            parte = min(durata, BATTUTA)
            voce.append(Evento(altezza, parte, legatura=durata > parte))
            durata -= parte
        if not ultimo:
            voce.append(Evento(None, 2))
        restanti -= blocco
    return voce
