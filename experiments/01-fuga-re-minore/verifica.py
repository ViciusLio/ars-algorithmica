"""Verifica automatica della fuga, eseguita sul file MusicXML prodotto.

Controlla: numero e completezza delle battute, estensione dei flauti, quinte e
ottave parallele, entrate del tema (forma e tonalità); in più, come avvisi,
quinte/ottave per moto retto, dissonanze non preparate, incroci, distanza fra
le voci e respiri. Esce con codice 1 se trova errori.

Uso:  python verifica.py [file.musicxml]
"""
from __future__ import annotations

import sys
from pathlib import Path

import music21 as m21

from fuga import analisi as an
from fuga import materiali as mat
from fuga.notazione import BATTUTA, Evento

CARTELLA = Path(__file__).resolve().parent
FILE = CARTELLA / 'fuga_re_minore.musicxml'
RAPPORTO = CARTELLA / 'rapporto_verifica.txt'

MIN_BATTUTE = 70
ESTENSIONE = ('D4', 'A6')
TESSITURA_ALTA = 'E6'
MAX_SENZA_RESPIRO = 6  # battute
MAX_DISTANZA = 16  # semitoni: decima maggiore


def _nome(p: m21.pitch.Pitch) -> str:
    return p.nameWithOctave.replace('-', 'b')


def leggi_parte(parte: m21.stream.Part) -> tuple[list[an.Suono], list[Evento]]:
    """Suoni (note legate unite) ed eventi con pause, in sedicesimi."""
    piatta = parte.stripTies().flatten()
    suoni, eventi = [], []
    for el in piatta.notesAndRests:
        inizio = round(float(el.offset) * 4)
        durata = round(float(el.quarterLength) * 4)
        if el.isRest:
            eventi.append(Evento(None, durata))
        else:
            nome = _nome(el.pitch)
            suoni.append(an.Suono(inizio, durata, el.pitch.midi, nome))
            eventi.append(Evento(nome, durata))
    return suoni, eventi


