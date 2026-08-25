import random


class QuestionSelector:

    POSITION_CONFIG = {
        "LLM Engineer": ["llm", "rag"],
        "Generative AI Engineer": ["llm", "rag"],
        "RAG Engineer": ["rag", "llm"],
    }

    ALLOWED_DIFFICULTIES = {
        "Junior": ["easy", "medium"],
        "Mid-level": ["easy", "medium", "hard"],
        "Senior": ["easy", "medium", "hard"],
    }

    def __init__(self, question_banks: dict[str, list[dict]]):
        self.question_banks = question_banks

    def get_questions(
        self,
        position: str,
        level: str,
        number_of_questions: int = 10,

    ) -> list[dict]:

        if position not in self.POSITION_CONFIG:
            raise ValueError(f"Unsupported position: {position}")

        if level not in self.ALLOWED_DIFFICULTIES:
            raise ValueError(f"Unsupported level: {level}")

        allowed_banks = self.POSITION_CONFIG[position]
        allowed_difficulties = self.ALLOWED_DIFFICULTIES[level]

        eligible_questions = []

        for bank_name in allowed_banks:
            questions = self.question_banks.get(
                bank_name,
                []
            )
            for question in questions:

                if question["difficulty"] in allowed_difficulties:
                    eligible_questions.append(question)

        if not eligible_questions:
            return []

        number_of_questions = min(
            number_of_questions,
            len(eligible_questions)
        )
        return random.sample(
            eligible_questions,
            number_of_questions
        )
