from src.interview.graph import build_interview_graph


initial_state = {
    "candidate": {
        "name": "Test User",
        "experience": "2 years of Python",
        "skills": ["Python", "LLMs"],
        "level": "Junior",
        "position": "LLM Engineer",
        "company": "Amazon",
    },

    "selected_questions": [],

    "current_question": None,

    "current_question_index": 0,

    "current_difficulty": "easy",

    "answers": [],

    "question_count": 0,

    "interview_finished": False,

    "user_answer": None,
}


graph = build_interview_graph()

result = graph.invoke(initial_state)


print("\n------------------------------")
print("Graph Test")
print("------------------------------")

print(
    "Question count:",
    result["question_count"]
)

print(
    "Interview finished:",
    result["interview_finished"]
)

print(
    "Answers recorded:",
    len(result["answers"])
)

print(
    "Current question index:",
    result["current_question_index"]
)

print(
    "\nFinal difficulty:",
    result["current_difficulty"]
)

print("\nAnswers:")

for answer in result["answers"]:

    print(
        answer["question_id"],
        "| correct:",
        answer["correct_answer"],
        "| user:",
        answer["selected_answer"],
        "|",
        "✓" if answer["is_correct"] else "✗"
    )
