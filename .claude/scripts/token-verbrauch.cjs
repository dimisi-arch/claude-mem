#!/usr/bin/env node
/*
Token-Verbrauch: liest die lokalen Claude-Code-Mitschriften und rechnet aus,
wofür Tokens verbraucht wurden.

Run:   node .claude/scripts/token-verbrauch.cjs [Ausgabe-Ordner]
Reads: ~/.claude/projects/<Projekt>/<Sitzung>.jsonl (nur lesend)
Writes (in den Ausgabe-Ordner, Standard: ./token-verbrauch):
  tage.json       je Tag: Anfragen und Tokens nach Art
  sitzungen.json  je Sitzung: Tokens, Grundlast, größter Kontext, Neuaufbauten
  werkzeuge.json  je Werkzeug: Aufrufe, Größe der Ergebnisse, mitgeschleppte Tokens

Nur Sitzungen, die auf diesem Rechner liefen, haben hier eine Mitschrift.
Tokens aus Zeichen sind geschätzt (Zeichen / 4). "Gewichtet" rechnet mit den
Preisverhältnissen der API: Ausgabe x5, Cache schreiben x2 (1 Std.) bzw. x1,25
(5 Min.), Cache lesen x0,1. Wie ein Abo die Arten gewichtet, ist nicht bekannt.
*/
const fs = require('fs');
const os = require('os');
const path = require('path');

const root = path.join(os.homedir(), '.claude', 'projects');
const out = path.resolve(process.argv[2] || 'token-verbrauch');
const W = { input: 1, output: 5, write1h: 2, write5m: 1.25, read: 0.1 };
const REBUILD_GAP_MIN = 5; // ab dieser Pause zählt ein großer Cache-Neuschrieb als Neuaufbau

const berlinDay = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Berlin' });
const berlinTime = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Berlin', dateStyle: 'short', timeStyle: 'short' });
const est = (chars) => Math.round(chars / 4);

function sizeOf(content) {
  if (content == null) return 0;
  if (typeof content === 'string') return content.length;
  if (Array.isArray(content)) return content.reduce((s, b) => s + sizeOf(b && (b.text != null ? b.text : b.content != null ? b.content : b.type === 'image' ? '' : JSON.stringify(b))), 0);
  return JSON.stringify(content).length;
}
function group(name) {
  let m = /^mcp__claude_ai_(.+?)__/.exec(name);
  if (m) return 'Connector ' + m[1].replace(/_/g, ' ');
  m = /^mcp__(.+?)__/.exec(name);
  if (m) return 'Connector ' + m[1];
  return 'Eingebaut';
}
function shortName(name) {
  return name.replace(/^mcp__claude_ai_.+?__/, '').replace(/^mcp__.+?__/, '');
}
function firstLine(s) {
  const line = String(s).split(/\r?\n/).map((x) => x.trim()).find((x) => x && !x.startsWith('<')) || '';
  return line.length > 70 ? line.slice(0, 69) + '…' : line;
}

const sessions = [];
const tools = new Map();

