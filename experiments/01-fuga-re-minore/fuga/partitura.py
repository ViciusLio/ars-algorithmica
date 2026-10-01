"""Costruzione della partitura music21 ed esportazione in MusicXML e MIDI.

music21 è importato come `m21`, quindi nessun nome locale copre i suoi moduli
(`note`, `chord`, `stream`...).
"""
from __future__ import annotations

from pathlib import Path

import music21 as m21

from .forma import Sezione
from .notazione import BATTUTA, Evento, Voce

TITOLO = 'Fuga a due voci in Re minore'
SOTTOTITOLO = 'per due flauti traversi'
AUTORE = 'ars-algorithmica · esperimento 01 (Python + music21)'
ANDAMENTO = ('Allegro moderato', 80)

# velocità MIDI per le dinamiche (il MusicXML conserva i segni, il MIDI li "suona")
VELOCITA = {'pp': 40, 'p': 52, 'mp': 64, 'mf': 76, 'f': 92, 'ff': 106}


def _nome_m21(altezza: str) -> str:
    """'Bb4' → 'B-4' (music21 usa il trattino per il bemolle)."""
    return altezza[0] + altezza[1:].replace('b', '-')


def _in_battute(voce: Voce) -> list[list[Evento]]:
    """Divide la voce in battute; un evento a cavallo della stanghetta viene spezzato e legato."""
    battute: list[list[Evento]] = [[]]
    t = 0
    for ev in voce:
        resto = ev.durata
        primo = True
        while resto:
            spazio = BATTUTA - t % BATTUTA
            parte = min(resto, spazio)
            spezzato = parte < resto
            pezzo = ev.con(durata=parte,
                           legatura=(ev.legatura or spezzato) and not ev.pausa,
                           **({} if primo else dict(dinamica=None, forcella=None, testo=None,
                                                    arco_inizio=False, trillo=False)))
            if spezzato:
                pezzo = pezzo.con(arco_fine=False, corona=False)
            battute[-1].append(pezzo)
            t += parte
            resto -= parte
            primo = False
            if t % BATTUTA == 0:
                battute.append([])
    if not battute[-1]:
        battute.pop()
    return battute


def costruisci_parte(voce: Voce, nome: str, abbreviazione: str, sezioni: list[Sezione],
                     con_indicazioni: bool) -> m21.stream.Part:
    parte = m21.stream.Part(id=abbreviazione)
    parte.partName = nome
    parte.partAbbreviation = abbreviazione
    flauto = m21.instrument.Flute()
    flauto.partName = nome
    flauto.partAbbreviation = abbreviazione
    parte.insert(0, flauto)

    inizi_sezione = {s.prima: s.nome for s in sezioni}
    archi, forcelle = [], []
    forcella_aperta = None  # (tipo, prima nota, note coinvolte)
    arco_aperto = None
    legata_prec = False
    velocita = VELOCITA['mf']
    for numero, eventi in enumerate(_in_battute(voce), start=1):
        misura = m21.stream.Measure(number=numero)
        if numero == 1:
            misura.insert(0, m21.clef.TrebleClef())
            misura.insert(0, m21.key.KeySignature(-1))
            misura.insert(0, m21.meter.TimeSignature('4/4'))
            if con_indicazioni:
                testo, bpm = ANDAMENTO
                misura.insert(0, m21.tempo.MetronomeMark(text=testo, number=bpm,
                                                         referent=m21.duration.Duration(1.0)))
        if con_indicazioni and numero in inizi_sezione:
            misura.insert(0, m21.expressions.RehearsalMark(inizi_sezione[numero]))
        offset = 0.0
        for ev in eventi:
            durata = m21.duration.Duration(ev.durata / 4)
            if ev.pausa:
                elemento = m21.note.Rest(duration=durata)
                legata_prec = False
            else:
                elemento = m21.note.Note(_nome_m21(ev.altezza), duration=durata)
                if legata_prec and ev.legatura:
                    elemento.tie = m21.tie.Tie('continue')
                elif legata_prec:
                    elemento.tie = m21.tie.Tie('stop')
                elif ev.legatura:
                    elemento.tie = m21.tie.Tie('start')
                legata_prec = ev.legatura
                if ev.trillo:
                    elemento.expressions.append(m21.expressions.Trill())
                if ev.arco_inizio:
                    arco_aperto = elemento
                if ev.arco_fine and arco_aperto is not None:
                    archi.append(m21.spanner.Slur(arco_aperto, elemento))
                    arco_aperto = None
            if ev.corona:
                corona = m21.expressions.Fermata()
                corona.type = 'upright'
                elemento.expressions.append(corona)
            if ev.dinamica:
                misura.insert(offset, m21.dynamics.Dynamic(ev.dinamica))
                velocita = VELOCITA[ev.dinamica]
            if ev.forcella in ('<', '>'):
                forcella_aperta = (ev.forcella, elemento, [])
            if ev.testo:
                misura.insert(offset, m21.expressions.TextExpression(ev.testo))
            if not ev.pausa:
                elemento.volume.velocityIsRelative = False  # niente ricalcolo dalle dinamiche
                elemento.volume.velocity = velocita
                if forcella_aperta:
                    forcella_aperta[2].append(elemento)
            if ev.forcella == '=' and forcella_aperta:
                tipo, inizio, coinvolte = forcella_aperta
                classe = m21.dynamics.Crescendo if tipo == '<' else m21.dynamics.Diminuendo
                forcelle.append(classe(inizio, elemento))
                velocita = _sfuma_velocita(coinvolte, velocita, tipo)
                forcella_aperta = None
            misura.insert(offset, elemento)
            offset += ev.durata / 4
        parte.append(misura)

    for sp in archi:
        parte.insert(0, sp)
    for sp in forcelle:
        parte.insert(0, sp)
    parte.getElementsByClass(m21.stream.Measure).last().rightBarline = m21.bar.Barline('final')
    return parte


def _sfuma_velocita(note_coinvolte: list, v0: int, tipo: str) -> int:
    """Nel MIDI la forcella diventa un aumento (o calo) graduale della velocità.
    Restituisce la velocità raggiunta alla fine."""
    v1 = min(127, v0 + 20) if tipo == '<' else max(30, v0 - 20)
    for i, n in enumerate(note_coinvolte):
        n.volume.velocity = round(v0 + (v1 - v0) * i / max(1, len(note_coinvolte) - 1))
    return v1


def costruisci_partitura(fl1: Voce, fl2: Voce, sezioni: list[Sezione]) -> m21.stream.Score:
    partitura = m21.stream.Score()
    meta = m21.metadata.Metadata()
    meta.title = TITOLO
    meta.subtitle = SOTTOTITOLO
    meta.composer = AUTORE
    partitura.metadata = meta
    partitura.insert(0, costruisci_parte(fl1, 'Flauto 1', 'Fl. 1', sezioni, con_indicazioni=True))
    partitura.insert(0, costruisci_parte(fl2, 'Flauto 2', 'Fl. 2', sezioni, con_indicazioni=False))
    return partitura


def esporta(partitura: m21.stream.Score, cartella: Path, nome: str) -> tuple[Path, Path]:
    xml = partitura.write('musicxml', fp=cartella / f'{nome}.musicxml')
    mid = partitura.write('midi', fp=cartella / f'{nome}.mid')
    return Path(xml), Path(mid)
