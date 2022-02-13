from scrapers.abstract_scraper import AbstractScraper
from entities.question import Question
from entities.radiobutton_question import RadioButtonQuestion
from entities.text_question import TextQuestion
from entities.checkbox_question import CheckBoxQuestion
from entities.select_question import SelectQuestion
from scrapers.config import headers, selectors, jscontrollers, classes
from typing import Callable, List
from bs4 import Tag, BeautifulSoup
import requests


selectors = selectors['src']
jscontrollers = jscontrollers['src']

class SourcePageScraper(AbstractScraper):

    def __init__(self, url: str):
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            raise ConnectionError(f'Can`t load page: code {req.status_code}')
        self.html = req.text

    def extract_all_questions(self) -> List[Question]:
        soup = BeautifulSoup(self.html, 'html.parser')
        question_elements = list(filter(
            lambda el: el['jscontroller'] in jscontrollers.values(),
            soup.select(selectors['question_element'])
        ))

        questions = []
        for question_element in question_elements:
            extract = self._get_question_extractor(question_element)
            questions.append(extract(question_element))

        return questions

    def _get_question_extractor(self, question_element: Tag) -> Callable[[Tag], Question]:
        jscontroller = question_element['jscontroller']
        if jscontroller == jscontrollers['radiobutton']:
            return self._extract_question_with_radiobutton
        elif jscontroller == jscontrollers['checkbox']:
            return self._extract_question_with_checkbox
        elif jscontroller == jscontrollers['select']:
            return self._extract_question_with_select
        elif jscontroller == jscontrollers['text']:
            return self._extract_question_with_text

    def _get_question_title(self, question_element: Tag) -> str:
        return question_element.select_one(selectors['question_title']).get_text()

    def _extract_question_with_radiobutton(self, question_element: Tag) -> RadioButtonQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['radiobutton_option'])
        checked_option = next(filter(lambda opt: classes['is_checked'] in opt['class'], options))
        answer = None
        if checked_option:
            answer = checked_option.select_one(selectors['radiobutton_label']).get_text()
        
        print({'title': title, 'answer': answer})
        return RadioButtonQuestion(title, answer)

    def _extract_question_with_checkbox(self, question_element: Tag) -> CheckBoxQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['checkbox_option'])
        checked_options = list(filter(lambda opt: classes['is_checked'] in opt['class'], options))
        answer = None
        if checked_options:
           answer = [opt.select_one(selectors['checkbox_label']).get_text() for opt in checked_options] 
    
        print({'title': title, 'answer': answer})
        return CheckBoxQuestion(title, answer)

    def _extract_question_with_text(self, question_element: Tag) -> TextQuestion:
        title = self._get_question_title(question_element)
        answer = question_element.select_one(selectors['text_label']).get_text()

        print({'title': title, 'answer': answer})
        return TextQuestion(title, answer)

    def _extract_question_with_select(self, question_element: Tag) -> SelectQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['select_option'])[1:]
        checked_option = next(filter(lambda opt: classes['is_selected'] in opt['class'], options))
        answer = None
        if checked_option:
            answer = checked_option.select_one(selectors['select_label']).get_text()
        
        print({'title': title, 'answer': answer})
        return SelectQuestion(title, answer)