for (const project of fs.existsSync(root) ? fs.readdirSync(root) : []) {
  const dir = path.join(root, project);
  if (!fs.statSync(dir).isDirectory()) continue;
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.jsonl'))) {
    const text = fs.readFileSync(path.join(dir, file), 'utf8');
    if (!text.trim()) continue;
    const requests = new Map(); // message.id -> {t, usage, model}
    const toolById = new Map(); // tool_use_id -> {name, reqIndex}
    const results = []; // {name, tokens, reqIndex}
    let topic = '';
    let prompts = 0;
    let cwd = '';
    for (const line of text.split('\n')) {
      if (!line.trim()) continue;
      let o;
      try { o = JSON.parse(line); } catch { continue; }
      if (o.cwd) cwd = o.cwd;
      if (o.type === 'assistant' && o.message && o.message.usage) {
        const id = o.message.id || o.uuid;
        const seen = requests.get(id);
        if (!seen) requests.set(id, { t: o.timestamp, usage: o.message.usage, model: o.message.model, side: !!o.isSidechain });
        else if ((o.message.usage.output_tokens || 0) >= (seen.usage.output_tokens || 0)) seen.usage = o.message.usage;
        for (const b of Array.isArray(o.message.content) ? o.message.content : []) {
          if (b.type === 'tool_use') toolById.set(b.id, { name: b.name, reqIndex: requests.size - 1 });
        }
      } else if (o.type === 'user' && o.message) {
        const c = o.message.content;
        const blocks = Array.isArray(c) ? c : [];
        const toolResults = blocks.filter((b) => b.type === 'tool_result');
        for (const b of toolResults) {
          const use = toolById.get(b.tool_use_id);
          if (use) results.push({ name: use.name, tokens: est(sizeOf(b.content)), reqIndex: requests.size });
        }
        if (!toolResults.length && !o.isMeta && !o.isSidechain) {
          const said = typeof c === 'string' ? c : blocks.filter((b) => b.type === 'text').map((b) => b.text).join('\n');
          const line1 = firstLine(said);
          if (line1) { prompts += 1; if (!topic) topic = line1; }
        }
      }
    }
    const reqs = [...requests.values()].filter((r) => r.t).sort((a, b) => a.t.localeCompare(b.t));
    if (!reqs.length) continue;

    const s = { Sitzung: file.slice(0, 8), Thema: topic || '(ohne Text)', Projekt: path.basename(cwd || project), Start: '', Tag: '', Dauer_Min: 0, Modell: '', Anfragen: reqs.length, Prompts: prompts,
      Eingabe: 0, Ausgabe: 0, Cache_schreiben: 0, Cache_lesen: 0, Gesamt: 0, Gewichtet: 0, Startkontext: 0, Maxkontext: 0, Grundlast: 0, Neuaufbauten: 0, Neuaufbau_Tokens: 0, days: new Map() };
    const models = {};
    let prev = null;
    reqs.forEach((r, i) => {
      const u = r.usage;
      const inp = u.input_tokens || 0, outp = u.output_tokens || 0, cw = u.cache_creation_input_tokens || 0, cr = u.cache_read_input_tokens || 0;
      const cw1h = u.cache_creation && u.cache_creation.ephemeral_1h_input_tokens != null ? u.cache_creation.ephemeral_1h_input_tokens : cw;
      const cw5m = cw - cw1h;
      const weighted = inp * W.input + outp * W.output + cw1h * W.write1h + cw5m * W.write5m + cr * W.read;
      const context = inp + cw + cr;
      s.Eingabe += inp; s.Ausgabe += outp; s.Cache_schreiben += cw; s.Cache_lesen += cr; s.Gewichtet += weighted;
      if (i === 0) s.Startkontext = context;
      if (context > s.Maxkontext) s.Maxkontext = context;
      const gap = prev ? (new Date(r.t) - new Date(prev.t)) / 60000 : 0;
      if (i > 0 && gap >= REBUILD_GAP_MIN && cw > 0.5 * context && cw > 20000) { s.Neuaufbauten += 1; s.Neuaufbau_Tokens += cw; }
      models[r.model] = (models[r.model] || 0) + 1;
      const day = berlinDay.format(new Date(r.t));
      const d = s.days.get(day) || { Tag: day, Anfragen: 0, Eingabe: 0, Ausgabe: 0, Cache_schreiben: 0, Cache_lesen: 0, Gewichtet: 0 };
      d.Anfragen += 1; d.Eingabe += inp; d.Ausgabe += outp; d.Cache_schreiben += cw; d.Cache_lesen += cr; d.Gewichtet += weighted;
      s.days.set(day, d);
      prev = r;
    });
    s.Gesamt = s.Eingabe + s.Ausgabe + s.Cache_schreiben + s.Cache_lesen;
    s.Gewichtet = Math.round(s.Gewichtet);
    s.Grundlast = Math.min(s.Startkontext * s.Anfragen, s.Eingabe + s.Cache_schreiben + s.Cache_lesen);
    s.Start = berlinTime.format(new Date(reqs[0].t));
    s.Tag = berlinDay.format(new Date(reqs[0].t));
    s.Dauer_Min = Math.round((new Date(reqs[reqs.length - 1].t) - new Date(reqs[0].t)) / 60000);
    s.Modell = Object.keys(models).sort((a, b) => models[b] - models[a])[0] || '';
    sessions.push(s);

    for (const r of results) {
      const t = tools.get(r.name) || { Werkzeug: shortName(r.name), Gruppe: group(r.name), Aufrufe: 0, Ergebnis_Tokens: 0, Groesstes_Ergebnis: 0, Mitgeschleppt: 0 };
      t.Aufrufe += 1;
      t.Ergebnis_Tokens += r.tokens;
      if (r.tokens > t.Groesstes_Ergebnis) t.Groesstes_Ergebnis = r.tokens;
      t.Mitgeschleppt += r.tokens * Math.max(0, reqs.length - r.reqIndex - 1);
      tools.set(r.name, t);
    }
  }
}

