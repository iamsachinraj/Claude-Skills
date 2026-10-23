# content.json reference

`scripts/build.py` turns one `content.json` into the finished site. Every
visible word on the page comes from this file. `examples/sample-content.json`
is a complete, working example; copy its shape.

All text is plain text (HTML is escaped). The one formatting feature is in
`leadership.headline`, where `[[...]]` marks the phrase that lights up gold.

## Top level

| Key | Required | What it drives |
|---|---|---|
| `meta` | no | Browser tab title and link-preview description |
| `person` | yes | Name, initials, location |
| `contact` | yes | Header icon buttons and the contact cards |
| `hero` | yes | First screen: pill, name, typing line, intro, photo badges |
| `stats` | yes | Up to 5 tiles under the hero |
| `leadership` | yes | Dark/light band: headline, optional gauge, up to 4 pillars |
| `work` | no | Stacking case-study cards (section hides if empty) |
| `career` | yes | Expandable timeline |
| `skills` | no | Clickable skill chips that light up timeline roles |
| `toolkit` | no | Scrolling tool ticker plus credential cards |
| `contactSection` | no | Contact headline and line |

## Fields

**meta**: `title`, `description` (~150 characters).

**person**: `firstName` (required), `lastName`, `initials` (defaults to
first letters), `headline` (short professional title), `location`,
`photoPosition` (CSS object-position for the photo, default `"50% 38%"`;
lower the second number to move the crop up toward the face).

**contact**: `email`, `phone`, `linkedin` (full URL). Leave any as `""` to
hide it. Ask before including a phone number; the site is public.

**hero**
- `pill`: 3–6 words, e.g. `"Customer success leader, Pune"`
- `typedLead`: words before the typed phrase, default `"I bring"`
- `roles`: 4–8 short lowercase phrases that complete the sentence
  (`"I bring" + "onboarding design"`). Keep each under ~32 characters.
- `intro`: 2–3 sentences, first person, the combined persona
- `badges`: exactly 3 `{icon, text}` floating around the photo, each under
  ~24 characters

**stats**: 3–5 tiles. Each is either a number tile
`{icon, value: 13, suffix: "+", label}` (the number counts up) or a word tile
`{icon, title: "Team builder", label}`. Mix both kinds; only use numbers the
resume states.

**leadership**
- `navLabel`: menu name for this section, default `"Leadership"`
  (use `"Approach"` for individual contributors)
- `kicker`: small label, e.g. `"What stays constant"`
- `headline`: 1–2 sentences, under ~200 characters, with one `[[phrase]]`
- `lede`: one sentence
- `gauge` (optional): `{value: 0-100, suffix: "%", label}`. Only for a real
  percentage the person stated (engagement, CSAT, retention). Omit otherwise.
- `pillars`: 4 `{icon, title, text}`; titles 1–3 words, text 1–2 sentences

**work.cases**: 3–5 items, strongest first (the first card is styled as the
feature). Each: `icon`, `where` (`"As <hat>, <Company>, <years>"`), `title`,
`problem`, `action`, `result`. One or two sentences each.

**career**
- `kicker` (e.g. `"2014 to today"`), `title`, `lede`
- `roles`: newest first. Each role:
  - `id`: unique slug, e.g. `"acme-lead"` (skills refer to these)
  - `badge`: 2–4 letter company abbreviation
  - `title`, `company`, `years` (`"2020 to 2022"`, `"2022 to present"`)
  - `current: true` on the present role
  - `growth` (optional): a promotion story, e.g. `"Agent to lead in 2 years"`
  - `summary`: one sentence
  - `highlights`: 2–7 short achievements
  - `tags`: 2–6 short labels

**skills**: 3–4 clusters `{cluster, icon, items: [{name, roles: [role ids]}]}`.
Every skill must list the role ids where it was used; this powers the
"Skills, with the receipts" interaction. 3–6 items per cluster.

**toolkit**: `title`, `tools` (`[{name, icon}]`, 4–14 items),
`credentials` (`[{icon, title, detail}]`: certifications and education;
use `award` for certifications, `cap` for degrees, `book` for schooling).

**contactSection**: `title` (short, confident line), `lede`.

## Icons

Use only these names:

`mail phone linkedin sparkles users layers clock heart trending pen compass
zap handshake bot star target pointer route award cap book send check arrow
calendar pin alert tool flag globe rocket building sliders`

Good defaults: years → `clock`; people/teams → `users`; growth → `trending`;
AI → `sparkles` or `bot`; operations/process → `sliders`; partnership →
`handshake`; launches → `rocket`; global → `globe`; design/content → `pen`;
platforms → `layers`.
