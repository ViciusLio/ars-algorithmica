"""La forma della fuga: ogni sezione restituisce le due voci per le sue battute.

Le entrate tematiche sono generate dai materiali; episodi, codette e coda sono
scritti a mano nella notazione di `notazione.py`.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import materiali as mat
from .episodi import marcia, pedale
from .notazione import BATTUTA, Voce, durata_totale, leggi
from .trasformazioni import (FA_MAGGIORE, LA_MINORE, RE_MINORE, SOL_MINORE, annota,
                             con_prima_nota)


@dataclass(frozen=True)
class Sezione:
    nome: str
    prima: int
    ultima: int
    tonalita: str
    descrizione: str


def _pausa(battute: int) -> Voce:
    return leggi(' '.join(['r:w |'] * battute))


def _controlla(nome: str, fl1: Voce, fl2: Voce, battute: int) -> None:
    for i, v in ((1, fl1), (2, fl2)):
        if durata_totale(v) != battute * BATTUTA:
            raise ValueError(f"{nome}: il flauto {i} dura {durata_totale(v) / BATTUTA} battute, attese {battute}")


# --- sezioni ---------------------------------------------------------------------

def esposizione() -> tuple[Voce, Voce]:
    """bb.1–6: soggetto al Flauto 1, risposta tonale al Flauto 2 con controsoggetto sopra."""
    fl1 = annota(mat.soggetto(), 0, dinamica='mf')
    fl1 += mat.controsoggetto(LA_MINORE, 'A5', contro='risposta')
    fl2 = _pausa(3) + annota(mat.risposta(), 0, dinamica='mf')
    return fl1, fl2


def codetta() -> tuple[Voce, Voce]:
    """bb.7–8: dalla dominante torna a Re minore sul motivo della coda del soggetto."""
    fl1 = leggi("""
        A5:e r:e E5:s( D5:s E5:s F5:s) G5:e E5:e F5:e A5:e |
        G5:s( F5:s E5:s D5:s) E5:q~ E5:e D5:e C#5:q |""")
    fl2 = leggi("""
        C5:q C#5:h D5:q |
        Bb4:q( A4:e G4:e) A4:h |""")
    return fl1, fl2


def episodio_1() -> tuple[Voce, Voce]:
    """bb.9–14: marcia per quinte discendenti (Re m – Sol m – Do – Fa) sulla testa
    del soggetto, modello di due battute con scambio delle parti; cadenza in Fa."""
    modello_alto = leggi("""
        D5:q A5:q G5:e F5:e G5:e A5:e |
        Bb5:e A5:e Bb5:e F5:e E5:h |""")
    modello_basso = leggi("""
        F4:e E4:e F4:e A4:e Bb4:h |
        G4:q D5:q C5:e Bb4:e A4:e G4:e |""")
    alto, basso = marcia(modello_alto, modello_basso, 2, -1, RE_MINORE)
    alto = annota(alto, 0, dinamica='p')
    basso = annota(con_prima_nota(basso, 'D4'), 0, dinamica='p')
    alto += leggi("""
        r:e D5:e( G5:e F5:e) E5:e( G5:e) Bb5:e( A5:e) |
        G5:s( F5:s G5:s A5:s) Bb5:e G5:e A5:e F5:e G5:q* |""")
    basso += leggi("""
        Bb4:h G4:h |
        C5:q Bb4:q F4:q E4:q |""")
    return alto, basso


def entrata_fa() -> tuple[Voce, Voce]:
    """bb.15–17: soggetto in Fa maggiore al Flauto 1, controsoggetto rivoltato sotto."""
    fl1 = annota(mat.soggetto(FA_MAGGIORE, 'F5'), 0, dinamica='mf')
    fl2 = annota(con_prima_nota(mat.controsoggetto(FA_MAGGIORE, 'F4'), 'F4'), 0, dinamica='mf')
    return fl1, fl2


