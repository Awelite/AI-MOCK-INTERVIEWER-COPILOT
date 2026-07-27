from qgen.qgen_engine import (
    generate_questions
)


resume = """
Python backend developer
SQL
Docker
REST APIs
FastAPI
"""

jd = """
Looking for backend engineer with
Python SQL APIs Docker
"""

result = generate_questions(

    resume,
    jd,
    "medium"
)

print(result)