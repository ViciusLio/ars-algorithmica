# PIANO — Fuga a due voci in Re minore per due flauti traversi

Stato: **piano approvato e realizzato.** Questo è il documento scritto prima del codice; la forma effettiva, battuta per battuta, e gli scostamenti dal piano sono nel [README](README.md).

Notazione usata in questo documento (la stessa che userà il codice):
altezze in notazione scientifica (`C4` = Do centrale; `Bb` = Si♭, `C#` = Do♯),
durate `h` minima · `q` semiminima · `q.` semiminima puntata · `e` croma · `s` semicroma,
`~` legatura di valore, `r` pausa, `|` stanghetta.

---

## 1. Metro, tempo, organico

| | |
|---|---|
| Metro | 4/4 |
| Andamento | **Allegro moderato**, ♩ = 80 |
| Tonalità | Re minore (1 bemolle) |
| Organico | Flauto traverso 1, Flauto traverso 2 (`instrument.Flute()`) |
| Lunghezza | **74 battute** (minimo richiesto: 70) |
| Estensione | Re4–La6 assoluta; tessitura Re4–Mi6 (unica eccezione prevista: Fa6 come culmine nei due stretti) |

---

## 2. Soggetto (3 battute, Re minore)

```
b.1 | D5 q    A5 q      F5 e  E5 e   D5 q        |
b.2 | C#5 e   E5 e      G5 e  Bb5 e  A5 q   G5 e  F5 e |
b.3 | E5 s D5 s E5 s F5 s   G5 e E5 e   F5 e D5 e   E5 q |  → F5 (b.4, nota d'arrivo)
```

Gradi: `1 5 3 2 1 | ♯7 2 4 ♭6 5 4 3 | 2 1 2 3 4 2 3 1 2 | → 3`

Carattere e motivi (riusati negli episodi):

- **a — testa**: salto di quinta ascendente Re–La in semiminime. È il segnale ritmico riconoscibile di ogni entrata.
- **b**: discesa per grado a crome (Fa–Mi–Re).
- **c — slancio**: dalla sensibile **Do♯** l'arpeggio di settima diminuita Do♯–Mi–Sol–**Si♭** sale al culmine (sesto grado abbassato), che risolve su La.
- **d — coda**: volta di quattro semicrome + terze discendenti a crome (Sol–Mi, Fa–Re), chiusa sospesa sul 2° grado (armonia di dominante).

Il ritmo accelera in modo tipicamente bachiano: semiminime → crome → semicrome.
Ambito: Do♯5–Si♭5 (settima diminuita). L'ambito stretto è voluto: permette di trasportare il tema a tutti i livelli necessari restando nell'estensione del flauto.

Nota d'arrivo: nelle entrate interne il soggetto sfocia sul 3° grado (così la voce che entra una quarta sotto trova una sesta, non una quarta); nell'ultima entrata chiude su Re.

## 3. Risposta — **tonale**

Il soggetto tocca subito la dominante (Re→La sul secondo quarto), quindi la risposta deve essere tonale: alla quinta Re–La risponde la quarta La–Re (la dominante risponde con la tonica, non con Mi). La mutazione riguarda **una sola nota**; dal terzo quarto in poi la risposta è la trasposizione esatta alla dominante (La minore).

```
b.4 | A4 q    D5 q      C5 e  B4 e   A4 q        |
b.5 | G#4 e   B4 e      D5 e  F5 e   E5 q   D5 e  C5 e |
b.6 | B4 s A4 s B4 s C5 s   D5 e B4 e   C5 e A4 e   B4 q |  → C5 (b.7)
```

Effetto della mutazione: nel soggetto dopo il La si scende di terza (La–Fa), nella risposta dopo il Re si scende di grado (Re–Do). In La minore ricompaiono le due note caratteristiche: Fa♮ (sesto abbassato) e Sol♯ (sensibile).

## 4. Controsoggetto (invertibile al contrappunto doppio all'ottava)

Forma dell'esposizione, sopra la risposta (Flauto 1, bb. 4–6):

