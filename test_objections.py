#!/usr/bin/env python3
"""Test script for objection parsing with Festone example."""

import re

# Russian strategy words that introduce responses to objections
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
]

# Markdown image syntax: ![...](url) or ![](url)
MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
# HTML/Word image directives with attributes: ![](media/...) or similar with {...}
WORD_IMAGE_DIRECTIVE = re.compile(r"\.?\s*!\[([^\]]*)\]\([^)]+\)\s*\{[^}]*\}")

PAREN_URL = re.compile(r"\(\s*(?:https?://)[^()]*(?:\([^()]*\)[^()]*)*\)")
BARE_URL = re.compile(r"https?://\S+")


def clean(text: str) -> str:
    t = PAREN_URL.sub("", text)
    t = BARE_URL.sub("", t)
    # Remove Word/Markdown image directives first (they may contain {...} attributes)
    t = WORD_IMAGE_DIRECTIVE.sub("", t)
    # Remove any remaining Markdown image syntax
    t = MARKDOWN_IMAGE.sub("", t)
    t = re.sub(r"\(\s*(nan|Данные отсутствуют[^)]*|URL non disponibile)\s*\)", "", t, flags=re.I)
    t = re.sub(r"\([^)]*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


def parse_objections(raw):
    """
    Parse objections in multiple formats:
    1. Interleaved Russian guillemet format where strategy word sits inside «...»
       e.g., «Question StrategyWord AnswerPart1» AnswerPart2
    2. Bracket format: [Q] -> A || [Q] -> A
    3. Fallback: Q || A (pipe-separated)
    """
    if not isinstance(raw, str) or not raw.strip():
        return []

    out = []

    # Check if this is the Russian 'Возражение Стратегия' / guillemet format
    is_strat_format = "Возражение" in raw or any(sw in raw for sw in STRATEGY_WORDS)

    if "«" in raw and is_strat_format:
        cleaned = clean(raw)
        cleaned = re.sub(r"^Возражение\s+Стратегия\s+[^\s«]+\s*", "", cleaned)
        cleaned = cleaned.replace("---", "города")

        parts = cleaned.split("«")
        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Find strategy word within this part
            strat_found = None
            strat_idx = -1
            for sw in STRATEGY_WORDS:
                m = re.search(r"\b" + re.escape(sw) + r"\b", part)
                if m:
                    if strat_idx == -1 or m.start() < strat_idx:
                        strat_idx = m.start()
                        strat_found = (m.start(), m.end(), sw)

            if not strat_found:
                continue

            q = part[:strat_found[0]].strip(" \t\n\r,;«»")
            rest = part[strat_found[1]:].strip()

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

    # Fall back to bracket format: [Q] -> A
    if "[" in raw and "]" in raw:
        for block in re.split(r"\|\|", raw):
            block = block.strip().strip(",")
            if not block:
                continue
            m = re.match(r"^\s*\[(.+?)\]\s*->\s*(.*)$", block, flags=re.S)
            if m:
                out.append({"q": clean(m.group(1)), "a": clean(m.group(2))})
            else:
                out.append({"q": "", "a": clean(block)})

        if out:
            return out

    # Generic pipe delimiter fallback
    if "||" in raw:
        for block in re.split(r"\|\|", raw):
            block = block.strip()
            if block:
                out.append({"q": "", "a": clean(block)})
        if out:
            return out

    # Last fallback: single block
    if raw.strip():
        out.append({"q": "", "a": clean(raw)})

    return out


# Test with Festone objections
test_input = """Возражение Стратегия преодоления «Слишком много объема Поясните, что встречные складки заложены таким на бедрах» образом, чтобы лежать плоско у основания талии, раскрываясь в объеме только ниже, что сохраняет изящество бедер. «Разрез кажется Укажите на то, что в статичном положении слишком открытым» разрез скрыт в глубине складки и проявляет себя только при широком шаге, сохраняя элегантную сдержанность. «Макси-длина неудобна Предложите примерить юбку с курткой Stelle для города» 0919, как в витрине №75. Это доказывает, что модель отлично адаптируется к активному городскому ритму. «Плиссировка/складки Продемонстрируйте стайлинг с трикотажным --- это слишком жилетом Maica 2050. Сочетание строгой официально» формы юбки и мягкого трикотажа делает образ расслабленным и современным. «Сложно подобрать верх Рекомендуйте заправлять плечевые изделия к такой длине» (например, рубашку Barberino 0201) внутрь, чтобы подчеркнуть конструкцию пояса и сохранить правильные пропорции фигуры.![](media/image13.jpg){width='0.5833333333333334in' height='0.78125in'}"""

print("=" * 80)
print("TESTING OBJECTION PARSING - FESTONE MODEL")
print("=" * 80)
print()

results = parse_objections(test_input)

print(f"Total objections parsed: {len(results)}")
print()

for i, obj in enumerate(results, 1):
    print(f"--- Objection {i} ---")
    print(f"Q: {obj['q']}")
    print(f"A: {obj['a']}")
    print()

print("=" * 80)
