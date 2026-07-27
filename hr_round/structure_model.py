STAR_WORDS = [
    "problem","challenge",
    "task","responsibility",
    "action","implemented",
    "result","improved","impact"
]

def structure_score(text):

    text = text.lower()

    count = 0

    for w in STAR_WORDS:
        if w in text:
            count += 1

    return min(count/4 , 1)