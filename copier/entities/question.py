from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from selenium.webdriver.remote.webelement import WebElement


Answer = Union[str, List[str]]
SelectElement = Union[List[Dict[str, Union[str, WebElement]]], WebElement]

# todo consider moving class variables to instance variables
class Question(ABC):
    _title: str
    _answer: Union[Answer, None]
    _select_element: Union[SelectElement, None]

    @abstractmethod
    def select_answer(self, answer: Answer) -> None:
        pass

    def get_title(self) -> str:
        return self._title

    def get_answer(self) -> Union[Answer, None]:
        return self._answer

    def __eq__(self, question: Question) -> bool:
        if isinstance(question, type(self)):
            return self._title == question.get_title()
        return False