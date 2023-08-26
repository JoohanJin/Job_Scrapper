from requests import get
from bs4 import BeautifulSoup

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
        print(JOBS)
        return JOBS