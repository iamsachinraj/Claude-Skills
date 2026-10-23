---
name: career-portfolio
description: Turn someone's resume, headshot and LinkedIn URL into an interactive, animated personal portfolio website (single HTML file) they can share on LinkedIn. Use when someone asks for a portfolio site, personal website, career website, interactive resume or "website from my resume", or attaches a resume and photo asking for a site.
---

# Career portfolio website

Builds a polished one-page portfolio from three inputs: a **resume**, a
**professional photo** and a **LinkedIn profile URL**. The design is fixed
and already finished (animated network background, letter-by-letter name,
typing roles, stacking case-study cards, clickable skills that light up a
career timeline, light and dark mode, mobile layout). Your job is the
**content**: read the resume, write one `content.json`, run the build script.

Files in this skill:
- `assets/template.html`: the finished design; do not edit it for normal use
- `scripts/build.py`: merges `content.json` and the photo into one HTML file
- `references/content-schema.md`: every field, length guide and icon name
- `examples/sample-content.json`: a complete working example

## 1. Collect the three inputs

Ask once, together, for whatever is missing:
1. **Resume**: any format (PDF, DOCX, text, pasted). Required.
2. **Photo**: a well-lit, front-facing headshot. Optional; without one the
   portrait shows their initials.
3. **LinkedIn URL**: used for the contact links.

Don't request anything else up front. LinkedIn pages usually block automated
reading, so treat the URL as a link, not a data source; the resume is the
source of truth. If you can read the profile and it adds facts, use them.

## 2. Read the resume and find the persona

Read the whole resume. Then, before writing anything, decide on the
**combined persona**: one identity that holds every major hat the person
has worn, not just their latest job title. Example: "customer success
leader who designs onboarding, runs CS operations on data, and builds
engaged teams", rather than "Head of CS". People rarely want a site about
one role; they want the through-line of their career.

Pick out:
- the 4–8 identities they bring (these become the typing line)
- the constant thread across roles (becomes the leadership headline and
  pillars)
- 3–5 stories with a clear problem, action and result (case studies)
- every stated number (stats, gauge, highlights)
- tools, platforms, certifications, education

## 3. Write content.json

Follow `references/content-schema.md`; mirror the shape of
`examples/sample-content.json`. Rules:

- **Only facts from the resume.** Never invent metrics, employers, dates,
  team sizes or results. If a case study has no stated result, describe the
  outcome qualitatively. Use the gauge only for a real stated percentage.
- **First person, plain and confident.** Short sentences, no buzzword
  stacking, no "passionate", "results-driven" or "dynamic".
- **Respect the length guides**; long text breaks the layout's rhythm.
- **Skills must point at real role ids**, and each skill should map to every
  role where the resume shows it.
- Order career roles newest first; mark the present role `current: true`.
- Leave `contact.phone` empty unless the person says to include it.

Save it as `content.json` in the working directory.

## 4. Build

```bash
python3 <skill-dir>/scripts/build.py --content content.json --photo <photo-path> --out portfolio.html
```

Pillow (`pip install pillow`) crops and compresses the photo; without it the
photo is embedded as-is. Fix every `ERROR`; read each `WARNING` and fix it
unless it's intentional.

## 5. Check it

If you can open a browser or take screenshots, look at the hero on desktop
and phone widths, scroll the whole page once, and toggle dark mode. Check
that the photo crop shows the face (adjust `person.photoPosition`) and that
no text overflows. Otherwise, re-read content.json against the length guides.

## 6. Deliver

- If you can publish an artifact or web page, publish `portfolio.html`
  privately and give them the link, explaining they choose when to share it.
- Otherwise, send them the file.

Then tell them, briefly:
- what persona you built the site around, so they can redirect it
- that they can ask for any copy change and you'll rebuild
- how to share it: publish/share the artifact link, or host the single
  file free on GitHub Pages or Netlify Drop, then add the link to the
  Featured section of their LinkedIn profile

## Edits

For copy changes, edit `content.json` and rebuild; never hand-edit the
built HTML. Design changes (colours, fonts, sections) go in
`assets/template.html`; keep the `/*__PORTFOLIO_DATA__*/null`,
`"/*__PHOTO__*/"`, `__TITLE__` and `__DESCRIPTION__` placeholders intact.
