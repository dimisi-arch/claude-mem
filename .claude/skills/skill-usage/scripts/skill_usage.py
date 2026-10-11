#!/usr/bin/env python3
"""Count how often each skill was used and switch long-unused ones to name-only.

Reads the session transcripts Claude Code keeps on this machine
(~/.claude/projects/**/*.jsonl), prints a German report, and with --apply sets
`skillOverrides` entries in the project's .claude/settings.local.json.
Standard library only.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

CAP = 1536  # Claude Code truncates description + when_to_use at this length in the listing
MIN_SAVING = 60  # a description shorter than this is not worth switching
HOME = Path.home()
STATE_DIR = HOME / ".claude" / "skill-usage"
SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_REF = re.compile(r"skills[\\/]+([A-Za-z0-9_.-]+)")
RUNS_SCRIPT = re.compile(r"[\\/]scripts[\\/]")
SLASH = re.compile(r"<command-name>/?([\w:.-]+)</command-name>")
STAMP = re.compile(r'"timestamp":"([^"]+)"')


def berlin(dt):
    """UTC datetime -> Europe/Berlin wall time (EU summer-time rule, no tz database needed)."""
    def last_sunday(year, month):
        d = datetime(year, month, 31, 1, tzinfo=timezone.utc)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    summer = last_sunday(dt.year, 3) <= dt < last_sunday(dt.year, 10)
    return dt + timedelta(hours=2 if summer else 1)


def parse_ts(text):
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def frontmatter(text):
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n", text, re.S)
    out, key = {}, None
    for line in (m.group(1).splitlines() if m else []):
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top:
            key, val = top.group(1), top.group(2).strip()
            out[key] = "" if val in (">", "|", ">-", "|-", ">+", "|+") else val.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def installed(project):
    """Skills on disk: {name: {'desc': chars, 'body': chars, 'where': label}}."""
    skills = {}
    for root, where in ((HOME / ".claude" / "skills", "Benutzer"), (project / ".claude" / "skills", "Projekt")):
        for path in sorted(root.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            fm = frontmatter(text)
            desc = (fm.get("description", "") + " " + fm.get("when_to_use", "")).strip()
            skills[fm.get("name") or path.parent.name] = {
                "desc": min(len(desc), CAP), "body": len(text), "where": where}
    return skills


def scan(since):
    """Return (events, sessions_active, data_start). An event is (skill, utc time, kind)."""
    events, seen_ids, sessions, data_start = [], set(), 0, None
    for path in (HOME / ".claude" / "projects").rglob("*.jsonl"):
        first = None
        try:
            active = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= since
            with path.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if first is None:
                        m = STAMP.search(line)
                        first = parse_ts(m.group(1)) if m else None
                    if not active:
                        if first:
                            break
                        continue
                    if '"Skill"' not in line and "command-name" not in line and "scripts" not in line:
                        continue
                    try:
                        entry = json.loads(line)
                    except ValueError:
                        continue
                    ts = parse_ts(entry.get("timestamp", ""))
                    content = (entry.get("message") or {}).get("content")
                    if ts is None or ts < since:
                        continue
                    if isinstance(content, str):
                        content = [{"type": "text", "text": content}]
                    for item in content or []:
                        if not isinstance(item, dict):
                            continue
                        if item.get("type") == "text" and entry.get("type") == "user":
                            events += [(name, ts, "call") for name in SLASH.findall(item.get("text", ""))]
                        if item.get("type") != "tool_use" or item.get("id") in seen_ids:
                            continue
                        seen_ids.add(item.get("id"))
                        tool, args = item.get("name"), item.get("input") or {}
                        if tool == "Skill" and args.get("skill"):
                            events.append((args["skill"], ts, "call"))
                        elif tool in ("Bash", "PowerShell"):
                            # a skill folder named in a command that also runs something under scripts/
                            command = str(args.get("command", ""))
                            if RUNS_SCRIPT.search(command):
                                events += [(n, ts, "script") for n in set(SKILL_REF.findall(command))]
        except OSError:
            continue
        if first:
            data_start = min(data_start, first) if data_start else first
        if active and "subagents" not in path.parts:
            sessions += 1
    return events, sessions, data_start


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def overrides(project):
    """Effective skillOverrides, later files win: user, project, local."""
    merged = {}
    for path in (HOME / ".claude" / "settings.json", project / ".claude" / "settings.json",
                 project / ".claude" / "settings.local.json"):
        merged.update(load_json(path, {}).get("skillOverrides") or {})
    return merged


def protected():
    names = {SKILL_DIR.name}
    for line in (SKILL_DIR / "protected.txt").read_text(encoding="utf-8").splitlines():
        name = line.split("#")[0].strip()
        if name:
            names.add(name)
    return names


def tokens(chars):
    return round(chars / 4)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="report window in days (default 7)")
    ap.add_argument("--idle-days", type=int, default=14, help="unused for this long -> name-only (default 14)")
    ap.add_argument("--project", default=".", help="project root holding .claude/ (default: current directory)")
    ap.add_argument("--apply", action="store_true", help="write the switches; without it only the plan is shown")
    ap.add_argument("--daily", action="store_true", help="do nothing if --apply already ran today (for the start hook)")
    ap.add_argument("--quiet", action="store_true", help="print only switches that were made")
    opt = ap.parse_args()

    project = Path(opt.project).resolve()
    now = datetime.now(timezone.utc)
    today = berlin(now).date().isoformat()
    state = load_json(STATE_DIR / "state.json", {})
    state.setdefault("first_seen", {}), state.setdefault("managed", {}), state.setdefault("log", [])
    if opt.daily and state.get("last_apply") == today:
        return

    skills = installed(project)
    for name in skills:
        state["first_seen"].setdefault(name, today)
    events, sessions, data_start = scan(now - timedelta(days=max(opt.days, opt.idle_days)))
    window = now - timedelta(days=opt.days)
    span_days = (now - data_start).days if data_start else 0
    status = overrides(project)
    keep = protected()

    def bare(name):
        return name if name in skills else name.split(":")[-1]

    stats = defaultdict(lambda: {"call": 0, "script": 0, "days": set(), "last": None})
    last_any = {}
    for name, ts, kind in events:
        key = bare(name) if bare(name) in skills else name
        last_any[key] = max(last_any.get(key, ts), ts)
        if ts >= window:
            s = stats[key]
            s[kind] += 1
            s["days"].add(berlin(ts).date())
            s["last"] = max(s["last"] or ts, ts)

    # --- switch plan -------------------------------------------------------
    plan = []
    for name, info in skills.items():
        managed = state["managed"].get(name)
        used = last_any.get(name)
        if managed and used and berlin(used).date().isoformat() >= managed["since"]:
            plan.append((name, "on", "wieder benutzt am " + berlin(used).strftime("%d.%m.")))
        elif (not managed and name not in keep and status.get(name, "on") == "on" and info["desc"] >= MIN_SAVING
              and span_days >= opt.idle_days and used is None
              and state["first_seen"][name] <= (berlin(now) - timedelta(days=opt.idle_days)).date().isoformat()):
            plan.append((name, "name-only", f"seit {opt.idle_days} Tagen nicht benutzt"))

    if opt.apply:
        local = project / ".claude" / "settings.local.json"
        settings = load_json(local, {})
        table = settings.get("skillOverrides") or {}
        for name, target, reason in plan:
            if target == "on":
                table.pop(name, None)
                state["managed"].pop(name, None)
            else:
                table[name] = target
                state["managed"][name] = {"since": today}
            state["log"].append({"date": today, "skill": name, "to": target, "reason": reason})
        if plan:
            if table:
                settings["skillOverrides"] = table
            else:
                settings.pop("skillOverrides", None)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            status = overrides(project)
        state["last_apply"] = today
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if opt.quiet:
        if opt.apply and plan:
            print("skill-usage: " + "; ".join(f"{n} -> {'an' if t == 'on' else 'nur Name'} ({r})" for n, t, r in plan))
        return

    # --- report ------------------------------------------------------------
    label = {"on": "an", "name-only": "nur Name", "user-invocable-only": "nur per /Befehl", "off": "aus"}
    out = [f"# Skill-Nutzung, letzte {opt.days} Tage (Stand {berlin(now).strftime('%d.%m.%Y %H:%M')} Uhr)", ""]
    if data_start:
        out.append(f"Datenbasis: Sitzungen auf diesem Rechner seit {berlin(data_start).strftime('%d.%m.%Y')} "
                   f"({span_days} Tage), {sessions} Sitzungen mit Aktivität im Zeitraum. "
                   "Cloud-Sitzungen sind nicht enthalten.")
    else:
        out.append("Keine Sitzungsprotokolle auf diesem Rechner gefunden: Die Zählung ist leer, es wird nichts geschaltet.")
    out += ["", "## Benutzt", "", "| Skill | Aufrufe | Skript-Läufe | an Tagen | zuletzt | Kosten je Aufruf | Status |",
            "|---|---:|---:|---:|---|---:|---|"]
    week_cost = 0
    for name, s in sorted(stats.items(), key=lambda kv: (-(kv[1]["call"] + kv[1]["script"]), kv[0])):
        info = skills.get(name)
        per_call = tokens(info["body"]) if info else None
        week_cost += (per_call or 0) * s["call"]
        out.append(f"| {name} | {s['call']} | {s['script']} | {len(s['days'])} | "
                   f"{berlin(s['last']).strftime('%d.%m. %H:%M')} | "
                   f"{'≈ ' + format(per_call, ',').replace(',', '.') if per_call else 'mitgeliefert'} | "
                   f"{label.get(status.get(name, 'on'), status.get(name)) if info else 'nicht schaltbar'} |")
    if not stats:
        out.append("| (keiner) | | | | | | |")

    unused = [n for n in skills if n not in stats]
    listing = sum(len(n) + (i["desc"] if status.get(n, "on") == "on" else 0)
                  for n, i in skills.items() if status.get(n, "on") in ("on", "name-only"))
    out += ["", f"## Nicht benutzt in {opt.days} Tagen ({len(unused)} von {len(skills)})", "",
            "| Skill | Platz in der Liste | Status | geschützt |", "|---|---:|---|---|"]
    for name in sorted(unused, key=lambda n: -skills[n]["desc"]):
        st = status.get(name, "on")
        out.append(f"| {name} | ≈ {tokens(len(name) + (skills[name]['desc'] if st == 'on' else 0))} | "
                   f"{label.get(st, st)} | {'ja' if name in keep else ''} |")

    out += ["", "## Kosten (grobe Schätzung: 4 Zeichen ≈ 1 Token)", "",
            f"- Skill-Liste der {len(skills)} eigenen Skills: ≈ {tokens(listing):,} Tokens je Sitzung".replace(",", "."),
            f"- Geladene Skill-Texte im Zeitraum: ≈ {week_cost:,} Tokens".replace(",", "."), "",
            "## Schaltungen", ""]
    if plan:
        verb = "Geschaltet" if opt.apply else "Geplant (noch nicht geschaltet)"
        out += [f"- {verb}: {n} -> {label[t]} ({r})" for n, t, r in plan]
    elif span_days < opt.idle_days:
        out.append(f"- Keine. Geschaltet wird erst, wenn {opt.idle_days} Tage Verlauf vorliegen "
                   f"(bisher {span_days}).")
    else:
        out.append("- Keine nötig.")
    managed_now = sorted(state["managed"])
    if managed_now:
        out.append("- Von diesem Skill auf „nur Name“ gesetzt: " + ", ".join(managed_now))
    text = "\n".join(out) + "\n"
    (STATE_DIR / "report.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