def verifica(file: Path) -> tuple[list[str], int]:
    partitura = m21.converter.parse(file)
    parti = list(partitura.parts)
    righe: list[str] = []
    errori = 0

    def titolo(testo: str) -> None:
        righe.append('')
        righe.append(testo)
        righe.append('-' * len(testo))

    righe.append(f"Verifica di {file.name}")

    # 1. battute ---------------------------------------------------------------
    titolo('1. Battute')
    conteggi = []
    for parte in parti:
        misure = list(parte.getElementsByClass(m21.stream.Measure))
        conteggi.append(len(misure))
        incomplete = [m.number for m in misure
                      if abs(m.duration.quarterLength - m.barDuration.quarterLength) > 1e-9]
        stato = 'tutte complete (4/4)' if not incomplete else f"INCOMPLETE: {incomplete}"
        errori += len(incomplete)
        righe.append(f"{parte.partName}: {len(misure)} battute, {stato}")
    if len(set(conteggi)) != 1:
        errori += 1
        righe.append("ERRORE: le parti hanno un numero diverso di battute")
    if min(conteggi) < MIN_BATTUTE:
        errori += 1
        righe.append(f"ERRORE: meno di {MIN_BATTUTE} battute")
    else:
        righe.append(f"OK: {min(conteggi)} battute (minimo richiesto {MIN_BATTUTE})")

    voci = [leggi_parte(p) for p in parti]
    (s1, e1), (s2, e2) = voci

    # 2. estensione ------------------------------------------------------------
    titolo(f"2. Estensione ({ESTENSIONE[0]}–{ESTENSIONE[1]})")
    for parte, (suoni, _) in zip(parti, voci):
        fuori = an.fuori_estensione(suoni, *ESTENSIONE)
        alte = [s for s in an.fuori_estensione(suoni, ESTENSIONE[0], TESSITURA_ALTA) if s not in fuori]
        bassa = min(suoni, key=lambda s: s.midi)
        alta = max(suoni, key=lambda s: s.midi)
        righe.append(f"{parte.partName}: da {bassa.nome} a {alta.nome}"
                     + (f" — FUORI ESTENSIONE: {[(an.dove(s.inizio), s.nome) for s in fuori]}" if fuori else " — OK"))
        if alte:
            righe.append(f"   sopra {TESSITURA_ALTA} (culmini previsti): "
                         + ', '.join(f"{an.dove(s.inizio)} {s.nome}" for s in alte))
        errori += len(fuori)

    # 3. quinte e ottave parallele --------------------------------------------
    titolo('3. Quinte e ottave parallele')
    paralleli = an.paralleli(s1, s2)
    errori += len(paralleli)
    righe += paralleli or ['Nessuna.']
    dirette = an.dirette(s1, s2)
    righe.append(f"Quinte/ottave per moto retto con salto della voce superiore: {len(dirette) or 'nessuna'}")
    righe += [f"   {d}" for d in dirette]

    # 4. entrate del tema --------------------------------------------------------
    titolo('4. Entrate del tema')
    modelli = [an.modello('Soggetto', mat.soggetto()),
               an.modello('Risposta tonale', mat.risposta()),
               an.modello('Inverso', mat.inverso(), indice_tonica=1, indice_terza=2)]
    trovate = []
    for parte, (suoni, _) in zip(parti, voci):
        for e in an.entrate(suoni, modelli):
            trovate.append((e['inizio'], parte.partName, e))
    for inizio, nome, e in sorted(trovate, key=lambda x: x[0]):
        completezza = 'completa' if e['completa'] else f"testa e arpeggio ({e['note']}/{e['totale']} note)"
        righe.append(f"{an.dove(inizio):<10} {nome:<9} {e['forma']:<16} {e['tonalita']:<12} "
                     f"da {e['prima_nota']:<4} {completezza}")

    # 5. altri controlli (avvisi) ---------------------------------------------
    titolo('5. Altri controlli (avvisi, non bloccanti)')
    diss = an.dissonanze(s1, s2)
    righe.append(f"Dissonanze sui tempi non preparate/non risolte: {len(diss) or 'nessuna'}")
    righe += [f"   {d}" for d in diss]
    incroci = an.incroci(s1, s2)
    righe.append(f"Incroci delle voci: {len(incroci) or 'nessuno'}"
                 + ''.join(f"\n   {an.dove(a)} per {(b - a) / 4:g} quarti" for a, b in incroci))
    distanti = an.distanze_eccessive(s1, s2, MAX_DISTANZA)
    righe.append(f"Attacchi oltre la decima: {len(distanti)} su {len(an.sonorita(s1, s2))} "
                 f"(soprattutto semicrome di passaggio, controsoggetto rivoltato e pedali)")
    for parte, eventi in zip(parti, (e1, e2)):
        tratti = an.respiri(eventi)
        piu_lungo = max(tratti, key=lambda x: x[1] - x[0])
        lunghezza = (piu_lungo[1] - piu_lungo[0]) / BATTUTA
        stato = 'OK' if lunghezza <= MAX_SENZA_RESPIRO else 'TROPPO LUNGO'
        righe.append(f"Respiri {parte.partName}: tratto più lungo senza pause né note lunghe "
                     f"{lunghezza:.1f} battute (da {an.dove(piu_lungo[0])}) — {stato}")

    titolo('Esito')
    righe.append('NESSUN ERRORE' if errori == 0 else f"{errori} ERRORI")
    return righe, errori


def main() -> int:
    file = Path(sys.argv[1]) if len(sys.argv) > 1 else FILE
    righe, errori = verifica(file)
    testo = '\n'.join(righe)
    print(testo)
    RAPPORTO.write_text(testo + '\n', encoding='utf-8')
    return 1 if errori else 0


if __name__ == '__main__':
    sys.exit(main())
