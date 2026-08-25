from src.data.loader import QuestionLoader
from src.interview.evaluator import Evaluator


# --------------------------------------------------
# Load Questions
# --------------------------------------------------

loader = QuestionLoader()

llm_questions = loader.load(
    "data/llm_interview_questions.json"
)

rag_questions = loader.load(
    "data/rag_interview_questions.json"
)

questions = (
    llm_questions[:5]
    + rag_questions[:5]
)


# --------------------------------------------------
# Fake Answers
# --------------------------------------------------

answers = []

for index, question in enumerate(questions):

    correct_answer = question["correct_answer"]

    # First 6 correct
    if index < 6:
        selected_answer = correct_answer
    else:
        selected_answer = (
            0
            if correct_answer != 0
            else 1
        )

    answers.append(
        {
            "question_id": question["id"],
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": (
                selected_answer == correct_answer
            ),
        }
    )


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

evaluator = Evaluator(
    questions=questions,
    answers=answers
)

result = evaluator.evaluate()


# --------------------------------------------------
# Print Result
# --------------------------------------------------

print()
print("-" * 40)
print("Evaluator Test")
print("-" * 40)

print(
    f"Total questions: "
    f"{result['total_questions']}"
)

print(
    f"Correct answers: "
    f"{result['correct_answers']}"
)

print(
    f"Overall score: "
    f"{result['score']:.1f}%"
)

print()
print("Category Performance:")

for category, stats in result[
    "category_performance"
].items():

    print(
        f"{category}: "
        f"{stats['correct']}/{stats['total']} "
        f"({stats['score']:.1f}%)"
    )

print()
print("Difficulty Performance:")

for difficulty, stats in result[
    "difficulty_performance"
].items():

    print(
        f"{difficulty}: "
        f"{stats['correct']}/{stats['total']} "
        f"({stats['score']:.1f}%)"
    )
