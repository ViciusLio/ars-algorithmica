"""Anteprima HTML autonoma: partitura, ascolto e mappa della forma in una sola pagina.

La pagina contiene già il MusicXML e il MIDI (nessun file esterno da caricare),
quindi si apre anche con un doppio clic; su GitHub Pages diventa la vetrina
dell'esperimento. Le librerie arrivano da CDN:
OpenSheetMusicDisplay per la partitura, html-midi-player per l'audio.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

from .forma import Sezione

TITOLO_PAGINA = 'Fuga in Re minore · ars-algo'
SECONDI_PER_BATTUTA = 4 * 60 / 80  # 4/4 a ♩ = 80
REPO = 'https://github.com/ViciusLio/ars-algorithmica'

_MODELLO = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITOLO__</title>
<meta name="description" content="Fuga a due voci in Re minore per due flauti, scritta come codice Python con music21: partitura, ascolto e forma.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap">
<style>
  :root {
    color-scheme: light;
    --carta: #f7f3ec; --foglio: #ffffff; --inchiostro: #1f1b16; --tenue: #6b6257;
    --linea: #e3d9ca; --accento: #8c2f39; --accento-chiaro: #f1dfdc;
    --episodio: #d9cdb9; --stretto: #5c1f27; --pedale: #a8865a;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--carta); color: var(--inchiostro);
         font: 16px/1.55 Inter, system-ui, sans-serif; }
  main { max-width: 1100px; margin: 0 auto; padding: 40px 16px 64px; }
  header { margin-bottom: 28px; }
  .marchio { font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--accento); font-weight: 600; }
  h1 { font: 600 clamp(36px, 6vw, 56px)/1.05 'EB Garamond', Georgia, serif; margin: 6px 0 6px; }
  .sottotitolo { font: italic 500 22px/1.3 'EB Garamond', Georgia, serif; color: var(--tenue); margin: 0 0 14px; }
  .dati { display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0; list-style: none; }
  .dati li { font-size: 13px; padding: 4px 10px; border: 1px solid var(--linea); border-radius: 999px; background: var(--foglio); }
  section { margin-top: 28px; }
  h2 { font: 600 24px/1.2 'EB Garamond', Georgia, serif; margin: 0 0 12px; }
  .riquadro { background: var(--foglio); border: 1px solid var(--linea); border-radius: 12px; padding: 18px; }
  midi-player { display: block; width: 100%; }
  midi-player::part(control-panel) { background: var(--accento-chiaro); border-radius: 10px; }
  midi-player::part(play-button) { color: var(--accento); }
  midi-player::part(seek-bar) { accent-color: var(--accento); }
  .stato { font-size: 14px; color: var(--tenue); margin-top: 10px; min-height: 1.5em; }
  .stato strong { color: var(--inchiostro); }
  .scarica { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
  .scarica a { font-size: 14px; color: var(--accento); text-decoration: none; border: 1px solid var(--accento);
               border-radius: 8px; padding: 6px 12px; }
  .scarica a:hover { background: var(--accento); color: #fff; }
  .linea-tempo { display: flex; height: 44px; border-radius: 8px; overflow: hidden; border: 1px solid var(--linea); }
  .linea-tempo button { border: 0; padding: 0; cursor: pointer; font: 600 11px Inter, sans-serif; color: var(--inchiostro);
                        border-right: 1px solid rgba(255,255,255,.6); overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 4px; }
  .linea-tempo button:last-child { border-right: 0; }
  .linea-tempo button[data-tipo="tema"] { background: var(--accento); color: #fff; }
  .linea-tempo button[data-tipo="episodio"] { background: var(--episodio); }
  .linea-tempo button[data-tipo="stretto"] { background: var(--stretto); color: #fff; }
  .linea-tempo button[data-tipo="pedale"] { background: var(--pedale); color: #fff; }
  .linea-tempo button.attiva { outline: 3px solid var(--inchiostro); outline-offset: -3px; }
  .legenda { margin: 14px 0 0; padding: 0; list-style: none; display: grid; gap: 6px 18px;
             grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
  .legenda li { font-size: 14px; display: grid; grid-template-columns: 76px 1fr; gap: 8px; padding: 6px 8px; border-radius: 6px; cursor: pointer; }
  .legenda li:hover, .legenda li.attiva { background: var(--accento-chiaro); }
  .legenda .battute { color: var(--tenue); font-variant-numeric: tabular-nums; white-space: nowrap; }
  .legenda .nome { font-weight: 600; }
  .legenda .descr { display: block; color: var(--tenue); font-size: 13px; }
  #partitura { min-height: 240px; }
  #partitura .attesa { color: var(--tenue); font-style: italic; }
  footer { margin-top: 40px; font-size: 13px; color: var(--tenue); border-top: 1px solid var(--linea); padding-top: 16px; }
  footer a { color: var(--accento); }
</style>
</head>
<body>
<main>
  <header>
    <div class="marchio">ars-algo · esperimento 01</div>
    <h1>Fuga in Re minore</h1>
    <p class="sottotitolo">a due voci per due flauti traversi, nello stile di J.S. Bach</p>
    <ul class="dati">
      <li>__BATTUTE__ battute</li><li>4/4</li><li>Allegro moderato, ♩ = 80</li>
      <li>scritta come codice Python con music21</li>
    </ul>
  </header>

  <section aria-labelledby="ascolto">
    <h2 id="ascolto">Ascolto</h2>
    <div class="riquadro">
      <midi-player id="lettore" src="data:audio/midi;base64,__MIDI__" sound-font></midi-player>
      <div class="stato" id="stato">Premi play: i campioni del flauto si caricano al primo ascolto.</div>
      <div class="scarica">
        <a href="__NOME__.musicxml" download>Partitura MusicXML (per MuseScore)</a>
        <a href="__NOME__.mid" download>File MIDI</a>
        <a href="__REPO__/tree/main/experiments/01-fuga-re-minore">Codice sorgente</a>
      </div>
    </div>
  </section>

  <section aria-labelledby="forma">
    <h2 id="forma">Forma</h2>
    <div class="riquadro">
      <div class="linea-tempo" id="linea-tempo" role="list"></div>
      <ul class="legenda" id="legenda"></ul>
    </div>
  </section>

  <section aria-labelledby="titolo-partitura">
    <h2 id="titolo-partitura">Partitura</h2>
    <div class="riquadro"><div id="partitura"><p class="attesa">Caricamento della partitura…</p></div></div>
  </section>

  <footer>
    Generata da <code>componi.py</code> e controllata da <code>verifica.py</code> nel repository
    <a href="__REPO__">ars-algorithmica</a>. Codice MIT, musica CC BY 4.0.
  </footer>
</main>

<script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
<script src="https://cdn.jsdelivr.net/npm/opensheetmusicdisplay@1.8.9/build/opensheetmusicdisplay.min.js"></script>
<script>
const SEZIONI = __SEZIONI__;
const SECONDI_PER_BATTUTA = __SPB__;
const PARTITURA = __XML__;

const lettore = document.getElementById('lettore');
const stato = document.getElementById('stato');
const linea = document.getElementById('linea-tempo');
const legenda = document.getElementById('legenda');
const totale = SEZIONI[SEZIONI.length - 1].ultima;

function tipo(nome) {
  if (/Stretti/.test(nome)) return 'stretto';
  if (/Pedale|Coda|Codetta/.test(nome)) return 'pedale';
  if (/Episodio/.test(nome)) return 'episodio';
  return 'tema';
}

function vaiA(sezione) {
  try {
    lettore.currentTime = (sezione.prima - 1) * SECONDI_PER_BATTUTA;
    if (!lettore.playing) lettore.start();
  } catch (e) { /* il lettore non è ancora pronto */ }
  evidenzia(sezione.prima);
}

SEZIONI.forEach((s, i) => {
  const n = s.ultima - s.prima + 1;
  const b = document.createElement('button');
  b.dataset.tipo = tipo(s.nome);
  b.style.flex = n;
  b.title = `${s.nome}, bb.${s.prima}-${s.ultima}`;
  b.textContent = n >= 6 ? s.nome : '';
  b.setAttribute('role', 'listitem');
  b.addEventListener('click', () => vaiA(s));
  linea.appendChild(b);
  const li = document.createElement('li');
  li.innerHTML = `<span class="battute">bb.${s.prima}-${s.ultima}</span>` +
    `<span><span class="nome">${s.nome}</span> · ${s.tonalita}<span class="descr">${s.descrizione}</span></span>`;
  li.addEventListener('click', () => vaiA(s));
  legenda.appendChild(li);
});

function evidenzia(battuta) {
  const i = SEZIONI.findIndex(s => battuta >= s.prima && battuta <= s.ultima);
  [...linea.children].forEach((el, k) => el.classList.toggle('attiva', k === i));
  [...legenda.children].forEach((el, k) => el.classList.toggle('attiva', k === i));
  if (i >= 0) stato.innerHTML = `Battuta <strong>${battuta}</strong> di ${totale} · <strong>${SEZIONI[i].nome}</strong> (${SEZIONI[i].tonalita})`;
}

lettore.addEventListener('note', () => evidenzia(Math.min(totale, Math.floor(lettore.currentTime / SECONDI_PER_BATTUTA) + 1)));
lettore.addEventListener('stop', () => { [...linea.children, ...legenda.children].forEach(el => el.classList.remove('attiva')); });

const osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay('partitura', {
  autoResize: true, backend: 'svg', drawTitle: false, drawSubtitle: false, drawComposer: false,
  drawPartNames: true, drawMeasureNumbers: true,
});
osmd.load(PARTITURA).then(() => { osmd.zoom = window.innerWidth < 700 ? 0.6 : 0.85; osmd.render(); })
  .catch(e => { document.getElementById('partitura').textContent = 'Impossibile mostrare la partitura: ' + e; });
</script>
</body>
</html>
"""


