from abc import ABC, abstractmethod
from typing import Dict, List, Union


class Question(ABC):
    title: str
    answer: Union[str, List[Dict]]

    @abstractmethod
    def select_answer(self) -> None:
        pass
