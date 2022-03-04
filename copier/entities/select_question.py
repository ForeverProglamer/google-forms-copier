from .question import Question, Answer, SelectElement
from copier.scrapers.config import selectors
from selenium.webdriver.common.by import By


selectors = selectors['dest']

class SelectQuestion(Question):
    def __init__(self, title: str, answer: Answer=None, select_element: SelectElement=None):
        self._title = title
        self._answer = answer
        self._select_element = select_element

    def select_answer(self, answer: Answer) -> None:
        clickable_select = self._select_element.find_element(By.CSS_SELECTOR, selectors['select'])
        clickable_select.click()
        options = self._select_element.find_elements(By.CSS_SELECTOR, selectors['select_option'])
        options_with_labels = list(map(
            lambda opt: {
                'label': opt.find_element(By.CSS_SELECTOR, selectors['select_label']).text,
                'element': opt
            },
            options
        ))
        try:
            option_to_select = next(filter(lambda opt: opt['label'] == answer, options_with_labels))
        except StopIteration:
            pass
        else:
            option_to_select['element'].click()
