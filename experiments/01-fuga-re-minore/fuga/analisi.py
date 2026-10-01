"""Controlli di condotta delle voci per due voci (Python puro).

Lavora su liste di `Suono` (note già unite attraverso le legature di valore),
che si possono ottenere sia dalle strutture interne (`suoni`) sia da un file
MusicXML letto con music21 (vedi verifica.py). Tempi in sedicesimi.
"""
from __future__ import annotations

from dataclasses import dataclass

from .notazione import BATTUTA, Altezza, Voce
from .trasformazioni import nome_tonalita

QUALITA = {0: 'P8', 1: 'm2', 2: 'M2', 3: 'm3', 4: 'M3', 5: 'P4', 6: 'TT',
           7: 'P5', 8: 'm6', 9: 'M6', 10: 'm7', 11: 'M7'}
CONSONANZE = {0, 3, 4, 7, 8, 9}
PERFETTE = {0: 'ottave', 7: 'quinte'}


@dataclass(frozen=True)
class Suono:
    inizio: int
    durata: int
    midi: int
    nome: str  # nome con lettera, es. 'C#5' (serve per gli intervalli diatonici)

    @property
    def fine(self) -> int:
        return self.inizio + self.durata

    @property
    def lettera_assoluta(self) -> int:
        return Altezza.da_nome(self.nome).lettera_assoluta


def suoni(voce: Voce) -> list[Suono]:
    """Converte una voce in suoni, unendo le note legate."""
    out: list[Suono] = []
    t, legata = 0, False
    for ev in voce:
        if not ev.pausa:
            if legata and out and out[-1].midi == ev.midi:
                ultimo = out.pop()
                out.append(Suono(ultimo.inizio, ultimo.durata + ev.durata, ultimo.midi, ultimo.nome))
            else:
                out.append(Suono(t, ev.durata, ev.midi, ev.altezza))
        legata = ev.legatura and not ev.pausa
        t += ev.durata
    return out


def dove(t: int) -> str:
    """Posizione leggibile: battuta e quarto (es. 'b.12 q3' o 'b.12 q3½')."""
    quarto, resto = divmod(t % BATTUTA, 4)
    frazione = {0: '', 1: '¼', 2: '½', 3: '¾'}[resto]
    return f"b.{t // BATTUTA + 1} q{quarto + 1}{frazione}"


def _sonante(lista: list[Suono], t: int) -> Suono | None:
    for s in lista:
        if s.inizio <= t < s.fine:
            return s
        if s.inizio > t:
            break
    return None


def sonorita(alta: list[Suono], bassa: list[Suono]) -> list[tuple[int, Suono | None, Suono | None]]:
    """Tutti gli istanti in cui almeno una voce attacca, con ciò che suona in ciascuna."""
    tempi = sorted({s.inizio for s in alta} | {s.inizio for s in bassa})
    return [(t, _sonante(alta, t), _sonante(bassa, t)) for t in tempi]


def intervallo(a: Suono, b: Suono) -> int:
    return abs(a.midi - b.midi) % 12


# --- controlli ----------------------------------------------------------------

def fuori_estensione(lista: list[Suono], minimo: str, massimo: str) -> list[Suono]:
    lo, hi = Altezza.da_nome(minimo).midi, Altezza.da_nome(massimo).midi
    return [s for s in lista if not lo <= s.midi <= hi]


def paralleli(alta: list[Suono], bassa: list[Suono]) -> list[str]:
    """Quinte e ottave consecutive fra due attacchi successivi in cui entrambe le voci si muovono."""
    out = []
    son = sonorita(alta, bassa)
    for (t0, a0, b0), (t1, a1, b1) in zip(son, son[1:]):
        if None in (a0, b0, a1, b1) or a0 is a1 or b0 is b1:
            continue
        if a0.midi == a1.midi or b0.midi == b1.midi:
            continue
        i0, i1 = intervallo(a0, b0), intervallo(a1, b1)
        if i0 == i1 and i0 in PERFETTE:
            moto = 'retto' if (a1.midi - a0.midi) * (b1.midi - b0.midi) > 0 else 'contrario'
            out.append(f"{dove(t0)} → {dove(t1)}: {PERFETTE[i0]} parallele per moto {moto} "
                       f"({a0.nome}/{b0.nome} → {a1.nome}/{b1.nome})")
    return out


