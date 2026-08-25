from src.interview.graph import build_interview_graph
from src.interview.session import create_initial_state


candidate = {
    "name": "Test User",
    "experience": "2 years of Python",
    "skills": ["Python", "LLMs"],
    "level": "Junior",
    "position": "LLM Engineer",
    "company": "Amazon",
}


print("-" * 50)
print("5-Question Agent Graph Test")
print("-" * 50)


# --------------------------------------------------
# Create Initial State
# --------------------------------------------------

state = create_initial_state(candidate)

print(
    f"Question bank size: "
    f"{len(state['question_bank'])}"
)


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

graph = build_interview_graph()


# --------------------------------------------------
# Start Interview
# --------------------------------------------------

state = graph.invoke(state)


# --------------------------------------------------
# Simulate 10 Questions
# --------------------------------------------------

while not state["interview_finished"]:

    question = state["current_question"]

    print()
    print("-" * 50)

    print(
        f"Question {state['question_count']}/5"
    )

    print(
        f"ID: {question['id']}"
    )

    print(
        f"Difficulty: "
        f"{question['difficulty']}"
    )

    print(
        f"Category: "
        f"{question['category']}"
    )

    print(
        f"Question: "
        f"{question['question']}"
    )

    # --------------------------------------------------
    # Simulate Answer
    #
    # Alternate between correct and incorrect
    # --------------------------------------------------

    if state["question_count"] % 2 == 1:

        state["user_answer"] = (
            question["correct_answer"]
        )

        print("Simulated answer: CORRECT")

    else:

        wrong_answers = [
            index
            for index in range(
                len(question["options"])
            )
            if index != question["correct_answer"]
        ]

        state["user_answer"] = (
            wrong_answers[0]
        )

        print("Simulated answer: WRONG")

    # --------------------------------------------------
    # Run Graph
    # --------------------------------------------------

    state = graph.invoke(state)


# --------------------------------------------------
# Final Result
# --------------------------------------------------

print()
print("=" * 50)
print("FINAL RESULT")
print("=" * 50)

print(
    f"Question count: "
    f"{state['question_count']}"
)

print(
    f"Interview finished: "
    f"{state['interview_finished']}"
)

print(
    f"Answers recorded: "
    f"{len(state['answers'])}"
)

print()
print("Questions asked:")

for index, answer in enumerate(
    state["answers"],
    start=1
):

    print(
        f"{index}. "
        f"{answer['question_id']} | "
        f"{answer['difficulty']} | "
        f"{answer['category']} | "
        f"{'✓' if answer['is_correct'] else '✗'}"
    )