def episodio_2() -> tuple[Voce, Voce]:
    """bb.18–25: progressione ascendente Fa – Sol m – La m. Ogni coppia di battute
    porta la testa del soggetto al basso e la volta di semicrome sopra, poi la
    dominante secondaria della tonalità un grado più su; il motivo della coda
    passa da una voce all'altra nella cadenza in La minore."""
    fl1 = leggi("""
        A5:e r:e A5:s( G5:s A5:s Bb5:s) C6:q A5:q |
        A5:s( Bb5:s A5:s G5:s) F#5:e( C6:e) A5:e( C6:e) D6:q |
        Bb5:e r:e Bb5:s( A5:s Bb5:s C6:s) D6:q Bb5:q |
        B5:s( C6:s B5:s A5:s) G#5:e( D6:e) B5:e( D6:e) E6:q |
        C6:e r:e C6:s( B5:s C6:s D6:s) E6:q C6:q |
        B5:s( A5:s B5:s C6:s) D6:e( B5:e) C6:e( A5:e) B5:q |
        r:q F5:q E5:q D5:q |
        E5:s( D5:s E5:s F#5:s) G#5:e( B5:e) D6:e( B5:e) G#5:q* |""")
    fl2 = leggi("""
        F4:q C5:q A4:e( G4:e) F4:q |
        F#4:q A4:q C5:q Bb4:e( A4:e) |
        G4:q D5:q Bb4:e( A4:e) G4:q |
        G#4:e r:e B4:q D5:q C5:e( B4:e) |
        A4:q E5:q C5:e( B4:e) A4:q |
        G#4:q B4:q A4:q G#4:q |
        B4:s( A4:s B4:s C5:s) D5:e( B4:e) C5:e( A4:e) B4:q |
        E4:q B4:h E4:q |""")
    return fl1, fl2


def entrata_la() -> tuple[Voce, Voce]:
    """bb.26–28: soggetto in La minore (forma reale) al Flauto 2, controsoggetto sopra.
    Il soggetto chiude con una croma (respiro prima dell'inverso); il controsoggetto
    chiude salendo (La–Si → Do) per preparare l'inverso."""
    fl2 = annota(mat.soggetto(LA_MINORE, 'A4'), 0, dinamica='mf')
    fl2 = fl2[:-1] + [fl2[-1].con(durata=2)] + leggi('r:e', controlla_battute=False)
    fl1 = con_prima_nota(mat.controsoggetto(LA_MINORE, 'A5'), 'A5')
    fl1 = annota(fl1, -1, altezza='B5')
    return fl1, fl2


def episodio_3() -> tuple[Voce, Voce]:
    """bb.29–39: l'inverso del soggetto al Flauto 2 (La minore) e al Flauto 1
    (Re minore), poi marcia discendente sulla testa invertita (Sol m – Fa – Mi♭)
    e cadenza in Sol minore."""
    inv_la = annota(mat.inverso(LA_MINORE, 'E5'), 0, dinamica='p')
    fl2 = inv_la
    fl1 = leggi("""
        @p C6:s( B5:s A5:s B5:s) C6:e( B5:e) A5:q C6:s( B5:s C6:s D6:s) |
        D6:q. B5:e C6:h |
        B5:q G#5:q A5:e( C6:e) r:q |""")
    fl1 += annota(mat.inverso(), 0, dinamica='mf')
    fl2 += leggi("""
        r:e F4:e Bb4:e( G4:e) A4:q C#5:e( A4:e) |
        G4:h F4:q A4:q |
        Bb4:q C#5:q D5:q Bb4:q |""")
    alto, basso = marcia(
        leggi("r:e A5:e Bb5:q G5:q F5:s( G5:s A5:s F5:s) |"),
        leggi("D5:q G4:q Bb4:e( C5:e) D5:q |"),
        3, -1, SOL_MINORE)
    fl1 += alto + leggi("""
        r:e Eb5:s( F5:s) C6:e( G5:e) F#5:e( A5:e) C6:e( A5:e) |
        G5:e( F5:e) Eb5:e( G5:e) Bb5:q A5:q* |""")
    fl2 += basso + leggi("""
        C5:q Eb5:q D5:q C5:q |
        Bb4:q C5:q D5:h |""")
    return fl1, fl2