def dirette(alta: list[Suono], bassa: list[Suono]) -> list[str]:
    """Quinte/ottave per moto retto (nascoste): arrivo su intervallo giusto con
    entrambe le voci nella stessa direzione e la voce superiore che salta."""
    out = []
    son = sonorita(alta, bassa)
    for (t0, a0, b0), (t1, a1, b1) in zip(son, son[1:]):
        if None in (a0, b0, a1, b1) or a0 is a1 or b0 is b1:
            continue
        da, db = a1.midi - a0.midi, b1.midi - b0.midi
        i1 = intervallo(a1, b1)
        if i1 in PERFETTE and da * db > 0 and intervallo(a0, b0) != i1:
            sup_da = da if a1.midi >= b1.midi else db
            if abs(sup_da) > 2:
                out.append(f"{dove(t1)}: {PERFETTE[i1][:-1]}a per moto retto ({a0.nome}/{b0.nome} → {a1.nome}/{b1.nome})")
    return out


def incroci(alta: list[Suono], bassa: list[Suono]) -> list[tuple[int, int]]:
    """Intervalli di tempo (inizio, fine) in cui la voce bassa sta sopra la voce alta."""
    spans, aperto = [], None
    son = sonorita(alta, bassa)
    for t, a, b in son:
        sopra = a is not None and b is not None and b.midi > a.midi
        if sopra and aperto is None:
            aperto = t
        if not sopra and aperto is not None:
            spans.append((aperto, t))
            aperto = None
    if aperto is not None:
        spans.append((aperto, son[-1][0] + 1))
    return spans


def distanze_eccessive(alta: list[Suono], bassa: list[Suono], massimo: int = 16) -> list[str]:
    """Attacchi in cui le voci distano più di `massimo` semitoni (16 = decima maggiore)."""
    return [f"{dove(t)}: {a.nome}/{b.nome} ({abs(a.midi - b.midi)} semitoni)"
            for t, a, b in sonorita(alta, bassa)
            if a and b and abs(a.midi - b.midi) > massimo]


def respiri(voce: Voce, nota_lunga: int = 8, pausa_minima: int = 2) -> list[tuple[int, int]]:
    """Tratti senza respiro: restituisce (inizio, fine) dei segmenti fra due punti di respiro.

    Punto di respiro = pausa di almeno una croma oppure nota di almeno una minima
    (anche ottenuta con legature)."""
    punti = []  # istanti in cui si può respirare
    t = 0
    for s_inizio, s_fine, pausa in _blocchi(voce):
        if (pausa and s_fine - s_inizio >= pausa_minima) or (not pausa and s_fine - s_inizio >= nota_lunga):
            punti.append((s_inizio, s_fine))
        t = s_fine
    segmenti, precedente = [], 0
    for ini, fin in punti:
        segmenti.append((precedente, ini))
        precedente = fin
    segmenti.append((precedente, t))
    return segmenti


def _blocchi(voce: Voce):
    """Pause consecutive unite e note legate unite: (inizio, fine, è_pausa)."""
    t = 0
    corrente = None
    for ev in voce:
        if corrente and corrente[2] == ev.pausa and (ev.pausa or corrente[3]):
            corrente = (corrente[0], t + ev.durata, ev.pausa, ev.legatura)
        else:
            if corrente:
                yield corrente[:3]
            corrente = (t, t + ev.durata, ev.pausa, ev.legatura)
        t += ev.durata
    if corrente:
        yield corrente[:3]


PEDALE = BATTUTA * 3 // 2  # una nota grave tenuta così a lungo è un pedale


