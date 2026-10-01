"""Notazione testuale minima e rappresentazione interna delle voci.

Una voce è una lista di `Evento`; le durate sono in sedicesimi (1 = semicroma),
quindi una battuta di 4/4 vale 16.

Sintassi dei token (separati da spazi):

    D5:q        nota (C4 = Do centrale; diesis '#', bemolle 'b')
    r:e         pausa
    w h q e s   semibreve, minima, semiminima, croma, semicroma; '.' = punto
    ~           legatura di valore verso la nota seguente   (es. D6:e~)
    ( )         inizio / fine di una legatura di frase      (es. E5:s(  F5:s) )
    *           trillo                                      (es. E5:q*)
    !           corona                                      (es. D4:w!)
    @mf         dinamica applicata alla nota seguente (pp p mp mf f ff)
    @<  @>      inizio forcella di crescendo / diminuendo, @= chiude la forcella
    "Testo"     didascalia (senza spazi, '_' = spazio) applicata alla nota seguente
    |           stanghetta: serve solo a controllare che le battute siano complete
"""
from __future__ import annotations

import re
from dataclasses import dataclass, replace

LETTERE = 'CDEFGAB'
SEMITONI_LETTERA = [0, 2, 4, 5, 7, 9, 11]
DURATE = {'w': 16, 'h': 8, 'q': 4, 'e': 2, 's': 1}
BATTUTA = 16  # sedicesimi in una battuta di 4/4

_RE_ALTEZZA = re.compile(r'([A-G])(#{1,2}|b{1,2})?(-?\d)$')
_RE_EVENTO = re.compile(r'(r|[A-G](?:#{1,2}|b{1,2})?-?\d):([whqes])(\.?)([~()*!]*)$')


@dataclass(frozen=True)
class Altezza:
    """Altezza scomposta: indice di lettera assoluto (ottava*7 + lettera) e alterazione."""
    lettera_assoluta: int
    alterazione: int  # -2..+2

    @property
    def lettera(self) -> int:
        return self.lettera_assoluta % 7

    @property
    def ottava(self) -> int:
        return self.lettera_assoluta // 7

    @property
    def midi(self) -> int:
        return 12 * (self.ottava + 1) + SEMITONI_LETTERA[self.lettera] + self.alterazione

    @property
    def nome(self) -> str:
        segno = '#' * self.alterazione if self.alterazione > 0 else 'b' * -self.alterazione
        return f"{LETTERE[self.lettera]}{segno}{self.ottava}"

    @classmethod
    def da_nome(cls, nome: str) -> 'Altezza':
        m = _RE_ALTEZZA.match(nome)
        if not m:
            raise ValueError(f"altezza non valida: {nome!r}")
        segno = m.group(2) or ''
        alt = len(segno) if segno.startswith('#') else -len(segno)
        return cls(int(m.group(3)) * 7 + LETTERE.index(m.group(1)), alt)

    @classmethod
    def da_lettera_e_midi(cls, lettera_assoluta: int, midi: int) -> 'Altezza':
        """Costruisce l'altezza con la lettera data e l'alterazione che produce `midi`."""
        base = cls(lettera_assoluta, 0).midi
        alt = midi - base
        if not -2 <= alt <= 2:
            raise ValueError(f"alterazione impossibile: lettera {lettera_assoluta}, midi {midi}")
        return cls(lettera_assoluta, alt)


@dataclass(frozen=True)
class Evento:
    altezza: str | None  # None = pausa
    durata: int  # in sedicesimi
    legatura: bool = False  # legatura di valore verso l'evento seguente
    arco_inizio: bool = False  # legatura di frase
    arco_fine: bool = False
    trillo: bool = False
    corona: bool = False
    dinamica: str | None = None
    forcella: str | None = None  # '<' '>' oppure '=' (fine)
    testo: str | None = None

    @property
    def pausa(self) -> bool:
        return self.altezza is None

    @property
    def midi(self) -> int | None:
        return None if self.altezza is None else Altezza.da_nome(self.altezza).midi

    def con(self, **modifiche) -> 'Evento':
        return replace(self, **modifiche)


Voce = list[Evento]


def leggi(testo: str, controlla_battute: bool = True) -> Voce:
    """Converte la notazione testuale in una lista di eventi."""
    eventi: Voce = []
    in_sospeso: dict = {}
    accumulato = 0
    for tok in testo.split():
        if tok == '|':
            if controlla_battute and accumulato % BATTUTA:
                raise ValueError(f"battuta incompleta ({accumulato % BATTUTA}/16) prima di '|' in: {testo[:60]}…")
            continue
        if tok.startswith('@'):
            valore = tok[1:]
            if valore in ('<', '>', '='):
                in_sospeso['forcella'] = valore
            else:
                in_sospeso['dinamica'] = valore
            continue
        if tok.startswith('"'):
            in_sospeso['testo'] = tok.strip('"').replace('_', ' ')
            continue
        m = _RE_EVENTO.match(tok)
        if not m:
            raise ValueError(f"token non valido: {tok!r}")
        alt, dur, punto, segni = m.groups()
        durata = DURATE[dur] * 3 // 2 if punto else DURATE[dur]
        ev = Evento(
            altezza=None if alt == 'r' else Altezza.da_nome(alt).nome,
            durata=durata,
            legatura='~' in segni,
            arco_inizio='(' in segni,
            arco_fine=')' in segni,
            trillo='*' in segni,
            corona='!' in segni,
            **in_sospeso,
        )
        in_sospeso = {}
        eventi.append(ev)
        accumulato += durata
    return eventi


def scrivi(voce: Voce) -> str:
    """Operazione inversa di `leggi` (senza ornamenti): utile per stampare i materiali."""
    inv = {v: k for k, v in DURATE.items()}
    out, acc = [], 0
    for ev in voce:
        d = inv.get(ev.durata) or (inv[ev.durata * 2 // 3] + '.')
        out.append(f"{ev.altezza or 'r'}:{d}{'~' if ev.legatura else ''}")
        acc += ev.durata
        if acc % BATTUTA == 0:
            out.append('|')
    return ' '.join(out)


def durata_totale(voce: Voce) -> int:
    return sum(ev.durata for ev in voce)
