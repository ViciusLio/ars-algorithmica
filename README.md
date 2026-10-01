# ars-algorithmica

**A sound workshop — *una bottega sonora* — for music written as code.**

In a Renaissance *bottega*, apprentices learned a craft by making real pieces under real
constraints. This repository works the same way: each experiment is a piece of music
built from source code, with the rules of its style written down as checks the code
must pass. The output is the kind of material musicians actually use: a score you can open in
MuseScore (MusicXML) and a MIDI file you can listen to.

The idea is not to have a machine "improvise" music, but to treat composition as
engineering in the old sense of the word: plan, materials, transformations,
verification.

## Experiments

| # | Experiment | What it explores |
|---|---|---|
| 01 | [Fuga a due voci in Re minore](experiments/01-fuga-re-minore/) | A 74-bar two-part fugue for two flutes in the style of J.S. Bach. Subject, tonal answer, invertible countersubject, inversion and strettos are derived by diatonic transformations, and a verifier checks range, parallel fifths/octaves, dissonance treatment, breathing points and every thematic entry. |

Each experiment folder contains its own plan (`PIANO.md`), the generator, the
verifier, the generated score and MIDI, and a README describing the form bar by bar.
The experiment documents are written in Italian; the code is commented in Italian.

## Principles

- **Plan before code.** Every piece starts from a written plan: materials, form, constraints.
- **Write the material once, derive the rest.** Answers, inversions, transpositions and
  sequences are functions, not copy-paste.
- **Constraints are tests.** Range, voice leading, dissonance treatment and form are
  checked automatically on the exported score, not just on internal data.
- **Plain data first.** Music lives as simple Python data until the last step; music21
  is used only for engraving and export, so the core ideas stay portable.
- **Outputs musicians can use.** MusicXML for notation software, MIDI for listening.

## Getting started

Requires Python 3.10+.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt     # Linux/macOS: .venv/bin/python
cd experiments/01-fuga-re-minore
../../.venv/Scripts/python componi.py     # writes fuga_re_minore.musicxml and .mid
../../.venv/Scripts/python verifica.py    # verifies the score, writes rapporto_verifica.txt
```

Open the `.musicxml` file with [MuseScore](https://musescore.org) to see and hear the score.

## Possible next experiments

- Canons and invertible counterpoint generated from constraints (a small search engine for
  countersubjects and stretto distances).
- Four-part chorale harmonization with a rule checker.
- Process music (phasing, additive rhythms) where the score is a function of time.
- A shared toolkit extracted from the experiments: notation, transformations, analysis.

## Tools

[music21](https://web.mit.edu/music21/) for notation and export ·
[MuseScore](https://musescore.org) to open the scores.

## License

Code: [MIT](LICENSE). Music (scores, MIDI files and the musical material in the code):
[CC BY 4.0](LICENSE-MUSIC.md). Reuse is welcome, just credit the source.
