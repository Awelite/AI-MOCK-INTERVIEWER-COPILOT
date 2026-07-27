CONFIDENT = [
    "implemented","developed","built",
    "designed","led","achieved","improved"
]

UNCERTAIN = [
    "maybe","probably","i think",
    "not sure","guess","kind of"
]

def confidence_score(text):

    text = text.lower()

    score = 0.5

    for w in CONFIDENT:
        if w in text:
            score += 0.08

    for w in UNCERTAIN:
        if w in text:
            score -= 0.12

    return max(0,min(score,1))