from PyQt5.QtCore import QObject, QThread, pyqtSignal
from copier.ui.design import Ui_MainWindow
from PyQt5 import QtWidgets
from selenium.common.exceptions import InvalidElementStateException

from typing import List, Union
from time import sleep
import logging
import sys

from copier.scrapers.destination_page_scraper import DestinationPageScraper, DriverType
from copier.scrapers.source_page_scraper import SourcePageScraper
from copier.entities.question import Question


src_url = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewscore?viewscore=AE0zAgA4kyXwcDpvREbb0iYxBTytUwiUQPGyEMLi-8YtFxmbNBzfYTi7y55JA2YlKInu3sw'
dest_url = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewform'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, src_url: str, dest_url: str, driver_type: DriverType):
        super().__init__()
        self.src_url = src_url
        self.dest_url = dest_url
        self.driver_type = driver_type

    def run(self) -> None:
        logger.info('Extracting answers from source page...')

        src_questions = []
        try:
            src_scraper = SourcePageScraper(self.src_url)
        except TimeoutError as e:
            logger.info(e)
            self.finished.emit()
            return
        else:
            src_questions = src_scraper.extract_all_questions()
            
        logger.info(f'{len(src_questions)} source page answers are successfully extracted!')
            
        logger.info('Extracting question elements from destination page...')
        dest_scraper = DestinationPageScraper(self.dest_url, self.driver_type)
        dest_questions = dest_scraper.extract_all_questions()
        logger.info(f'{len(dest_questions)} question elements from destination page are successfully extracted!')

        logger.info('Copying answers from source page to destination page...')
        self.copy_answers(src_questions, dest_questions)
        logger.info('Answers are successfully copied!')

        logger.info('Job is done :)')
        self.finished.emit()

    def copy_answers(self, source_page_questions: List[Question], destination_page_questions: List[Question]) -> None:
        def find_question_in_list(source_page_question: Question, destination_page_questions: List[Question]) -> Union[Question, None]:
            for dest_question in destination_page_questions:
                if source_page_question == dest_question:
                    destination_page_questions.remove(dest_question)
                    return dest_question
            return None

        for src_question in source_page_questions:
            dest_question = find_question_in_list(src_question, destination_page_questions)
            if dest_question:
                try:
                    dest_question.select_answer(src_question.get_answer())
                    sleep(0.1)
                except InvalidElementStateException as e:
                    logger.info(f'An error occured: {e}. Try to run again')
                    return


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.radioButton.setChecked(True)
        self.ui.radioButton.driver = DriverType.FIREFOX
        self.ui.radioButton_2.driver = DriverType.CHROME

        self.ui.textEdit.setReadOnly(True)

        self.ui.lineEdit.setText(src_url)
        self.ui.lineEdit_2.setText(dest_url)

        self.ui.pushButton.clicked.connect(self.start_button_action)

    def get_text_edit(self) -> QtWidgets.QTextEdit:
        return self.ui.textEdit

    def get_data_from_radiobutton(self) -> DriverType:
        if self.ui.radioButton.isChecked():
            return self.ui.radioButton.driver
        if self.ui.radioButton_2.isChecked():
            return self.ui.radioButton_2.driver

    def start_button_action(self):
        src_url = self.ui.lineEdit.text()
        dest_url = self.ui.lineEdit_2.text()
        driver_type = self.get_data_from_radiobutton()

        self.thread = QThread()
        self.worker = Worker(src_url, dest_url, driver_type)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.ui.pushButton.setEnabled(False)

        self.thread.finished.connect(lambda: self.ui.pushButton.setEnabled(True))
        

class QtHandler(logging.Handler):
    def __init__(self, text_edit: QtWidgets.QTextEdit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record: logging.LogRecord) -> None:
        messsage = self.format(record)
        self.text_edit.append(messsage)


def run():
    app = QtWidgets.QApplication([])
    window = Window()

    formatter = logging.Formatter('%(asctime)s  %(message)s')

    handler = QtHandler(window.get_text_edit())
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    window.show()
    sys.exit(app.exec())