```
b.4 | F5 e  A5 s G5 s   F5 s E5 s F5 s G5 s   A5 q        C6 s B5 s A5 s C6 s |
b.5 | B5 q.             D6 e ~ D6 e   C6 e    B5 e  A5 e  |
b.6 | G#5 h                           A5 e  C6 e    B5 e  A5 s G#5 s |  → A5 (b.7)
```

Quando accompagna il **soggetto** (non la risposta) la testa cambia: pausa di semiminima (respiro) e poi la stessa volta di semicrome, `3 2 3 ♯7 → 1` (in Re minore: `r q | F s E s F s C# s | D q …`). Il corpo, dal terzo quarto in poi, è sempre identico.

**Complementarità ritmica**

| Punto | Risposta/Soggetto | Controsoggetto |
|---|---|---|
| b.1, quarti 1–2 | due semiminime (testa) | semicrome |
| b.1, quarto 3 | crome | semiminima |
| b.1, quarto 4 | semiminima | semicrome |
| b.2, quarti 1–2 | crome (arpeggio di 7ª dim.) | semiminima puntata + sincope |
| b.2, quarto 3 | semiminima | risoluzione del ritardo |
| b.3, quarti 1–2 | semicrome e crome | minima |
| b.3, quarto 4 | semiminima | croma + due semicrome (formula cadenzale) |

**Invertibilità** — già verificata con uno script di bozza (intervallo per intervallo, nelle due disposizioni):

- sui tempi forti ci sono solo terze, seste e ottave (che rivoltate restano seste, terze e ottave); nessuna quinta strutturale, quindi nessuna quarta nel rivolto;
- un **ritardo 7–6** preparato e risolto (b.2, terzo quarto: Re6 legato sopra Mi5 → Do6), che nel rivolto diventa un regolare **2–3** nella voce inferiore;
- un tritono Sol♯–Re in b.3 (armonia di V7) che risolve correttamente: Sol♯→La, Re→Do;
- le altre dissonanze sono note di passaggio o di volta su suddivisione debole, per grado congiunto;
- quattro seste parallele (b.2–3), che nel rivolto diventano terze parallele.

In pratica il rivolto si realizza alla quindicesima (il CS scende di due ottave rispetto alla disposizione originale), perché nell'originale compaiono anche decime.

## 5. Inverso del soggetto (per l'episodio 3 e lo stretto II)

Inversione tonale con asse sul 3° grado (1↔5, 2↔4, ♭6↔♯7): sensibile e sesto abbassato si scambiano, e l'arpeggio di settima diminuita diventa discendente.

```
| A5 q    D5 q      F5 e  G5 e   A5 q        |
| Bb5 e   G5 e      E5 e  C#5 e  D5 q   E5 e  F5 e |
| G5 s A5 s G5 s F5 s   E5 e G5 e   F5 e A5 e   G5 q |
```

---

## 6. Mappa formale

