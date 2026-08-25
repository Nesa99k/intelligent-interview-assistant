from collections import Counter


class QuestionAnalyzer:

    @staticmethod
    def total_questions(questions: list[dict]) -> int:
        return len(questions)
# -----------------------------------------------------------------------

    @staticmethod
    def difficulty_distribution(questions: list[dict]) -> dict:
        return dict(
            Counter(
                question["difficulty"] for question in questions
            )
        )
# -----------------------------------------------------------------------

    @staticmethod
    def category_distribution(questions: list[dict]) -> dict:
        return dict(
            Counter(
                question["category"]
                for question in questions
            )
        )
