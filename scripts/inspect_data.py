from src.data.loader import QuestionLoader
from src.data.analyzer import QuestionAnalyzer

loader = QuestionLoader()
analyzer = QuestionAnalyzer()


llm_questions = loader.load("data/llm_interview_questions.json")
rag_questions = loader.load("data/rag_interview_questions.json")

print("LLM")
print("Total:", analyzer.total_questions(llm_questions))
print("Difficulty:", analyzer.difficulty_distribution(llm_questions))
print("Categories:", analyzer.category_distribution(llm_questions))

print("\nRAG")
print("Total:", analyzer.total_questions(rag_questions))
print("Difficulty:", analyzer.difficulty_distribution(rag_questions))
print("Categories:", analyzer.category_distribution(rag_questions))