| Battute | Sezione | Tonalità | Flauto 1 | Flauto 2 | Chiusura |
|---|---|---|---|---|---|
| 1–3 | **Esposizione** — soggetto | Re min | **S** (da Re5) | tace | sospesa su V |
| 4–6 | Esposizione — risposta | La min | **CS** (sopra) | **R tonale** (da La4) | V–i in La min a b.7 |
| 7–8 | Codetta | La min → Re min | motivo *d* | linea di basso, respiro | cadenza in Re min a b.9 |
| 9–14 | **Episodio 1** | Re m – Sol m – Do – Fa | marcia armonica per quinte discendenti, modello di 1 battuta dalla testa (*a*+*b*), le voci si scambiano il modello | idem, in imitazione | bb.13–14 cadenza perfetta in Fa |
| 15–17 | **Entrata in Fa maggiore** | Fa magg | **S** (da Fa5) | **CS** (sotto: rivolto) | V–I in Fa a b.18 |
| 18–25 | **Episodio 2** | Fa → Sol m → La m | motivo *d* in dialogo, progressione ascendente per grado, modello di 2 battute | idem | bb.24–25 cadenza perfetta in La min |
| 26–28 | **Entrata in La minore** | La min | **CS** (sopra) | **S** (da La4, forma reale: La–Mi) | V–i in La min a b.29 |
| 29–31 | **Episodio 3** — inverso | La min | contrappunto libero | **Inverso** (da Mi5) | |
| 32–34 | Episodio 3 — inverso | Re min | **Inverso** (da La5) | contrappunto libero | |
| 35–39 | Episodio 3 — progressione | Re m → Sol m | testa invertita (quinta discendente + crome ascendenti) in progressione | idem | b.39 V7 di Sol min, cadenza a b.40 |
| 40–42 | **Entrata in Sol minore** | Sol min | **S** (da Sol5) | **CS** (sotto: rivolto) | V–i in Sol min a b.43 |
| 43–50 | **Episodio 4** | Sol m → Re m | motivo *c* (arpeggi di 7ª dim.) in progressione ascendente, con ritardi 7–6 presi dal CS | idem | bb.49–50 **semicadenza** su La (iv⁶–V, frigia) |
| 51–55 | **Stretto I** | Re min | **R** alla quinta sopra (da La5), entra a b.52 sul 3° quarto | **S** (da Re5) da b.51 | |
| 56–59 | **Stretto II** (più serrato, moto contrario) | Re min | **R** (da La5), entra dopo soli 3 quarti | **Inverso** (da La5) da b.56 | arrivo sulla dominante a b.60 |
| 60–65 | **Pedale di dominante** | Re min (V) | frammenti di *a* e *c* sopra il pedale, in crescendo | La4 tenuto (riattaccato ogni 2 battute per respirare) | V7 |
| 66–68 | **Ultima entrata** | Re min | **S** (da Re5), chiude su Re | basso libero derivato dal CS | |
| 69–74 | **Coda** | Re min → Re magg | formula cadenzale, ultima eco della testa | idem | cadenza perfetta; b.74 **terza piccarda** Re4 + Fa♯5 con corona |

Totale: 74 battute. Dodici entrate tematiche: 3 del soggetto in Re minore (bb. 1, 51, 66), 3 in altre tonalità (Fa b.15, La m b.26, Sol m b.40), 3 risposte tonali (bb. 4, 52, 56), 3 inversi (bb. 29, 32, 56); negli stretti sono sovrapposte a coppie.

### Sugli stretti (cosa aspettarsi)

Ho provato con lo script di bozza tutte le combinazioni soggetto/risposta/inverso a varie distanze. Risultati:

- **Stretto I** — S (Fl.2) e risposta tonale alla quinta sopra (Fl.1) a distanza di una battuta e mezza: la sovrapposizione è pulita finché dura la seconda battuta del soggetto; poi la voce che guida adatta la coda (motivo *d*) alla nuova armonia. La voce che segue espone il tema per intero.
- **Stretto II** — inverso (Fl.2) e risposta (Fl.1) a soli tre quarti: quasi un canone, con ritocchi nella terza battuta della voce che guida.
- Uno stretto **all'ottava** non è realizzabile con questo organico: l'entrata bassa richiederebbe Do♯4 (sotto il Re4 del flauto) e quella alta Si♭6 (sopra il La6).

Adattare la coda della voce che guida è prassi normale nello stretto; lo segnalo perché non si tratta di un canone rigoroso da capo a fondo.

### Registri delle entrate (tutti dentro l'estensione)

| Entrata | Voce | Ambito del tema | Ambito dell'altra voce |
|---|---|---|---|
| S Re min | Fl.1 | Do♯5–Si♭5 | — |
| R La min | Fl.2 | Sol♯4–Fa5 | CS Fl.1: Mi5–Re6 |
| S Fa magg | Fl.1 | Mi5–Re6 | CS Fl.2: Mi4–Si♭4 |
| S La min | Fl.2 | Sol♯4–Fa5 | CS Fl.1: Sol♯5–Re6 |
| Inverso La min | Fl.2 | Sol♯4–Fa5 | libero |
| Inverso Re min | Fl.1 | Do♯5–Si♭5 | libero |
| S Sol min | Fl.1 | Fa♯5–Mi♭6 | CS Fl.2: Fa♯4–Do5 |
| Stretti | Fl.2 / Fl.1 | Do♯5–Si♭5 / Sol♯5–**Fa6** | — |

Il Flauto 1 sta sempre sopra il Flauto 2 nelle entrate (nessun incrocio prolungato); il soggetto in Re minore compare sempre da Re5, perché un'ottava sotto servirebbe Do♯4.

