from requests import get
from bs4 import BeautifulSoup

def extract_jobs(keyword):
    # a list to store the final result
    URL = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    JOBS = []

    # get the html page from the given website
    response = get(URL)
    
    # if the result is not successful e.g. access denied or blocked
    if response.status_code != 200:
        print(response)
        print("cannot get the info")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job in jobs:
            job_posts = job.find_all("li")
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                # print(anchor['href'])
                # anchor['href']
                company_name, work_type, location = anchor.find_all("span", class_="company")
                job_title = anchor.find("span", class_="title")
                JOBS.append(
                    {
                        "link": f"https://weworkremotely.com{anchor['href']}",
                        "company": company_name.string.replace(",", ""),
                        "job_title": job_title.string.replace(",", ""),
                        "work_type": work_type.string.replace(",", ""),
                        "location": location.string.replace(",", ""),
                    }
                )
    print(JOBS)
    return JOBS