# 01 · Fuga a due voci in Re minore

*Two-part fugue in D minor for two flutes, in the style of J.S. Bach, written as Python code with music21.*

Fuga a due voci per due flauti traversi, 74 battute in 4/4, Allegro moderato (♩ = 80).
Ogni nota è generata dal codice: il soggetto è scritto una volta sola, risposta,
controsoggetto, inverso ed entrate nelle altre tonalità si ottengono con funzioni di
trasformazione, e uno script di verifica controlla il risultato sul file MusicXML.

*Questo primo esperimento è dedicato alla mia cara Amica Annalisa.*

**[▶ Ascolta e leggi la partitura online](https://viciuslio.github.io/ars-algorithmica/experiments/01-fuga-re-minore/fuga-in-re-minore-ars-algo.html)**

| File | Contenuto |
|---|---|
| [`fuga-in-re-minore-ars-algo.html`](fuga-in-re-minore-ars-algo.html) | anteprima "Fuga in Re minore · ars-algo": partitura, ascolto con campioni di flauto e mappa cliccabile della forma (si apre anche con un doppio clic, serve internet per le librerie) |
| [`fuga_re_minore.musicxml`](fuga_re_minore.musicxml) | partitura (si apre con MuseScore) |
| [`fuga_re_minore.mid`](fuga_re_minore.mid) | esecuzione MIDI (due flauti, dinamiche come velocità) |
| [`PIANO.md`](PIANO.md) | il piano compositivo scritto prima del codice |
| [`rapporto_verifica.txt`](rapporto_verifica.txt) | l'ultimo esito di `verifica.py` |

## Come rigenerarla

Dalla radice del repository:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # su Linux/macOS: .venv/bin/python
cd experiments/01-fuga-re-minore
../../.venv/Scripts/python componi.py    # scrive .musicxml, .mid e l'anteprima .html
../../.venv/Scripts/python verifica.py   # controlla il MusicXML e scrive rapporto_verifica.txt
```

## Materiali

Notazione: `C4` = Do centrale, `q` semiminima, `e` croma, `s` semicroma, `~` legatura di valore.

**Soggetto** (3 battute): testa con salto di quinta Re-La, discesa per grado, arpeggio di
settima diminuita dalla sensibile Do♯ al culmine Si♭ (sesto abbassato), coda in semicrome.

```
D5:q A5:q F5:e E5:e D5:q | C#5:e E5:e G5:e Bb5:e A5:q G5:e F5:e | E5:s D5:s E5:s F5:s G5:e E5:e F5:e D5:e E5:q
```

**Risposta tonale**: il soggetto tocca subito la dominante, quindi a Re-La risponde La-Re
(una sola nota mutata, il resto è trasposto in La minore).

**Controsoggetto**: invertibile al contrappunto doppio all'ottava (in pratica alla
quindicesima) e ritmicamente complementare. Contiene un ritardo 7-6 preparato e risolto,
che nel rivolto diventa 2-3.

**Inverso**: inversione diatonica con asse sul terzo grado (1↔5, ♭6↔♯7), così l'arpeggio
diminuito diventa discendente.

## Forma

| Battute | Sezione | Tonalità | Che cosa succede |
|---|---|---|---|
| 1-6 | **Esposizione** | Re m → La m | Soggetto al Flauto 1; risposta tonale al Flauto 2 (b.4) con controsoggetto sopra |
| 7-8 | Codetta | La m → Re m | Coda del soggetto, ritorno alla tonica |
| 9-14 | **Episodio 1** | Re m → Fa | Marcia per quinte discendenti (Re m, Sol m, Do, Fa) sulla testa del soggetto, modello di due battute con scambio delle parti; cadenza perfetta in Fa |
| 15-17 | **Entrata in Fa maggiore** | Fa | Soggetto al Flauto 1, controsoggetto rivoltato sotto |
| 18-25 | **Episodio 2** | Fa → Sol m → La m | Progressione ascendente con dominanti secondarie e basso cromatico (Fa-Fa♯-Sol-Sol♯-La); il motivo della coda passa da una voce all'altra; cadenza in La minore |
| 26-28 | **Entrata in La minore** | La m | Soggetto (forma reale) al Flauto 2, controsoggetto sopra |
| 29-39 | **Episodio 3** | La m → Re m → Sol m | Inverso al Flauto 2 (bb.29-31, La m) e al Flauto 1 (bb.32-34, Re m); marcia discendente sulla testa invertita (Sol m, Fa, Mi♭); cadenza in Sol minore |
| 40-42 | **Entrata in Sol minore** | Sol m | Soggetto al Flauto 1, controsoggetto rivoltato sotto |
| 43-50 | **Episodio 4** | Sol m → Re m | Arpeggi di settima diminuita fra le voci; poi basso cromatico discendente Re-Do♯-Do-Si-Si♭-La (*lamento*) in crescendo; semicadenza frigia sulla dominante |
| 51-55 | **Stretto I** | Re m | Soggetto al Flauto 2; risposta alla quinta sopra al Flauto 1 dopo sei quarti (b.52) |
| 56-59 | **Stretto II** | Re m | Inverso al Flauto 2; risposta al Flauto 1 dopo soli tre quarti |
| 60-65 | **Pedale di dominante** | Re m (V) | La tenuto al Flauto 2 (riattaccato ogni due battute); sopra, arpeggi e coda del soggetto |
| 66-68 | **Ultima entrata** | Re m | Soggetto al Flauto 1, cadenza perfetta |
| 69-74 | **Coda** | Re m → Re magg | Testa al basso, pedale di tonica, ultima allusione al soggetto (b.72), **terza piccarda** finale (Re4 + Fa♯5) con corona |

Dinamiche a terrazze: *mf* all'esposizione e alle entrate, *p* negli episodi 1 e 3,
crescendo nel lamento dell'episodio 4, *f* dagli stretti alla fine.

## Entrate trovate dalla verifica

`verifica.py` riconosce il tema dal ritmo e dagli intervalli diatonici, quindi in qualsiasi tonalità:

| Battuta | Voce | Forma | Tonalità |
|---|---|---|---|
| 1 | Flauto 1 | Soggetto | Re minore |
| 4 | Flauto 2 | Risposta tonale | La minore |
| 15 | Flauto 1 | Soggetto | Fa maggiore |
| 26 | Flauto 2 | Soggetto | La minore |
| 29 | Flauto 2 | Inverso | La minore |
| 32 | Flauto 1 | Inverso | Re minore |
| 40 | Flauto 1 | Soggetto | Sol minore |
| 51 | Flauto 2 | Soggetto (stretto, coda adattata) | Re minore |
| 52 (3° quarto) | Flauto 1 | Risposta tonale | La minore |
| 56 | Flauto 2 | Inverso (stretto, coda adattata) | Re minore |
| 56 (4° quarto) | Flauto 1 | Risposta tonale | La minore |
| 66 | Flauto 1 | Soggetto | Re minore |
| 72 | Flauto 1 | Testa e arpeggio del soggetto (allusione finale) | Re minore |

## Che cosa controlla la verifica

1. 74 battute (minimo 70), tutte di 4/4 esatti in entrambe le parti.
2. Estensione Re4-La6 rispettata (Flauto 1: Do5-Fa6, Flauto 2: Re4-Si♭5); sopra Mi6 solo
   i due Fa6 previsti come culmine degli stretti (bb.53 e 58).
3. Nessuna quinta od ottava parallela; nessuna quinta/ottava per moto retto con salto della
   voce superiore.
4. Le entrate della tabella qui sopra.

Inoltre, come avvisi: nessuna dissonanza sui tempi che non sia passaggio, volta, ritardo
o tritono dell'armonia di dominante (sopra i pedali le dissonanze sono libere); nessun
incrocio delle voci; respiro almeno ogni 6 battute per flauto; distanza fra le voci entro
la decima tranne pochi istanti (semicrome di passaggio, controsoggetto rivoltato e pedali).

## Struttura del codice

```
componi.py            genera MusicXML e MIDI
verifica.py           controlli della Fase 3 sul MusicXML
fuga/
  notazione.py        notazione testuale (D5:q, Bb4:e~ …) ed eventi in sedicesimi
  trasformazioni.py   trasposizione diatonica, cambio di tonalità e modo, inversione
  materiali.py        soggetto, risposta tonale (calcolata), controsoggetto, inverso, motivi
  episodi.py          marce armoniche e pedali
  forma.py            le 13 sezioni, battuta per battuta
  analisi.py          paralleli, dissonanze, incroci, respiri, riconoscimento delle entrate
  partitura.py        music21: parti, Flute(), armatura, metro, tempo, dinamiche, legature, export
  anteprima.py        pagina HTML con partitura (OpenSheetMusicDisplay) e ascolto (html-midi-player)
```

Le voci restano liste di eventi in Python puro fino all'ultimo passaggio, quindi materiali
e controlli si possono riusare per altri brani senza music21. music21 è importato come
`m21` e nessuna variabile si chiama `note`, `chord` o `stream`.

## Scostamenti dal piano

- **Episodio 4**: oltre agli arpeggi di settima diminuita c'è un basso cromatico
  discendente (lamento), che prepara la semicadenza meglio di una progressione ascendente.
- **Stretti**: come previsto, la voce che guida adatta la coda. In entrambi gli stretti il
  Flauto 1 attacca all'unisono con il Flauto 2 (La5) e se ne stacca dalla nota successiva.
- **Ultima entrata**: il Flauto 2 suona un controsoggetto adattato, perché quello originale
  scenderebbe al Do♯4, sotto l'estensione del flauto.
