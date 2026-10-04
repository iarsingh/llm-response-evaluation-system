import re

STOP = {"the", "a", "an", "is", "of", "and", "to"}


def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP


def evaluate(answer, gold, context):
    aw, gw, cw = words(answer or ""), words(gold or ""), words(context or "")
    faithfulness = len(aw & cw) / len(aw) if aw else 0
    correctness = len(aw & gw) / len(gw) if gw else 0
    return {
        "faithfulness": round(faithfulness, 4),
        "correctness": round(correctness, 4),
        "passed": faithfulness >= 0.5 and correctness >= 0.5,
    }
