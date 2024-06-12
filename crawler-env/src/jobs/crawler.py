# jobs/crawler.py

import bs4 as bs
from urllib.request import urlopen, Request
from .models import Job

def scrape_and_save_jobs(ville, jobtitre, distance):
    print("coucou")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'  # Do Not Track Request Header
    }

    source = 'https://www.indeed.com/jobs?q={jobtitre}t&l={ville}&radius={distance}'
    
    print(source)

    req = Request(url=source, headers=headers)
    try:
        html = urlopen(req).read()
    except Exception as e:
        print(f"Failed to retrieve webpage: {e}")
        return None
    
    soup = bs.BeautifulSoup(html, 'lxml')
    
    for tag in soup.findAll('h2', {'class': 'jobTitle'}):
        a_tag = tag.find('a')
        if a_tag:
            job_title = a_tag.get_text()
            job_link = a_tag.get('href')
            description = scrape_job_description(job_link)
            company = scrapCompagnie(job_link)
            job = Job(title=job_title, company=company, location="", description=description, url=f"https://www.indeed.com{job_link}")
            job.save()
            print(f"Job saved to database: {job}")

def scrape_job_description(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'  # Do Not Track Request Header
    }
    try:
        req = Request(url='https://www.indeed.com'+link, headers=headers)
        html = urlopen(req).read()
        soup = bs.BeautifulSoup(html, 'html.parser')
        description = soup.find('div', class_='jobsearch-JobComponent-description css-16y4thd eu4oa1w0').get_text(separator=' ')
        return description
    except Exception as e:
        print(f"Failed to retrieve job description: {e}")
        return 'No description'

def scrapCompagnie(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'  # Do Not Track Request Header
    }
    try:
        req = Request(url='https://www.indeed.com'+link, headers=headers)
        html = urlopen(req).read()
        soup = bs.BeautifulSoup(html, 'html.parser')
        company = soup.find('a', class_='css-1ioi40n e19afand0').get_text()
        return company
    except Exception as e:
        print(f"Failed to retrieve job company: {e}")
        return 'No company'
