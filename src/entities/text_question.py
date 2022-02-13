from entities.question import Question, Answer, SelectElement


class TextQuestion(Question):

    def __init__(self, title: str, answer: Answer=None, select_element: SelectElement=None):
        self._title = title
        self._answer = answer
        self._select_element = select_element

    def select_answer(self, answer: Answer) -> None:
        self._select_element.clear()
        self._select_element.send_keys(answer)
