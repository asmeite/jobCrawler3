from django.core.management.base import BaseCommand
from jobs.crawler import scrape_and_save_jobs

class Command(BaseCommand):
    help = 'Crawl jobs from Indeed'

    def handle(self, *args, **kwargs):
        results = scrape_and_save_jobs()
        if results is not None:
            print("Scraping successful!")
            print(results)
        else:
            print("Scraping failed.")
