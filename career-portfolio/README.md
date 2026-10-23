# Career Portfolio skill for Claude

Give Claude your **resume**, a **headshot** and your **LinkedIn URL**, and it
builds an interactive, animated portfolio website you can share on LinkedIn.

What the site includes:
- animated network background and letter-by-letter name reveal
- a typing line that cycles through everything you bring
- a leadership/approach section that lights up as you scroll
- case studies that stack like cards
- skills you can click to light up where you used them in your career
- an expandable career timeline, toolkit ticker and contact cards
- light and dark mode, mobile layout, reduced-motion support

The whole site is one HTML file with the photo embedded, so it can be hosted
anywhere.

## Install it

**Claude (web or desktop app)**
1. [Download career-portfolio.zip](https://github.com/iamsachinraj/Claude-Skills/raw/main/career-portfolio.zip). Don't unzip it.
2. In Claude, open Settings and find the Skills section.
3. Upload the zip.

Custom skills need code execution turned on in Claude's settings, and a plan that supports custom skills.

**Claude Code**
1. [Download career-portfolio.zip](https://github.com/iamsachinraj/Claude-Skills/raw/main/career-portfolio.zip) and unzip it.
2. Copy the `career-portfolio` folder into `~/.claude/skills/`.

## Use

Start a chat, attach your resume and photo, and say:

> Build my portfolio website. My LinkedIn is https://www.linkedin.com/in/your-name

Claude reads your resume, writes the site content, builds the page and gives
it back to you. Ask for any wording changes afterwards and it will rebuild.

## Share it

- If Claude published it as an artifact, share that link.
- Or host the HTML file for free on GitHub Pages or Netlify Drop.
- Add the link to the Featured section of your LinkedIn profile.

## Build without Claude

```bash
pip install pillow   # optional, crops and compresses the photo
python3 scripts/build.py --content examples/sample-content.json --photo me.jpg --out portfolio.html
```

`references/content-schema.md` documents every field.

## Privacy

Everything on the site is public once you share the link. Claude leaves your
phone number off unless you ask for it.
