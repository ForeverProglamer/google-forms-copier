from scrapers.abstract_scraper import AbstractScraper
from entities.question import Question
from entities.radiobutton_question import RadioButtonQuestion
from entities.text_question import TextQuestion
from entities.checkbox_question import CheckBoxQuestion
from entities.select_question import SelectQuestion
from typing import Callable, List
from bs4 import Tag, BeautifulSoup
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Accept': '*/*'
}

selectors = {
    'question_element': '.freebirdFormviewerViewNumberedItemContainer > .freebirdFormviewerViewItemsItemItem',
    'question_title': '.freebirdFormviewerViewItemsItemItemTitle.exportItemTitle.freebirdCustomFont',
    'radiobutton_option': '.freebirdFormviewerViewItemsRadioOptionContainer > label',
    'radiobutton_label': '.freebirdFormviewerViewItemsRadioLabel',
    'checkbox_option': 'label.freebirdFormviewerViewItemsCheckboxContainer',
    'checkbox_label': '.freebirdFormviewerViewItemsCheckboxLabel',
    'text_label': '.freebirdFormviewerViewItemsTextTextItemContainer > div',
    'select_option': '.quantumWizMenuPaperselectOption',
    'select_label': 'span'
}

jscontrollers = {
    'text': 'rDGJeb', # short text, long text
    'radiobutton': 'pkFYWb', # radio button
    'checkbox': 'hIYTQc', # checkbox
    'select': 'jmDACb' # select root
}

classes = {
    'is_checked': 'isChecked',
    'is_selected': 'isSelected'
}

class SourcePageScraper(AbstractScraper):

    def __init__(self, url: str):
        self.url = url
        self.html = requests.get(url, headers=headers)

    def extract_all_questions(self) -> List[Question]:
        soup = BeautifulSoup(self.html.text, 'html.parser')
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
        answer = list(map(
            lambda option: {
                'label': option.select_one(selectors['radiobutton_label']).get_text(),
                'checked': classes['is_checked'] in option['class']
            },
            options
        ))
        # print({'title': title, 'answer': answer})
        return RadioButtonQuestion(title, answer)

    def _extract_question_with_checkbox(self, question_element: Tag) -> CheckBoxQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['checkbox_option'])
        answer = list(map(
            lambda option: {
                'lambda': option.select_one(selectors['checkbox_label']).get_text(),
                'checked': classes['is_checked'] in option['class']
            },
            options 
        ))
        # print({'title': title, 'answer': answer})
        return CheckBoxQuestion(title, answer)

    def _extract_question_with_text(self, question_element: Tag) -> TextQuestion:
        title = self._get_question_title(question_element)
        answer = question_element.select_one(selectors['text_label']).get_text()
        # print({'title': title, 'answer': answer})
        return TextQuestion(title, answer)

    def _extract_question_with_select(self, question_element: Tag) -> SelectQuestion:
        title = self._get_question_title(question_element)
        options = question_element.select(selectors['select_option'])[1:]
        answer = list(map(
            lambda option: {
                'label': option.select_one(selectors['select_label']).get_text(),
                'checked': classes['is_selected'] in option['class']
            },
            options
        ))
        print({'title': title, 'answer': answer})
        return SelectQuestion(title, answer)