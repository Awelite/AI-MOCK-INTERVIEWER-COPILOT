from coding_round.judge0_client import (
    Judge0Client
)

client = Judge0Client()

result = client.run_code(
    code="""
a,b=map(int,input().split())
print(a+b)
""",
    language="python",
    stdin="2 3"
)

print(result)