from .question import Question, Answer, SelectElement


class CheckBoxQuestion(Question):
    def __init__(self, title: str, answer: Answer=None, select_element: SelectElement=None):
        self._title = title
        self._answer = answer
        self._select_element = select_element

    def select_answer(self, answer: Answer) -> None:
        options_to_select = list(filter(lambda option: option['label'] in answer, self._select_element))
        for opt in options_to_select:
            opt['element'].click()