def scrivi_anteprima(cartella: Path, nome: str, sezioni: list[Sezione], file_html: str) -> Path:
    """Scrive la pagina HTML con MusicXML e MIDI incorporati."""
    xml = (cartella / f'{nome}.musicxml').read_text(encoding='utf-8')
    midi = base64.b64encode((cartella / f'{nome}.mid').read_bytes()).decode('ascii')
    dati_sezioni = [dict(nome=s.nome, prima=s.prima, ultima=s.ultima, tonalita=s.tonalita,
                         descrizione=s.descrizione) for s in sezioni]

    def js(valore) -> str:  # JSON sicuro dentro <script>
        return json.dumps(valore, ensure_ascii=False).replace('</', '<\\/')

    pagina = (_MODELLO
              .replace('__TITOLO__', TITOLO_PAGINA)
              .replace('__BATTUTE__', str(sezioni[-1].ultima))
              .replace('__NOME__', nome)
              .replace('__REPO__', REPO)
              .replace('__SPB__', str(SECONDI_PER_BATTUTA))
              .replace('__SEZIONI__', js(dati_sezioni))
              .replace('__MIDI__', midi)
              .replace('__XML__', js(xml)))
    percorso = cartella / file_html
    percorso.write_text(pagina, encoding='utf-8')
    return percorso
