def generate_feedback(p, c, cl, s):

    if c < 0.4:
        return "Use stronger action verbs and avoid uncertain words."

    elif cl < 0.4:
        return "Answer lacks clarity. Try structuring response better."

    elif s < 0.4:
        return "Use STAR method: Situation, Task, Action, Result."

    elif p < 0.4:
        return "Maintain a positive tone and highlight achievements."

    else:
        return "Good confident and structured HR response."