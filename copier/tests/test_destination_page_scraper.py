import unittest

from copier.scrapers.destination_page_scraper import DestinationPageScraper, DriverType
from copier.entities.question import Question


dest_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewform'
dest_url3 = 'https://docs.google.com/forms/d/e/1FAIpQLScg4TI1LnKkAYp2joyiCT_dGAkNyp5a8IHD3HbIdbpqL4mM3w/viewform'

class TestDestinationPageScraper(unittest.TestCase):

    def test_extract_all_questions(self):
        '''Checks if return value have elements and each element type is Question'''

        def test(scraper: DestinationPageScraper):
            questions = scraper.extract_all_questions()
            self.assertNotEqual(questions, [])
            self.assertTrue(all([isinstance(q, Question) for q in questions]))

        test(DestinationPageScraper(dest_url2, DriverType.CHROME))
