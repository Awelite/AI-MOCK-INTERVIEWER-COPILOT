from module8.memory.memory_engine import (
    MemoryEngine
)

from module8.analytics.analytics_engine import (
    AnalyticsEngine
)

from module8.memory.trend_engine import (
    TrendEngine
)

from module8.recruiter.decision_engine import (
    RecruiterDecisionEngine
)

# ---------------------------------
# LOAD MEMORY
# ---------------------------------

memory = MemoryEngine()

history = memory.get_candidate_history(
    "CAND_001"
)

latest_result = history[-1]

# ---------------------------------
# ANALYTICS
# ---------------------------------

analytics_engine = AnalyticsEngine()

analytics = analytics_engine.generate_report(
    history
)

# ---------------------------------
# TRENDS
# ---------------------------------

trend_engine = TrendEngine()

trends = trend_engine.detect_trends(
    history
)

# ---------------------------------
# RECRUITER AI
# ---------------------------------

engine = RecruiterDecisionEngine()

result = engine.generate_decision(
    analytics,
    trends,
    latest_result
)

# ---------------------------------
# OUTPUT
# ---------------------------------

print("\nRECRUITER AI REPORT:\n")

print(result)