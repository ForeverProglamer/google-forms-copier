from scrapers.source_page_scraper import SourcePageScraper
from scrapers.destination_page_scraper import DestinationPageScraper


src_url = 'https://docs.google.com/forms/d/e/1FAIpQLSf7xr53oCMl8e78yzq0zXCdSkP0YQstIqp4XFFS3Tz7GQ6eVg/viewscore?viewscore=AE0zAgBULBuL-rExQFnAzvGqM2usWMzNAwp-gHRbDMiwxuxYaOv_VIIOMY5zLHp-SM5XVio'
src_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewscore?viewscore=AE0zAgA4kyXwcDpvREbb0iYxBTytUwiUQPGyEMLi-8YtFxmbNBzfYTi7y55JA2YlKInu3sw'

dest_url2 = 'https://docs.google.com/forms/d/e/1FAIpQLScxIXHLGMp1Yq8GG3AfhYTRBxRTHTzDpzkbCDvLYe60_JArXA/viewform'

if __name__ == '__main__':
    src_scraper = SourcePageScraper(src_url2)
    source_questions = src_scraper.extract_all_questions()
    print(source_questions)
                   
    # dest_scraper = DestinationPageScraper(dest_url2)
    # dest_questions = dest_scraper.extract_all_questions()