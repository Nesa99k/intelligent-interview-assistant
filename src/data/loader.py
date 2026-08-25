import json
from pathlib import Path


class QuestionLoader:
    def load(self, file_path: str) -> list[dict]:
        path = Path(file_path)

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
