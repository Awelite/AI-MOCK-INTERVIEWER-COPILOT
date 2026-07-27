from coding_round.coding_session_manager import (
    CodingSessionManager
)

session = (
    CodingSessionManager(
        total_questions=3
    )
)

session.add_score(40)

session.add_score(70)

session.add_score(90)

print(
    session.final_score()
)