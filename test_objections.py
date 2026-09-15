#!/usr/bin/env python3
"""Test script for objection parsing with Festone example."""

import re

# Russian strategy words that introduce responses to objections
STRATEGY_WORDS = {
    "Поясните",      # Clarify
    "Укажите",       # Indicate / Point out
    "Предложите",    # Suggest / Offer
    "Продемонстрируйте",  # Demonstrate / Show
    "Рекомендуйте",  # Recommend
}

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
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"([,.;:])\s*([,.;:])+", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;")


def parse_objections(raw):
    """
    Parse objections in multiple formats:
    1. Concatenated Russian guillemet format: «Q1» StrategyWord1 A1«Q2» StrategyWord2 A2...
    2. Bracket format: [Q] -> A || [Q] -> A
    3. Fallback: Q || A (pipe-separated)
    
    For concatenated format, responses end at:
    - Next « (start of next question)
    - Capital Cyrillic letter (А-Я) at word boundary
    """
    if not isinstance(raw, str):
        return []
    
    out = []
    
    # Try concatenated Russian guillemet format first
    # Pattern: «question» followed by strategy word, then answer text
    if "«" in raw:
        # Split by « to find question blocks
        parts = raw.split("«")
        
        for i, part in enumerate(parts):
            if not part.strip():
                continue
            
            # Find the end of the question (closing »)
            q_end = part.find("»")
            if q_end == -1:
                continue
            
            question = part[:q_end].strip()
            remainder = part[q_end + 1:].strip()
            
            if not remainder:
                continue
            
            # Find strategy word in the remainder
            strategy_match = None
            for strategy in STRATEGY_WORDS:
                match = re.search(r"\b" + re.escape(strategy) + r"\b", remainder, re.IGNORECASE)
                if match:
                    strategy_match = match
                    break
            
            if not strategy_match:
                continue
            
            # Answer starts after the strategy word
            answer_start = strategy_match.end()
            answer_text = remainder[answer_start:].strip()
            
            # Answer ends at:
            # 1. Next « (if more questions follow), or
            # 2. Capital Cyrillic letter (А-Я) followed by space/word boundary
            # 3. End of string
            next_q_pos = answer_text.find("«")
            
            # Look for capital Cyrillic at word boundary
            capital_cyrillic_match = re.search(r"(?:^|\s)([А-Я])", answer_text)
            capital_pos = capital_cyrillic_match.start() + 1 if capital_cyrillic_match else len(answer_text)
            
            # Use whichever comes first
            if next_q_pos != -1:
                answer_end = min(next_q_pos, capital_pos) if capital_pos < len(answer_text) else next_q_pos
            else:
                answer_end = capital_pos
            
            answer = clean(answer_text[:answer_end])
            if question or answer:
                out.append({"q": clean(question), "a": answer})
        
        if out:
            return out
    
    # Fall back to bracket format: [Q] -> A
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
