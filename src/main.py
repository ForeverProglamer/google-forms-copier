from typing import List, Union
from entities.question import Question
from scrapers.source_page_scraper import SourcePageScraper
from scrapers.destination_page_scraper import DestinationPageScraper


src_url = 'https://docs.google.com/forms/d/e/1FAIpQLSf7xr53oCMl8e78yzq0zXCdSkP0YQstIqp4XFFS3Tz7GQ6eVg/viewscore?viewscore=AE0zAgBULBuL-rExQFnAzvGqM2usWMzNAwp-gHRbDMiwxuxYaOv_VIIOMY5zLHp-SM5XVio'
src_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewscore?viewscore=AE0zAgA4kyXwcDpvREbb0iYxBTytUwiUQPGyEMLi-8YtFxmbNBzfYTi7y55JA2YlKInu3sw'

dest_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewform'

def main(source_url: str, destination_url: str) -> None:
    src_scraper = SourcePageScraper(source_url)
    src_questions = src_scraper.extract_all_questions()
    print(src_questions)

    dest_scraper = DestinationPageScraper(destination_url)
    dest_questions = dest_scraper.extract_all_questions()
    print(dest_questions)

    copy_answers(src_questions, dest_questions)

def copy_answers(source_page_questions: List[Question], destination_page_questions: List[Question]) -> None:
    def find_question_in_list(source_page_question: Question, destination_page_questions: List[Question]) -> Union[Question, None]:
        for dest_question in destination_page_questions:
            if source_page_question == dest_question:
                destination_page_questions.remove(dest_question)
                return dest_question
        return None

    for src_question in source_page_questions:
        dest_question = find_question_in_list(src_question, destination_page_questions)
        if dest_question:
            dest_question.select_answer(src_question.get_answer())

        
if __name__ == '__main__':
    main(src_url2, dest_url2)
