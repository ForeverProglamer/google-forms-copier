from .abstract_scraper import AbstractScraper
from .config import selectors, jscontrollers
from copier.entities.question import Question
from copier.entities.radiobutton_question import RadioButtonQuestion
from copier.entities.text_question import TextQuestion
from copier.entities.checkbox_question import CheckBoxQuestion
from copier.entities.select_question import SelectQuestion
from typing import Callable, List
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os


selectors = selectors['dest']
jscontrollers = jscontrollers['dest']

# todo add waits for finding elements

class DestinationPageScraper(AbstractScraper):
    def __init__(self, url: str):
        path = os.path.join('resources', 'geckodriver.exe')
        self.driver = webdriver.Firefox(executable_path=path)
        self.driver.get(url)

    def extract_all_questions(self) -> List[Question]:
        question_elements = self.driver.find_elements(By.CSS_SELECTOR, selectors['question_element'])

        questions = []
        for question_element in question_elements:
            general_element = question_element.find_element(By.CSS_SELECTOR, selectors['general_div'])
            try:
                extract = self._get_question_extractor(general_element)
            except Exception as e:
                print(e)
                continue
            else:
                questions.append(extract(question_element))

        return questions

    def _get_question_extractor(self, question_element: WebElement) -> Callable[[WebElement], Question]:
        jscontroller = question_element.get_attribute('jscontroller')
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

    def _get_question_title(self, question_element: WebElement) -> str:
        return question_element.find_element(By.CSS_SELECTOR, selectors['question_title']).get_attribute('textContent')

    def _extract_question_with_radiobutton(self, question_element: WebElement) -> RadioButtonQuestion:
        title = self._get_question_title(question_element)
        clickable_options = question_element.find_elements(By.CSS_SELECTOR, selectors['radiobutton_option'])
        select_element = list(map(
            lambda option: {
                'label': option.find_element(By.CSS_SELECTOR, selectors['radiobutton_label']).get_attribute('textContent'),
                'element': option
            },
            clickable_options
        ))
        # print({'title': title, 'select_element': select_element})
        return RadioButtonQuestion(title, select_element=select_element)

    def _extract_question_with_checkbox(self, question_element: WebElement) -> CheckBoxQuestion:
        title = self._get_question_title(question_element)
        clickable_options = question_element.find_elements(By.CSS_SELECTOR, selectors['checkbox_option'])
        select_element = list(map(
            lambda option: {
                'label': option.get_attribute('textContent'),
                'element': option
            },
            clickable_options
        ))
        # print({'title': title, 'select_element': select_element})
        return CheckBoxQuestion(title, select_element=select_element)

    def _extract_question_with_text(self, question_element: WebElement) -> TextQuestion:
        title = self._get_question_title(question_element)
        select_element: WebElement
        try:
            select_element = question_element.find_element(By.CSS_SELECTOR, selectors['short_text'])
        except NoSuchElementException:
            select_element = question_element.find_element(By.CSS_SELECTOR, selectors['long_text'])

        # print({'title': title, 'select_element': select_element})
        return TextQuestion(title, select_element=select_element)
        

    def _extract_question_with_select(self, question_element: WebElement) -> SelectQuestion:
        title = self._get_question_title(question_element)
        
        # print({'title': title, 'select_element': question_element})
        return SelectQuestion(title, select_element=question_element)