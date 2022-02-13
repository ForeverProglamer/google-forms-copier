from entities.question import Question, Answer, SelectElement


class RadioButtonQuestion(Question):

    def __init__(self, title: str, answer: Answer=None, select_element: SelectElement=None):
        self._title = title
        self._answer = answer
        self._select_element = select_element

    def select_answer(self, answer: Answer) -> None:
        option_to_select = next(filter(lambda option: option['label'] == answer, self._select_element))
        option_to_select['element'].click()
    