const days = new Map();
for (const s of sessions) {
  for (const d of s.days.values()) {
    const a = days.get(d.Tag) || { Tag: d.Tag, Sitzungen: 0, Anfragen: 0, Eingabe: 0, Ausgabe: 0, Cache_schreiben: 0, Cache_lesen: 0, Gesamt: 0, Gewichtet: 0 };
    a.Sitzungen += 1; a.Anfragen += d.Anfragen; a.Eingabe += d.Eingabe; a.Ausgabe += d.Ausgabe; a.Cache_schreiben += d.Cache_schreiben; a.Cache_lesen += d.Cache_lesen; a.Gewichtet += d.Gewichtet;
    days.set(d.Tag, a);
  }
  delete s.days;
}
const dayRows = [...days.values()].sort((a, b) => a.Tag.localeCompare(b.Tag)).map((d) => ({ ...d, Gesamt: d.Eingabe + d.Ausgabe + d.Cache_schreiben + d.Cache_lesen, Gewichtet: Math.round(d.Gewichtet) }));
const sessionRows = sessions.sort((a, b) => b.Gewichtet - a.Gewichtet);
const toolRows = [...tools.values()].sort((a, b) => (b.Ergebnis_Tokens + b.Mitgeschleppt * W.read) - (a.Ergebnis_Tokens + a.Mitgeschleppt * W.read));

fs.mkdirSync(out, { recursive: true });
const write = (name, rows) => fs.writeFileSync(path.join(out, name), JSON.stringify(rows, null, 1));
write('tage.json', dayRows);
write('sitzungen.json', sessionRows);
write('werkzeuge.json', toolRows);

const sum = (rows, k) => rows.reduce((t, r) => t + r[k], 0);
const n = (x) => Math.round(x).toLocaleString('de-DE');
console.log(`Sitzungen: ${sessionRows.length}   Anfragen: ${n(sum(sessionRows, 'Anfragen'))}   Tage: ${dayRows.length}`);
console.log(`Eingabe ${n(sum(sessionRows, 'Eingabe'))} · Ausgabe ${n(sum(sessionRows, 'Ausgabe'))} · Cache schreiben ${n(sum(sessionRows, 'Cache_schreiben'))} · Cache lesen ${n(sum(sessionRows, 'Cache_lesen'))}`);
console.log(`Gewichtet: ${n(sum(sessionRows, 'Gewichtet'))}   davon Grundlast (Startkontext x Anfragen): ${n(sum(sessionRows, 'Grundlast'))} Tokens im Kontext`);
console.log(`Ausgabe nach: ${out}`);
