#!/usr/bin/env python3
"""
Fix unparsed Russian objections in src/data/models/*.json
"""

import glob
import json
import os
import re

STRATEGY_WORDS = [
    "Поясните",            # Clarify
    "Укажите",             # Indicate / Point out
    "Предложите",          # Suggest / Offer
    "Продемонстрируйте",   # Demonstrate / Show
    "Рекомендуйте",        # Recommend
    "Объясните",           # Explain
    "Обратите внимание",   # Pay attention
    "Покажите",            # Show
    "Подчеркните",         # Emphasize
    "Напомните",           # Remind
    "Заверьте",            # Assure
    "Сделайте акцент",     # Accentuate
    "Расскажите",          # Tell
    "Акцентируйте",        # Accentuate
    "Посоветуйте",         # Advise
]

MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
WORD_IMAGE_DIRECTIVE = re.compile(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}")
PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")


def clean(text: str) -> str:
    t = PAREN_URL.sub("", text)
    t = BARE_URL.sub("", t)
    t = WORD_IMAGE_DIRECTIVE.sub("", t)
    t = MARKDOWN_IMAGE.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


def parse_objections(raw: str):
    if not isinstance(raw, str) or not raw.strip():
        return []

    is_strat_format = "Возражение" in raw or any(sw in raw for sw in STRATEGY_WORDS)

    if "«" in raw and is_strat_format:
        cleaned = clean(raw)
        cleaned = re.sub(r"^Возражение\s+Стратегия\s+[^\s«]+\s*", "", cleaned)
        cleaned = cleaned.replace("---", "города")

        parts = cleaned.split("«")
        out = []
        for part in parts:
            part = part.strip()
            if not part:
                continue

            strat_found = None
            strat_idx = -1
            for sw in STRATEGY_WORDS:
                m = re.search(r"\b" + re.escape(sw) + r"\b", part)
                if m:
                    if strat_idx == -1 or m.start() < strat_idx:
                        strat_idx = m.start()
                        strat_found = (m.start(), m.end(), sw)

            if not strat_found and "»" in part:
                inside_guillemets = part[: part.find("»")]
                words = list(re.finditer(r"[A-Za-zА-Яа-яЁё]+", inside_guillemets))
                if len(words) >= 2:
                    for w in words[1:]:
                        if w.group(0)[0].isupper():
                            strat_found = (w.start(), w.start(), "")
                            break

            if not strat_found:
                continue

            q = part[: strat_found[0]].strip(" \t\n\r,;«»")
            rest = part[strat_found[1] :].strip()

            if "»" in rest:
                a_part1, a_part2 = rest.split("»", 1)
            else:
                a_part1, a_part2 = rest, ""

            a = (a_part1.strip() + " " + a_part2.strip()).strip(" \t\n\r,;«»")
            a = re.sub(r"^[,\s]+", "", a)
            a = re.sub(r"\s{2,}", " ", a)

            if q and a:
                if not a.endswith("."):
                    a += "."
                out.append({"q": q, "a": a})

        if out:
            return out

    return None


def main():
    fixed = 0
    models_dir = "src/data/models"
    for filepath in sorted(glob.glob(f"{models_dir}/*.json"), key=lambda x: int(os.path.basename(x).split(".")[0])):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        ru_objs = data.get("objections", {}).get("ru", [])
        if len(ru_objs) == 1 and ru_objs[0].get("q") == "":
            raw = ru_objs[0].get("a", "")
            parsed = parse_objections(raw)
            if parsed and len(parsed) > 0:
                data["objections"]["ru"] = parsed
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                fixed += 1
                print(f"Fixed model {data['id']} ({data['name']}): {len(parsed)} objections parsed")

    print(f"Total models fixed: {fixed}")


if __name__ == "__main__":
    main()
