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
        'DNT': '1'  # important
    }

    source = f'https://www.indeed.com/jobs?q={jobtitre}&l={ville}&radius={distance}'
    
    print(source)

    req = Request(url=source, headers=headers)
    try:
        html = urlopen(req).read()
    except Exception as e:
        print(f"Failed to retrieve webpage: {e}")
        return None
    
    soup = bs.BeautifulSoup(html, 'lxml')
    job_titles = []
    job_links = []
    job_descriptions = []
    job_companies = []
    
    for tag in soup.findAll('h2', {'class': 'jobTitle'}):
        a_tag = tag.find('a')
        if a_tag:
            job_titles.append(a_tag.get_text())
            job_links.append(f"https://www.indeed.com{a_tag.get('href')}")
            description = scrape_job_description(a_tag.get('href'))
            job_descriptions.append(description)
            company = scrapCompagnie(a_tag.get('href'))
            job_companies.append(company)
    jobs_data = {
        'Titles': job_titles,
        'Links': job_links,
        'Descriptions': job_descriptions,
        'Companies': job_companies
    }
    return jobs_data
           
           

# pour la desc
def scrape_job_description(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1' 
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

# pour la compagnie
def scrapCompagnie(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1' 
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

# return the resultat of the search in json object to the front
