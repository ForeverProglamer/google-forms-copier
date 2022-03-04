from .abstract_scraper import AbstractScraper
from .config import headers, selectors, jscontrollers, classes
from copier.entities.question import Question
from copier.entities.radiobutton_question import RadioButtonQuestion
from copier.entities.text_question import TextQuestion
from copier.entities.checkbox_question import CheckBoxQuestion
from copier.entities.select_question import SelectQuestion
from typing import Callable, List
from bs4 import Tag, BeautifulSoup
import requests


selectors = selectors['src']
jscontrollers = jscontrollers['src']


class SourcePageScraper(AbstractScraper):
    def __init__(self, url: str):
        self.logger.debug(f'Requesting {url}')
        req = requests.get(url, headers=headers)
        if not req.ok:
            self.logger.debug(f'Can`t load page: code {req.status_code}')
            raise ConnectionError(f'Can`t load page: code {req.status_code}')
        self.html = req.text

    def extract_all_questions(self) -> List[Question]:
        soup = BeautifulSoup(self.html, 'html.parser')
        try:
            question_elements = list(filter(
                lambda el: el['jscontroller'] in jscontrollers.values(),
                soup.select(selectors['question_element'])
            ))
        except KeyError as e:
            self.logger.debug('0 question elements found on page')
            return []

        self.logger.debug(f'{len(question_elements)} question elements found on page')

        questions = []
        for question_element in question_elements:
            try:
                extract = self._get_question_extractor(question_element)
            except Exception as e:
                print(e)
            else:
                questions.append(extract(question_element))

        self.logger.debug(f'{len(questions)} questions extracted from page')
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
        else:
            raise Exception(f'Can`t define a question type: jscontroller="{jscontroller}"')

    def _get_question_title(self, question_element: Tag) -> str:
        return question_element.select_one(selectors['question_title']).get_text()

    def _extract_question_with_radiobutton(self, question_element: Tag) -> RadioButtonQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['radiobutton_option'])
        try:
            checked_option = next(filter(lambda opt: classes['is_checked'] in opt['class'], options))
        except StopIteration:
            answer = None
        else:
            answer = checked_option.select_one(selectors['radiobutton_label']).get_text()
        
        # print({'title': title, 'answer': answer})
        return RadioButtonQuestion(title, answer)

    def _extract_question_with_checkbox(self, question_element: Tag) -> CheckBoxQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['checkbox_option'])
        checked_options = list(filter(lambda opt: opt.select_one(selectors['checkbox_checked_option']), options))
        answer = None
        if checked_options:
           answer = [opt.select_one(selectors['checkbox_label']).get_text() for opt in checked_options] 
    
        # print({'title': title, 'answer': answer})
        return CheckBoxQuestion(title, answer)

    def _extract_question_with_text(self, question_element: Tag) -> TextQuestion:
        title = self._get_question_title(question_element)
        answer = question_element.select_one(selectors['text_label'])
        if not answer:
            answer = question_element.select_one(selectors['long_text_label'])
        answer = answer.get_text()

        # print({'title': title, 'answer': answer})
        return TextQuestion(title, answer)

    def _extract_question_with_select(self, question_element: Tag) -> SelectQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['select_option'])[1:]
        try:
            checked_option = next(filter(lambda opt: opt['aria-selected'] == 'true', options))
        except StopIteration:
            answer = None
        else:
            answer = checked_option.select_one(selectors['select_label']).get_text()
        
        # print({'title': title, 'answer': answer})
        return SelectQuestion(title, answer)