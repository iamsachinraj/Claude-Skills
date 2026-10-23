#!/usr/bin/env python3
"""Build a single-file portfolio website from content.json and a photo.

Usage:
    python3 build.py --content content.json --photo headshot.jpg --out portfolio.html

The photo is optional; without one the portrait shows the person's initials.
The output is one self-contained HTML file (photo embedded) that can be
published as an artifact or hosted anywhere (GitHub Pages, Netlify, etc.).
"""
import argparse
import base64
import html
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")

ICONS = {
    "mail", "phone", "linkedin", "sun", "moon", "sparkles", "users", "layers", "clock",
    "heart", "trending", "pen", "down", "up", "compass", "zap", "handshake", "bot", "star",
    "target", "pointer", "route", "award", "cap", "book", "send", "copy", "check", "arrow",
    "chevron", "calendar", "pin", "alert", "tool", "flag", "globe", "rocket", "building", "sliders",
}


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def validate(d):
    """Return a list of warnings; exit on problems that would break the page."""
    warn = []
    p = d.get("person") or {}
    if not p.get("firstName"):
        fail("person.firstName is required")
    if not (d.get("hero") or {}).get("intro"):
        fail("hero.intro is required")
    roles = (d.get("career") or {}).get("roles") or []
    if not roles:
        fail("career.roles needs at least one role")
    ids = set()
    for r in roles:
        rid = r.get("id")
        if not rid:
            fail("every career role needs an id (e.g. 'acme-lead')")
        if rid in ids:
            fail("duplicate career role id: " + rid)
        ids.add(rid)
        for k in ("title", "company", "years"):
            if not r.get(k):
                warn.append("role %s is missing '%s'" % (rid, k))
    for cl in d.get("skills") or []:
        for it in cl.get("items") or []:
            bad = [x for x in it.get("roles") or [] if x not in ids]
            if bad:
                warn.append("skill '%s' points to unknown role ids %s (they will be ignored)" % (it.get("name"), bad))
            if not set(it.get("roles") or []) & ids:
                warn.append("skill '%s' has no valid roles and will be hidden" % it.get("name"))

    def check_icon(where, name):
        if name and name not in ICONS:
            warn.append("%s uses unknown icon '%s' (falls back to a star)" % (where, name))

    for b in (d.get("hero") or {}).get("badges") or []:
        check_icon("hero badge", b.get("icon"))
    for s in d.get("stats") or []:
        check_icon("stat", s.get("icon"))
    for pl in (d.get("leadership") or {}).get("pillars") or []:
        check_icon("pillar", pl.get("icon"))
    for c in (d.get("work") or {}).get("cases") or []:
        check_icon("case", c.get("icon"))
    for cl in d.get("skills") or []:
        check_icon("skill cluster", cl.get("icon"))
    for t in (d.get("toolkit") or {}).get("tools") or []:
        check_icon("tool", t.get("icon"))
    if len(d.get("stats") or []) > 5:
        warn.append("only the first 5 stats are shown")
    if len((d.get("leadership") or {}).get("pillars") or []) > 4:
        warn.append("only the first 4 pillars are shown")
    c = d.get("contact") or {}
    if not (c.get("email") or c.get("linkedin") or c.get("phone")):
        warn.append("no contact details: the contact section will be empty")
    return warn


def photo_data_uri(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        from PIL import Image, ImageOps
        im = Image.open(io.BytesIO(raw))
        im = ImageOps.exif_transpose(im).convert("RGB")
        w, h = im.size
        side = min(w, h)
        # square crop, biased slightly upward so faces sit well in a circle
        left = (w - side) // 2
        top = max(0, min(h - side, int((h - side) * 0.35)))
        im = im.crop((left, top, left + side, top + side)).resize((720, 720), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=84, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        ext = os.path.splitext(path)[1].lower().lstrip(".") or "jpeg"
        mime = "image/" + ("jpeg" if ext in ("jpg", "jpeg") else ext)
        if len(raw) > 2_500_000:
            print("WARNING: Pillow not installed and photo is large; page will load slowly. "
                  "Install it with: pip install pillow", file=sys.stderr)
        return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", required=True, help="path to content.json")
    ap.add_argument("--photo", help="path to a headshot (jpg/png)")
    ap.add_argument("--out", default="portfolio.html", help="output HTML path")
    a = ap.parse_args()

    try:
        with open(a.content, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        fail("content.json is not valid JSON: %s" % e)

    for w in validate(data):
        print("WARNING: " + w, file=sys.stderr)

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()

    p = data.get("person") or {}
    full = (p.get("firstName", "") + " " + p.get("lastName", "")).strip()
    meta = data.get("meta") or {}
    title = meta.get("title") or (full + (" | " + p["headline"] if p.get("headline") else ""))
    desc = meta.get("description") or (data.get("hero") or {}).get("intro", "")[:200]

    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    out = tpl.replace("/*__PORTFOLIO_DATA__*/null", blob, 1)
    out = out.replace('"/*__PHOTO__*/"', json.dumps(photo_data_uri(a.photo)) if a.photo else '""', 1)
    out = out.replace("__TITLE__", html.escape(title, quote=True))
    out = out.replace("__DESCRIPTION__", html.escape(desc, quote=True))

    with open(a.out, "w", encoding="utf-8") as f:
        f.write(out)
    print("Built %s (%.0f KB)" % (a.out, os.path.getsize(a.out) / 1024))


if __name__ == "__main__":
    main()
