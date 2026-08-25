from collections import defaultdict


class Evaluator:

    def __init__(self, questions, answers):

        self.questions = questions
        self.answers = answers

    def evaluate(self):

        # --------------------------------------------------
        # Overall Performance
        # --------------------------------------------------

        total_questions = len(self.answers)

        correct_answers = sum(
            answer["is_correct"]
            for answer in self.answers
        )

        score = (
            correct_answers / total_questions * 100
            if total_questions > 0
            else 0
        )

        # --------------------------------------------------
        # Difficulty Performance
        # --------------------------------------------------

        difficulty_stats = defaultdict(
            lambda: {
                "total": 0,
                "correct": 0
            }
        )

        for answer in self.answers:

            difficulty = answer["difficulty"]

            difficulty_stats[difficulty]["total"] += 1

            if answer["is_correct"]:
                difficulty_stats[difficulty]["correct"] += 1

        # --------------------------------------------------
        # Calculate Difficulty Percentages
        # --------------------------------------------------

        difficulty_performance = {}

        for difficulty, stats in difficulty_stats.items():

            percentage = (
                stats["correct"]
                / stats["total"]
                * 100
            )

            difficulty_performance[difficulty] = {
                "total": stats["total"],
                "correct": stats["correct"],
                "score": percentage
            }

        # --------------------------------------------------
        # Final Result
        # --------------------------------------------------

        return {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score": score,
            "difficulty_performance": (
                difficulty_performance
            ),
        }
