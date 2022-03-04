from abc import ABC, abstractmethod
from copier.entities.question import Question
from copier.entities.radiobutton_question import RadioButtonQuestion
from copier.entities.text_question import TextQuestion
from copier.entities.checkbox_question import CheckBoxQuestion
from copier.entities.select_question import SelectQuestion
from typing import Callable, List, Union
from bs4 import Tag
from selenium.webdriver.remote.webelement import WebElement
import logging


class AbstractScraper(ABC):
    logger = logging.getLogger('copier.scrapers.logger')
    
    # todo consider moving class variable to instance variable
    url: str

    @abstractmethod
    def extract_all_questions(self) -> List[Question]:
        pass

    @abstractmethod
    def _get_question_extractor(self, question_element: Union[Tag, WebElement]) -> Callable[[Union[Tag, WebElement]], Question]:
        pass

    @abstractmethod
    def _get_question_title(self, question_element: Union[Tag, WebElement]) -> str:
        pass

    @abstractmethod
    def _extract_question_with_radiobutton(self, question_element: Union[Tag, WebElement]) -> RadioButtonQuestion:
        pass

    @abstractmethod
    def _extract_question_with_checkbox(self, question_element: Union[Tag, WebElement]) -> CheckBoxQuestion:
        pass

    @abstractmethod
    def _extract_question_with_text(self, question_element: Union[Tag, WebElement]) -> TextQuestion:
        pass

    @abstractmethod
    def _extract_question_with_select(self, question_element: Union[Tag, WebElement]) -> SelectQuestion:
        pass