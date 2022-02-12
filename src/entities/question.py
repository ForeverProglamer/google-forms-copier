from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from selenium.webdriver.remote.webelement import WebElement

Answer = Union[str, List[str]]
SelectElement = Union[Dict[str, Union[str, WebElement]], WebElement]

class Question(ABC):
    title: str
    answer: Union[Answer, None]
    select_element: Union[SelectElement, None]

    @abstractmethod
    def select_answer(self, answer: Answer) -> None:
        pass

    def __eq__(self, question: Question) -> bool:
        if isinstance(question, type(self)):
            return self.title == question.title
        return False