def dissonanze(alta: list[Suono], bassa: list[Suono]) -> list[str]:
    """Dissonanze sui quarti che non sono note di passaggio, di volta o ritardi.

    Sopra un pedale le dissonanze sono libere; il tritono è accettato come
    intervallo dell'armonia di dominante se una delle due note vi arriva o ne
    parte per grado congiunto."""
    out = []
    for t, a, b in sonorita(alta, bassa):
        if t % 4 or a is None or b is None:
            continue
        iv = intervallo(a, b)
        if iv in CONSONANZE or b.durata >= PEDALE:
            continue
        spiegata = False
        for voce, nota in ((alta, a), (bassa, b)):
            prima, dopo = _vicini(voce, nota)
            if nota.inizio < t:  # nota tenuta: ritardo se risolve scendendo di grado
                if dopo and 0 < nota.midi - dopo.midi <= 2:
                    spiegata = True
            elif prima and dopo and prima.fine == nota.inizio and dopo.inizio == nota.fine:
                passo_in, passo_out = nota.midi - prima.midi, dopo.midi - nota.midi
                if 0 < abs(passo_in) <= 2 and 0 < abs(passo_out) <= 2:
                    spiegata = True  # passaggio o volta
            if iv == 6 and ((prima and 0 < abs(nota.midi - prima.midi) <= 2)
                            or (dopo and 0 < abs(dopo.midi - nota.midi) <= 2)):
                spiegata = True
        if not spiegata:
            out.append(f"{dove(t)}: {QUALITA[iv]} {a.nome}/{b.nome}")
    return out


def _vicini(voce: list[Suono], nota: Suono) -> tuple[Suono | None, Suono | None]:
    i = voce.index(nota)
    return (voce[i - 1] if i > 0 else None, voce[i + 1] if i + 1 < len(voce) else None)


# --- riconoscimento delle entrate -------------------------------------------

@dataclass(frozen=True)
class Modello:
    nome: str
    durate: tuple[int, ...]
    passi: tuple[int, ...]  # intervalli diatonici fra note consecutive (in lettere)
    indice_tonica: int  # quale nota del tema è la tonica della sua tonalità
    indice_terza: int  # quale nota ne dà il modo (terza sopra la tonica)


def modello(nome: str, voce: Voce, indice_tonica: int = 0, indice_terza: int = 2) -> Modello:
    ss = suoni(voce)
    return Modello(nome, tuple(s.durata for s in ss),
                   tuple(b.lettera_assoluta - a.lettera_assoluta for a, b in zip(ss, ss[1:])),
                   indice_tonica, indice_terza)


def entrate(lista: list[Suono], modelli: list[Modello], minimo_note: int = 10) -> list[dict]:
    """Cerca il tema (testa + arpeggio, almeno `minimo_note` note) nelle sue forme.

    Il confronto usa il ritmo e gli intervalli diatonici, quindi riconosce il tema
    in qualunque tonalità e modo. Riporta anche se l'entrata è completa."""
    trovate = []
    for i in range(len(lista)):
        for m in modelli:
            n = _note_coincidenti(lista, i, m)
            if n >= minimo_note:
                ton = lista[i + m.indice_tonica]
                terza = lista[i + m.indice_terza]
                modo = 'minore' if (terza.midi - ton.midi) % 12 == 3 else 'maggiore'
                tonica = ton.nome.rstrip('-0123456789')
                trovate.append({
                    'inizio': lista[i].inizio, 'forma': m.nome,
                    'tonalita': nome_tonalita(tonica, modo),
                    'completa': n == len(m.durate), 'note': n, 'totale': len(m.durate),
                    'prima_nota': lista[i].nome,
                })
    return trovate


def _note_coincidenti(lista: list[Suono], i: int, m: Modello) -> int:
    n = 0
    for k in range(len(m.durate)):
        j = i + k
        if j >= len(lista):
            break
        if k > 0:
            prec = lista[j - 1]
            if prec.fine != lista[j].inizio:
                break
            if lista[j].lettera_assoluta - prec.lettera_assoluta != m.passi[k - 1]:
                break
            if prec.durata != m.durate[k - 1]:
                break
        n += 1
    # l'ultima nota contata può durare di più (nota d'arrivo legata): si accetta
    return n


# --- tabella per lo sviluppo ---------------------------------------------------

def tabella(alta: list[Suono], bassa: list[Suono], da_battuta: int, a_battuta: int) -> str:
    righe = []
    for t, a, b in sonorita(alta, bassa):
        if not (da_battuta - 1) * BATTUTA <= t < a_battuta * BATTUTA:
            continue
        iv = '' if a is None or b is None else QUALITA[intervallo(a, b)]
        segno = '' if not iv or intervallo(a, b) in CONSONANZE else ' *'
        forte = '' if t % 4 else '·'
        righe.append(f"{dove(t):10s}{forte:1s} {a.nome if a else '-':5s} {b.nome if b else '-':5s} {iv}{segno}"
                     f"{'  INCROCIO' if a and b and b.midi > a.midi else ''}")
    return '\n'.join(righe)
