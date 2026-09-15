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

- The spreadsheet is converted once into a JSON file bundled with the app — no backend, instant loading, works offline after first visit. (The two model files you sent are identical, so one is used.)
- **Correct image for every cited model:** the second file `url.xlsx` (837 rows of `Model (colour code)` to image address) becomes the single source of truth. Every garment mentioned in a styling look is matched to that list by model name + colour code and shown with the matching picture, instead of trusting the addresses embedded in the styling text (which are frequently duplicated or attached to the wrong garment).
- Matching is case- and spacing-insensitive and handles multi-code entries like `Niccioleta (0906 0002)`; if the exact code isn't listed, the app falls back to another colour of the same model, and only then to a placeholder. 70 rows in the list have no address — those show the placeholder.
- A build-time report lists any cited garment that could not be matched, so gaps are visible rather than silent.
- Colour field parsed from `Name (code): URL`; also cross-checked against `url.xlsx`, with "URL non disponibile" resolved from the list when possible, otherwise a placeholder card.
- Styling field split on `|` into looks; garment name + colour code captured from each `Name Code (...)` pattern; duplicate repeats, `(nan)`, empty brackets and all raw links removed from the visible text.
- Sales advice split on `|`; objections split on `||` and on `[question] -> answer`.
- 60 rows have no English objection text and 13 have none at all: English view falls back to the Russian text for those rather than showing an empty section.
- Images load from an external server; a failed image falls back to the placeholder instead of a broken icon.

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
