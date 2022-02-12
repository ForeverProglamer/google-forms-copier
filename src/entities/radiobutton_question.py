from entities.question import Question, Answer, SelectElement


class RadioButtonQuestion(Question):

    def __init__(self, title: str, answer: Answer=None, select_element: SelectElement=None):
        self.title = title
        self.answer = answer
        self.select_element = select_element

    def select_answer(self, answer: Answer) -> None:
        pass
    