---

## 7. Vincoli di scrittura e come li rispetto

- **Quinte e ottave**: nessuna parallela; quelle per moto retto evitate (ammesse solo con la voce superiore per grado, e comunque elencate dal controllo come avvisi).
- **Dissonanze**: solo note di passaggio/volta su tempo debole, ritardi preparati e risolti per grado discendente, tritoni dentro V7/vii° risolti.
- **Distanza fra le voci**: di norma entro la decima; nei rivolti del CS arriva per singoli istanti alla dodicesima.
- **Respiri**: ogni voce ha una pausa (almeno di croma) o una nota lunga ogni 4–6 battute; le entrate del CS sul soggetto iniziano con pausa di semiminima; il pedale è riattaccato ogni due battute.
- **Cadenze**: una cadenza chiara chiude ogni sezione (ultima colonna della mappa).
- **Dinamiche** (a terrazze, poche): `mf` all'inizio, `p` negli episodi 1 e 3, `mf` alle entrate interne, crescendo nell'episodio 4, `f` da stretto e pedale fino alla fine. Legature di frase solo sui gruppi di semicrome per grado e sulle formule cadenzali; le crome restano staccate, alla maniera barocca.

---

## 8. Architettura del codice (Fase 2)

```
Music/
├─ PIANO.md               questo documento
├─ README.md              forma e battute di ogni sezione (Fase 4)
├─ requirements.txt       music21
├─ fuga/
│  ├─ materiali.py        soggetto(), risposta(), controsoggetto(), motivi
│  ├─ trasformazioni.py   trasponi() diatonico, inverti(), cambio di modo, ottava
│  ├─ episodi.py          marcia_armonica(), progressioni, pedale, cadenze
│  ├─ forma.py            la mappa del §6 come dati: sezioni → frammenti per voce
│  └─ partitura.py        costruzione music21: parti, Flute(), armatura, metro,
│                         tempo, dinamiche, legature, esportazione
├─ componi.py             punto d'ingresso: genera i due file
├─ verifica.py            controlli della Fase 3
├─ fuga_re_minore.musicxml
└─ fuga_re_minore.mid
```

Scelte di impostazione:

- Le voci sono rappresentate internamente come liste di eventi `(altezza, durata)` in Python puro; music21 entra solo in `partitura.py` e `verifica.py`. Così le trasformazioni si testano senza dipendenze e il materiale è riusabile in altri brani.
- Nessuna variabile si chiamerà `note`, `chord`, `stream`, `key`, `meter`, `tempo`, `instrument`, `interval`, `pitch`, `duration`: uso nomi italiani (`nota_m21`, `parte_fl1`, `battuta`…).
- La trasposizione è **diatonica** rispetto alla tonalità d'arrivo, con sesto e settimo grado alterati come nel modello (♭6 e ♯7 in minore), in modo che la stessa funzione generi le entrate in Fa maggiore, La minore e Sol minore.

Prerequisito: sulla macchina c'è Python 3.14.2 ma **music21 non è installato**. La Fase 2 comincerà con `pip install music21` (in un ambiente virtuale `.venv` dentro la cartella del progetto).

## 9. Verifica automatica (Fase 3)

`verifica.py` rilegge il MusicXML prodotto (non le strutture interne) e riporta:

1. numero di battute (≥ 70) e durata di ciascuna (4 quarti esatti in entrambe le parti);
2. note fuori da Re4–La6, e a parte quelle sopra Mi6;
3. quinte e ottave parallele, con numero di battuta e quarto; in più, come avvisi, quinte/ottave per moto retto e incroci delle voci;
4. le entrate tematiche trovate per riconoscimento del profilo (intervalli diatonici + ritmo): battuta, voce, forma (soggetto / risposta / inverso) e tonalità, da confrontare con la mappa del §6;
5. in aggiunta: respiro più lontano per ciascuna voce e distanza massima fra le voci.

Se un controllo fallisce correggo la scrittura e ripeto, finché il rapporto è pulito.

## 10. Output (Fase 4)

`fuga_re_minore.musicxml` (da aprire in MuseScore), `fuga_re_minore.mid`, e `README.md` con la forma effettiva e le battute di ogni sezione.