def entrata_sol() -> tuple[Voce, Voce]:
    """bb.40–42: soggetto in Sol minore al Flauto 1, controsoggetto rivoltato sotto."""
    fl1 = annota(mat.soggetto(SOL_MINORE, 'G5'), 0, dinamica='mf')
    fl2 = annota(con_prima_nota(mat.controsoggetto(SOL_MINORE, 'G4'), 'G4'), 0, dinamica='mf')
    return fl1, fl2


def episodio_4() -> tuple[Voce, Voce]:
    """bb.43–50: gli arpeggi di settima diminuita del soggetto passano da una voce
    all'altra riportando a Re minore; poi basso cromatico discendente (Re–Do♯–Do–Si–Si♭–La)
    con ritardi sopra, in crescendo, fino alla semicadenza sulla dominante."""
    fl1 = leggi("""
        Bb5:q r:e G5:e F#5:e( A5:e C6:e Eb6:e) |
        D6:q C6:e( Bb5:e) G5:h |
        F5:q E5:e( D5:e) C#5:e( E5:e G5:e Bb5:e) |
        @< A5:q Bb5:e( G5:e) E5:h* |
        F5:e( E5:e F5:e G5:e) A5:q~ A5:e( G5:e) |
        E5:q A5:q G5:q D5:q |
        G5:q Bb5:q~ Bb5:e( A5:e) G5:e( E5:e) |
        @= C#5:h E5:q r:q |""")
    fl2 = leggi("""
        G4:q Bb4:q D5:q C5:q |
        Bb4:q A4:q E4:e( G4:e Bb4:e C#5:e) |
        D5:q C5:e( Bb4:e) A4:q G4:q |
        @< F4:q G4:q A4:h |
        D5:h C#5:h |
        C5:h B4:h |
        Bb4:w |
        @= A4:h. r:q |""")
    return fl1, fl2


def stretti() -> tuple[Voce, Voce]:
    """bb.51–59. Stretto I: soggetto al Flauto 2, risposta alla quinta sopra al
    Flauto 1 dopo sei quarti. Stretto II: inverso al Flauto 2, risposta al Flauto 1
    dopo tre quarti. Le voci che guidano adattano la coda."""
    s = mat.soggetto()
    fl2 = annota(s[:12], 0, dinamica='f') + leggi("""
        E5:s( D5:s E5:s C5:s) D5:e( F5:e) E5:q D5:q |
        C5:q F5:e( E5:e) D5:q B4:q |
        A4:q G#4:q A4:q r:q |""")
    inv = mat.inverso()
    fl2 += inv[:12] + leggi("""
        F5:e( D5:e) C5:e( E5:e) B4:q G#4:q |
        B4:q A4:q D5:q E5:q |""")
    fl1 = leggi("r:w | r:h", controlla_battute=False) + annota(mat.risposta('A5'), 0, dinamica='f')
    fl1 += leggi("C6:h r:h r:q", controlla_battute=False) + mat.risposta('A5')
    fl1 += leggi("C#6:q", controlla_battute=False)
    return fl1, fl2


def pedale_dominante() -> tuple[Voce, Voce]:
    """bb.60–65: pedale di La al Flauto 2; sopra, frammenti di soggetto e inverso."""
    fl1 = leggi("""
        C#5:e( E5:e G5:e Bb5:e) A5:q G5:e( F5:e) |
        E5:s( D5:s E5:s F5:s) G5:e( E5:e) F5:e( D5:e) E5:q |
        r:e E5:e( G5:e Bb5:e) D6:q C#6:e( Bb5:e) |
        A5:s( G5:s A5:s Bb5:s) C#6:e( A5:e) D6:e( Bb5:e) G5:q |
        E6:q~ E6:e( D6:e) C#6:e( Bb5:e) A5:e( G5:e) |
        F5:e( E5:e D5:e C#5:e) r:e G5:e( E5:e C#5:e) |""")
    fl2 = pedale('A4', 6, riattacco=2)
    return fl1, fl2


def ultima_entrata() -> tuple[Voce, Voce]:
    """bb.66–68: ultima entrata del soggetto in Re minore al Flauto 1; sotto, il
    controsoggetto adattato (il Do♯4 è sotto l'estensione) che chiude con V–I."""
    fl1 = mat.soggetto()
    fl2 = leggi("""
        D4:q F4:s( E4:s F4:s A4:s) D4:q F4:s( E4:s D4:s F4:s) |
        E4:q. G4:e~ G4:e F4:e E4:e D4:e |
        E4:h D4:e( F4:e) A4:q |""")
    return fl1, fl2


