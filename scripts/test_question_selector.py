from src.data.loader import QuestionLoader
from src.interview.question_selector import QuestionSelector

loader = QuestionLoader()

llm_questions = loader.load(
    "data/llm_interview_questions.json"
)

rag_questions = loader.load(
    "data/rag_interview_questions.json"
)

question_banks = {
    "llm": llm_questions,
    "rag": rag_questions,
}
selector = QuestionSelector(question_banks)

questions = selector.get_questions(
    position="LLM Engineer",
    level="Junior",
    number_of_questions=10,
)

print(f"Selected questions: {len(questions)}")

for question in questions:
    print(
        question["id"],
        "|",
        question["difficulty"],
        "|",
        question["category"]
    )
