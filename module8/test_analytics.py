from module8.memory.memory_engine import (
    MemoryEngine
)

from module8.memory.analytics_engine import (
    AnalyticsEngine
)

# ---------------------------------
# LOAD MEMORY
# ---------------------------------

memory = MemoryEngine()

history = memory.get_candidate_history(
    "CAND_001"
)

# ---------------------------------
# ANALYZE
# ---------------------------------

analytics = AnalyticsEngine()

result = analytics.analyze_candidate_progress(
    history
)

# ---------------------------------
# OUTPUT
# ---------------------------------

print("\nANALYTICS REPORT:\n")

print(result)