def coda() -> tuple[Voce, Voce]:
    """bb.69–74: la testa al basso, la coda del soggetto sopra, poi pedale di tonica
    con l'arpeggio diminuito dell'inverso e chiusura sulla terza piccarda."""
    fl1 = leggi("""
        D5:q r:e E5:e A5:e( G5:e) F5:q |
        E5:s( D5:s E5:s F5:s) G5:e( E5:e) F5:e( D5:e) E5:q |
        r:e A5:e( F5:e D5:e) Bb5:e( G5:e E5:e C#5:e) |
        D5:q A5:q F5:e( E5:e) D5:q |
        "rall." C#5:e( E5:e G5:e Bb5:e) A5:q G5:e( E5:e) |
        F#5:w! |""")
    fl2 = leggi("""
        D4:q A4:q F4:e( E4:e) D4:q |
        A4:q Bb4:q D4:q A4:q |""") + pedale('D4', 4, riattacco=2)
    fl2 = annota(fl2, -1, corona=True)
    return fl1, fl2


SEZIONI_DEF = [
    ('Esposizione', 6, esposizione, 'Re minore → La minore',
     'Soggetto al Flauto 1 (bb.1–3); risposta tonale al Flauto 2 con controsoggetto al Flauto 1 (bb.4–6).'),
    ('Codetta', 2, codetta, 'La minore → Re minore', 'Coda del soggetto, ritorno alla tonica.'),
    ('Episodio 1', 6, episodio_1, 'Re minore → Fa maggiore',
     'Marcia per quinte discendenti sulla testa del soggetto, cadenza perfetta in Fa.'),
    ('Entrata in Fa maggiore', 3, entrata_fa, 'Fa maggiore',
     'Soggetto al Flauto 1, controsoggetto rivoltato al Flauto 2.'),
    ('Episodio 2', 8, episodio_2, 'Fa maggiore → La minore',
     'Progressione ascendente con dominanti secondarie; il motivo della coda passa fra le voci.'),
    ('Entrata in La minore', 3, entrata_la, 'La minore',
     'Soggetto (forma reale) al Flauto 2, controsoggetto al Flauto 1.'),
    ('Episodio 3', 11, episodio_3, 'La minore → Re minore → Sol minore',
     'Inverso al Flauto 2 (bb.29–31) e al Flauto 1 (bb.32–34), marcia sulla testa invertita, cadenza in Sol minore.'),
    ('Entrata in Sol minore', 3, entrata_sol, 'Sol minore',
     'Soggetto al Flauto 1, controsoggetto rivoltato al Flauto 2.'),
    ('Episodio 4', 8, episodio_4, 'Sol minore → Re minore',
     'Arpeggi di settima diminuita fra le voci, basso cromatico discendente, semicadenza su La.'),
    ('Stretti', 9, stretti, 'Re minore',
     'Stretto I (bb.51–55): soggetto e risposta a sei quarti. Stretto II (bb.56–59): inverso e risposta a tre quarti.'),
    ('Pedale di dominante', 6, pedale_dominante, 'Re minore (V)',
     'La tenuto al Flauto 2, frammenti del soggetto e dell\'inverso al Flauto 1.'),
    ('Ultima entrata', 3, ultima_entrata, 'Re minore', 'Soggetto al Flauto 1, cadenza perfetta.'),
    ('Coda', 6, coda, 'Re minore → Re maggiore',
     'Testa al basso, pedale di tonica, terza piccarda finale.'),
]


def componi() -> tuple[Voce, Voce, list[Sezione]]:
    fl1: Voce = []
    fl2: Voce = []
    sezioni = []
    battuta = 1
    for nome, n, funzione, tonalita, descrizione in SEZIONI_DEF:
        a, b = funzione()
        _controlla(nome, a, b, n)
        fl1 += a
        fl2 += b
        sezioni.append(Sezione(nome, battuta, battuta + n - 1, tonalita, descrizione))
        battuta += n
    return fl1, fl2, sezioni
