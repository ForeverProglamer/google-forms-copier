from __future__ import annotations
from entities.question import Question


class TextQuestion(Question):

    def __init__(self, title: str, answer: str):
        self.title = title
        self.answer = answer

    def select_answer(self) -> None:
        pass

    def __eq__(self, question: TextQuestion) -> bool:
        return self.title == question.title