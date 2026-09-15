# Luisa Spagnoli — Training Material FW 2026/2027

A mobile-first, bilingual (English default, Russian toggle) training app for retail staff, built from the uploaded spreadsheet of 273 models.

## What the app will do

**Home screen**
- Fixed header: LUISA SPAGNOLI in an elegant serif, subtitle "Training Material FW 2026/2027", and an EN | RU pill toggle on the right (choice remembered between visits).
- A searchable dropdown listing all 273 models alphabetically, plus a SEARCH / ПОИСК button in satin gold.

**Model sheet** (after choosing a model)
1. Title "ANALYSIS: [Model]" / "АНАЛИЗ: [Model]", ID badge, and a hero image taken from the first colour variant that has one.
2. Description in the selected language.
3. Colour variants: 2-column grid on phones, 3 on larger screens, gold-edged thumbnails that open full-screen when tapped. Variants with no image get a champagne placeholder card showing colour name and code.
4. Styling & combinations: each total look shown as clean text with every web address stripped out, followed by a row of cards for the garments named in that look (image, name, colour code). Tapping one jumps straight to that model's sheet when it exists in the data.
5. Sales advice: three numbered cards (01/02/03) with gold accents.
6. Objection handling: expandable cards, question on champagne, answer on cream with a gold left border. Text always shown in full, never cut off.

## Data handling

- The spreadsheet is converted once into a JSON file bundled with the app — no backend, instant loading, works offline after first visit.
- Colour field parsed from `Name (code): URL`; "URL non disponibile" becomes a placeholder card.
- Styling field split on `|` into looks; garment name + colour code + image captured from each `Name Code (url)` pattern; duplicate repeats, `(nan)`, empty brackets and stray links removed from the visible text.
- Sales advice split on `|`; objections split on `||` and on `[question] -> answer`.
- 60 rows have no English objection text and 13 have none at all: English view falls back to the Russian text for those rather than showing an empty section.
- Image links come from an external server; broken images fall back to the placeholder card instead of a broken icon.

## Design

- Background #FAF8F5, cards white with #E7E2DA borders, text #1C1917, accent gold #A37D45, champagne #F4F0EA.
- Playfair Display for headings, Inter for body, loaded properly for the build.
- All colours defined as reusable design tokens, not hardcoded per component.

## Technical notes

- TanStack Start + React + Tailwind v4 (the stack this project runs on), shadcn components for combobox, accordion, dialog, badge, tabs.
- Routes: `/` (picker) and `/model/$id` (sheet), so a model can be linked and shared directly; each has its own page title and description.
- A conversion script turns the Excel into `src/data/models.json` at build-prep time; the parsing helpers live in a shared module with unit-testable pure functions.
- Language state in React context, persisted to localStorage, defaulting to EN.

## One thing the data doesn't contain

The brief mentions a category badge (e.g. "Maglieria / Capispalla"), but the spreadsheet has no category column. I'll show only the ID badge unless you can supply categories.
