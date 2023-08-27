from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# browser.execute_script("window.scrollBy(0, window.innerHeight);")
def job_extract(KEYWORD):
    CONTENT_NUM = 0
    JOBS = []
    while True:
        url = f"https://hk.indeed.com/jobs?q={KEYWORD}&start={CONTENT_NUM}"

        options = Options()
        browser = webdriver.Chrome(options=options)
        browser.get(url)

        wait = WebDriverWait(browser, 10)  # Maximum wait time of 10 seconds
        element = wait.until(EC.visibility_of_element_located((By.ID, 'mosaic-provider-jobcards')))        

        soup = BeautifulSoup(browser.page_source, "html.parser")
        li = soup.find_all("li", class_="css-5lfssm eu4oa1w0")
        for i in li:
            table = i.find("table", class_="jobCard_mainContent big6_visualChanges")
            if (table != None):
                content = table.find("td", class_="resultContent")
                link = f"https://www.indeed.com{content.find('a')['href']}"
                job_title = content.find("span").string
                location = content.find("div", class_="companyLocation").string
                company = content.find("span", class_="companyName").string
                work_type = content.find("div", class_="attribute_snippet")
                
                if work_type == None:
                    work_type = "N/A"
                else: work_type = work_type.string

                JOBS.append(
                            {
                                "link": link.replace(",", "").strip(),
                                "company": company.replace(",", "").strip(),
                                "job_title": job_title.replace(",", "").strip(),
                                "work_type": str(work_type).replace(",", "").strip(),
                                "location": str(location).replace(",", "").strip(),
                            }
                        )
        # find the arrow button ("pagination-next-button") in the page.
        pagination_arrow = soup.find("nav", class_="css-jbuxu0 ecydgvn0").find_all("div")[-1]
        if not (pagination_arrow.find("a") == None):
            CONTENT_NUM = CONTENT_NUM + 10
        else:
            break

    print(JOBS)
    return JOBS
    # print(soup.find("div", id_="mosaic-jobResults"))