POSITIVE_WORDS = ["good","success","improved","achieved","led","built"]
NEGATIVE_WORDS = ["fail","problem","difficult","bad","issue"]

def sentiment_score(text):

    text = text.lower()

    pos = sum(word in text for word in POSITIVE_WORDS)
    neg = sum(word in text for word in NEGATIVE_WORDS)

    score = 0.5 + (pos - neg)*0.1

    return max(0,min(score,1))