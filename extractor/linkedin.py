from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time



def page_scoll_job_extract(keyword):
    JOBS = []
    URL = f"https://hk.linkedin.com/jobs/search?keywords={keyword}" 
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust waiting time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    job_list = soup.find("ul", class_="jobs-search__results-list").find_all("li")
    for jobs in job_list:
        anchor = jobs.find("a")
        job_title = jobs.find("h3", class_="base-search-card__title")
        if (jobs.find("a", class_="hidden-nested-link") == None):
                company_name = jobs.find("h4", class_="base-search-card__subtitle")
        else:
            company_name = jobs.find("a", class_="hidden-nested-link")
        location = jobs.find("span", class_="job-search-card__location")

    JOBS.append(
                {
                    "link": anchor["href"],
                    "company": company_name.string.replace(",", "").strip(),
                    "job_title": job_title.string.replace(",", "").strip(),
                    "work_type": "N/A",
                    "location": location.string.replace(",", "").strip(),
                }
            )
    return JOBS

def job_extract(keyword):
    URL = f"https://hk.linkedin.com/jobs/search?keywords={keyword}"
    JOBS = []

    r = get(URL)

    if r.status_code != 200:
        print(r)
        print("cannot get the information from linked in")
    else:
        soup = BeautifulSoup(r.text, "html.parser")
        job_list = soup.find("ul", class_="jobs-search__results-list").find_all("li")
        for jobs in job_list:
            anchor = jobs.find("a")
            job_title = jobs.find("h3", class_="base-search-card__title")
            if (jobs.find("a", class_="hidden-nested-link") == None):
                company_name = jobs.find("h4", class_="base-search-card__subtitle")
            else:
                company_name = jobs.find("a", class_="hidden-nested-link")
            location = jobs.find("span", class_="job-search-card__location")

            # base-search-card__subtitle

            JOBS.append(
                {
                    "link": anchor["href"],
                    "company": company_name.string.replace(",", "").strip(),
                    "job_title": job_title.string.replace(",", "").strip(),
                    "work_type": "N/A",
                    "location": location.string.replace(",", "").strip(),
                }
            )

        return JOBS