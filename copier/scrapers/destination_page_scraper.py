from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome

from typing import Callable, List
from enum import Enum
from os import path

from copier.entities.radiobutton_question import RadioButtonQuestion
from copier.entities.checkbox_question import CheckBoxQuestion
from copier.entities.select_question import SelectQuestion
from copier.entities.text_question import TextQuestion
from .abstract_scraper import AbstractScraper
from copier.entities.question import Question
from .config import selectors, jscontrollers


selectors = selectors['dest']
jscontrollers = jscontrollers['dest']

FIREFOX_DRIVER = path.join('copier', 'resources', 'geckodriver.exe')
CHROME_DRIVER = path.join('copier', 'resources', 'chromedriver.exe')

class DriverType(Enum):
    FIREFOX = 1
    CHROME = 2
        
# todo add waits for finding elements

class DestinationPageScraper(AbstractScraper):
    def __init__(self, url: str, driver_type: DriverType):
        self.driver = self.get_configured_driver(driver_type)
        self.logger.debug(f'{driver_type.name} driver requesting {url}')
        self.driver.get(url)

    @classmethod
    def get_configured_driver(cls, driver_type: DriverType):
        driver = None
        if driver_type == DriverType.FIREFOX:
            driver = Firefox(executable_path=FIREFOX_DRIVER)
            driver.maximize_window()
            
        elif driver_type == DriverType.CHROME:
            options = ChromeOptions()
            options.add_experimental_option('detach', True)
            driver = Chrome(options=options, executable_path=CHROME_DRIVER)
            driver.maximize_window()

        return driver

    def __wait_for_element_to_be_clickable(self, css_selector: str) -> None:
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )

    def extract_all_questions(self) -> List[Question]:
        question_elements = []
        try:
            question_elements = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selectors['question_element']))
            )
        except TimeoutException as e:
            self.logger.error(e)

        self.logger.debug(f'{len(question_elements)} question elements found on page')

        questions = []
        for question_element in question_elements:
            general_element = question_element.find_element(By.CSS_SELECTOR, selectors['general_div'])
            try:
                extract = self._get_question_extractor(general_element)
            except Exception as e:
                self.logger.error(e)
            else:
                questions.append(extract(question_element))

        question_elements[0].click()
        self.logger.debug(f'{len(questions)} questions extracted from page')
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

        clickable_options = []
        try:
            self.__wait_for_element_to_be_clickable(selectors['radiobutton_option'])
        except TimeoutException as e:
            self.logger.error(e)
        else:
            clickable_options = question_element.find_elements(By.CSS_SELECTOR, selectors['radiobutton_option'])

        select_element = list(map(
            lambda option: {
                'label': option.get_attribute('textContent'),
                'element': option
            },
            clickable_options
        ))
        # print({'title': title, 'select_element': select_element})
        return RadioButtonQuestion(title, select_element=select_element)

    def _extract_question_with_checkbox(self, question_element: WebElement) -> CheckBoxQuestion:
        title = self._get_question_title(question_element)

        clickable_options = []
        try:
            self.__wait_for_element_to_be_clickable(selectors['checkbox_option'])
        except TimeoutException as e:
            self.logger.error(e)
        else:
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
        try:
            self.__wait_for_element_to_be_clickable(selectors['select'])
        except TimeoutException as e:
            self.logger.error(e)
        
        # print({'title': title, 'select_element': question_element})
        return SelectQuestion(title, select_element=question_element)