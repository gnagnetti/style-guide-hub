"""Converts the source Excel files into src/data/models.json.

Run: python3 scripts/build_data.py <models.xlsx> <url.xlsx>
The image lookup (url.xlsx) is the single source of truth for every picture.
"""

import json
import re
import sys
from collections import defaultdict

import pandas as pd

MODELS_XLSX, URL_XLSX = sys.argv[1], sys.argv[2]
OUT = "src/data/models.json"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def codes_key(codes) -> str:
    return " ".join(codes)


# ---------------------------------------------------------------- image index
url_df = pd.read_excel(URL_XLSX)
by_full = {}
by_name = defaultdict(list)
for _, row in url_df.iterrows():
    raw = str(row["ModelloColore"])
    url = row["Style Image URL_1"]
    url = None if (pd.isna(url) or not str(url).startswith("http")) else str(url).strip()
    m = re.match(r"^(.*?)\s*\(([\d\s]+)\)\s*$", raw)
    if not m:
        continue
    name, codes = norm(m.group(1)), re.findall(r"\d+", m.group(2))
    if url:
        by_full.setdefault(f"{name}|{codes_key(codes)}", url)
        for c in codes:
            by_full.setdefault(f"{name}|{c}", url)
        by_name[name].append(url)

unmatched = defaultdict(int)


def lookup(name: str, codes) -> str | None:
    n = norm(name)
    if codes:
        hit = by_full.get(f"{n}|{codes_key(codes)}")
        if hit:
            return hit
        for c in codes:
            hit = by_full.get(f"{n}|{c}")
            if hit:
                return hit
    if by_name.get(n):
        return by_name[n][0]
    unmatched[f"{name} ({' '.join(codes)})"] += 1
    return None


# ---------------------------------------------------------------- text tidying
PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")


def clean(text: str) -> str:
    t = PAREN_URL.sub("", text)
    t = BARE_URL.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


ITEM_RE = re.compile(
    r"\b([A-ZА-Я][A-Za-z0-9]{2,}(?:\s+[A-Z]\b)?)((?:\s+\d{3,4})+)"
)


def parse_looks(raw, self_name):
    if not isinstance(raw, str) or not raw.strip():
        return []
    looks = []
    for seg in raw.split(" | "):
        seg = seg.strip()
        if not seg:
            continue
        title, body = None, seg
        head = re.match(r"^([^:]{0,60}?):\s*(.*)$", seg, flags=re.S)
        if head and re.search(r"(Total Look|Vetrina|Стилистическое|Look)", head.group(1), re.I):
            title, body = head.group(1).strip(), head.group(2)
        items, seen = [], set()
        for m in ITEM_RE.finditer(body):
            name = re.sub(r"\s+", " ", m.group(1)).strip()
            codes = re.findall(r"\d+", m.group(2))
            key = f"{norm(name)}|{codes_key(codes)}"
            if key in seen:
                continue
            seen.add(key)
            items.append({"name": name, "code": " ".join(codes), "imageUrl": lookup(name, codes)})
        looks.append({"title": title, "text": clean(body), "items": items})
    return looks


def parse_colors(raw, model_name):
    out = []
    if not isinstance(raw, str):
        return out
    for part in raw.split(" | "):
        m = re.match(r"^\s*(.+?)\s*\(([\d\s]+)\)\s*:\s*(.*)$", part.strip())
        if not m:
            continue
        name, codes, url = m.group(1).strip(), re.findall(r"\d+", m.group(2)), m.group(3).strip()
        if not url.startswith("http"):
            url = None
        resolved = lookup(model_name, codes) or url
        out.append({"name": name, "code": " ".join(codes), "imageUrl": resolved})
    return out


def split_pipe(raw):
    if not isinstance(raw, str):
        return []
    return [clean(p) for p in raw.split("|") if p.strip()]


def parse_objections(raw):
    if not isinstance(raw, str):
        return []
    out = []
    for block in re.split(r"\|\|", raw):
        block = block.strip().strip(",")
        if not block:
            continue
        m = re.match(r"^\s*\[(.+?)\]\s*->\s*(.*)$", block, flags=re.S)
        if m:
            out.append({"q": clean(m.group(1)), "a": clean(m.group(2))})
        else:
            out.append({"q": "", "a": clean(block)})
    return out


# ---------------------------------------------------------------- build
df = pd.read_excel(MODELS_XLSX)
name_to_id = {norm(r["Nome Modello"]): int(r["ID"]) for _, r in df.iterrows()}

models = []
for _, r in df.iterrows():
    name = str(r["Nome Modello"]).strip()
    looks = parse_looks(r["Styling / Abbinamenti"], name)
    for lk in looks:
        for it in lk["items"]:
            lid = name_to_id.get(norm(it["name"]))
            if lid and lid != int(r["ID"]):
                it["modelId"] = lid
    models.append(
        {
            "id": int(r["ID"]),
            "name": name,
            "description": {
                "en": clean(r["Descrizione Eng"]) if isinstance(r["Descrizione Eng"], str) else "",
                "ru": clean(r["Descrizione"]) if isinstance(r["Descrizione"], str) else "",
            },
            "colors": parse_colors(r["Colori"], name),
            "looks": looks,
            "advice": {
                "en": split_pipe(r["Consigli di Vendita Eng"]) or split_pipe(r["Consigli di Vendita"]),
                "ru": split_pipe(r["Consigli di Vendita"]),
            },
            "objections": {
                "en": parse_objections(r["Gestione Obiezioni Eng"]) or parse_objections(r["Gestione Obiezioni"]),
                "ru": parse_objections(r["Gestione Obiezioni"]),
            },
        }
    )

models.sort(key=lambda m: m["name"].lower())
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(models, f, ensure_ascii=False)

cited = sum(len(l["items"]) for m in models for l in m["looks"])
missing = sum(1 for m in models for l in m["looks"] for i in l["items"] if not i["imageUrl"])
colors = sum(len(m["colors"]) for m in models)
no_color_img = sum(1 for m in models for c in m["colors"] if not c["imageUrl"])
print(f"models={len(models)} cited_items={cited} without_image={missing}")
print(f"colors={colors} without_image={no_color_img}")
print("top unmatched:", sorted(unmatched.items(), key=lambda x: -x[1])[:15])
