try:
    import textstat
except ImportError:
    textstat = None

def clarity_score(text):
    if textstat is None:
        # Fallback: simple clarity based on word length and sentence structure
        words = len(text.split())
        sentences = len([s for s in text.split('.') if s.strip()])
        avg_word_length = sum(len(w) for w in text.split()) / max(words, 1)
        readability = 206.835 - 1.015 * (words / max(sentences, 1)) - 84.6 * (avg_word_length / 100)
    else:
        readability = textstat.flesch_reading_ease(text)

    clarity = readability / 100

    return max(0, min(clarity, 1))