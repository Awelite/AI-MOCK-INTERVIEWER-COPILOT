from module8.memory.memory_engine import (
    MemoryEngine
)

from module8.memory.trend_engine import (
    TrendEngine
)

# ---------------------------------
# LOAD HISTORY
# ---------------------------------

memory = MemoryEngine()

history = memory.get_candidate_history(
    "CAND_001"
)

# ---------------------------------
# ANALYZE TRENDS
# ---------------------------------

engine = TrendEngine()

result = engine.detect_trends(
    history
)

# ---------------------------------
# OUTPUT
# ---------------------------------

print("\nTREND ANALYSIS:\n")

print(result)