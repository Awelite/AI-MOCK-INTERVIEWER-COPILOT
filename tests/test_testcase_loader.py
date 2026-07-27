from coding_round.testcase_loader import (
    TestCaseLoader
)

loader = TestCaseLoader()

cases = loader.load_testcases(
    32
)

print(cases)