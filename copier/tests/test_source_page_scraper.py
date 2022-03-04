import unittest
from copier.scrapers.source_page_scraper import SourcePageScraper
from copier.entities.question import Question


src_url = 'https://docs.google.com/forms/d/e/1FAIpQLSf7xr53oCMl8e78yzq0zXCdSkP0YQstIqp4XFFS3Tz7GQ6eVg/viewscore?viewscore=AE0zAgBULBuL-rExQFnAzvGqM2usWMzNAwp-gHRbDMiwxuxYaOv_VIIOMY5zLHp-SM5XVio'
src_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewscore?viewscore=AE0zAgA4kyXwcDpvREbb0iYxBTytUwiUQPGyEMLi-8YtFxmbNBzfYTi7y55JA2YlKInu3sw'
src_url3 = 'https://docs.google.com/forms/d/e/1FAIpQLScg4TI1LnKkAYp2joyiCT_dGAkNyp5a8IHD3HbIdbpqL4mM3w/viewscore?viewscore=AE0zAgD7ykSXnlZ3OQzufmnH7mxSQzxCSVm0ehdcx2qOjqGvy-hulSUY-shiEMH7CMgt_mU'

class TestSourcePageScraper(unittest.TestCase):

    def test_extract_all_questions(self):
        '''Return value is not empty list and each element type is Question'''

        def test(scraper: SourcePageScraper) -> None:
            questions = scraper.extract_all_questions()
            self.assertNotEqual(questions, [])
            self.assertTrue(all([isinstance(q, Question) for q in questions]))

        test(SourcePageScraper(src_url2))
        test(SourcePageScraper(src_url3))
