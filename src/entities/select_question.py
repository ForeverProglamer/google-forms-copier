from __future__ import annotations
from entities.question import Question
from typing import List, Dict


class SelectQuestion(Question):

    def __init__(self, title: str, answer: List[Dict]):
        self.title = title
        self.answer = answer

    def select_answer(self) -> None:
        pass

    def __eq__(self, question: SelectQuestion) -> bool:
        return self.title == question.title