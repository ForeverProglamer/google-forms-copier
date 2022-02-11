from scrapers.abstract_scraper import AbstractScraper
from entities.question import Question
from entities.radiobutton_question import RadioButtonQuestion
from entities.text_question import TextQuestion
from entities.checkbox_question import CheckBoxQuestion
from entities.select_question import SelectQuestion
from typing import Callable, List, Union
from bs4 import Tag
from selenium.webdriver.remote.webelement import WebElement


class DestinationPageScraper(AbstractScraper):

    def __init__(self, url: str):
        self.url = url

    def extract_all_questions(self) -> List[Question]:
        pass

    def _get_question_extractor(self, question_element: Union[Tag, WebElement]) -> Callable[[Union[Tag, WebElement]], Question]:
        pass

    def _extract_question_with_radiobutton(self, question_element: Union[Tag, WebElement]) -> RadioButtonQuestion:
        pass

    def _extract_question_with_checkbox(self, question_element: Union[Tag, WebElement]) -> CheckBoxQuestion:
        pass

    def _extract_question_with_text(self, question_element: Union[Tag, WebElement]) -> TextQuestion:
        pass

    def _extract_question_with_select(self, question_element: Union[Tag, WebElement]) -> SelectQuestion:
        pass