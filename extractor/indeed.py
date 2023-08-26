from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options.add_experimental_option("detach", True)
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
#https://hk.indeed.com/jobs?q=python&start=10&pp=gQAPAAABiid85vsAAAACDmaOxgAxAQA-Yl1y9MRpve8jSyz9i--w3JVrye4Y7Ktj8KyBxr2r9MrssSAbagEN6j0HWbKiqgAA&vjk=143af0481f9e5720
# KEYWORD = "Python"
# CONTENT_NUM = 0
# url = f"https://hk.indeed.com/jobs?q={KEYWORD}&start={CONTENT_NUM}"

# options = Options()
# browser = webdriver.Chrome(options=options)
# browser.get(url)

# wait = WebDriverWait(browser, 10)  # Maximum wait time of 10 seconds
# element = wait.until(EC.visibility_of_element_located((By.ID, 'mosaic-provider-jobcards')))

# soup = BeautifulSoup(browser.page_source, "html.parser")
# pagination_arrow = soup.find("nav", class_="css-jbuxu0 ecydgvn0").find_all("div")[-1]#.find_all("div", class_="css-tvvxwd ecydgvn1")[-1].find("a")
# print(pagination_arrow)



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
                
                # print(link)
                # print(job_title)
                # print(location)
                # print(company)
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
        pagination_arrow = soup.find("nav", class_="css-jbuxu0 ecydgvn0").find_all("div")[-1]
        if not (pagination_arrow.find("a") == None):
            CONTENT_NUM = CONTENT_NUM + 10
        else:
            break

    print(JOBS)
    return JOBS
    # print(soup.find("div", id_="mosaic-jobResults"))