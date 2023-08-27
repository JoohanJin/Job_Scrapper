from extractor.wwr import extract_jobs as wwrEx
from extractor.linkedin import page_scoll_job_extract as lkEx
from extractor.indeed import job_extract as indeedEx

keyword = input("What do you want to search for?: ")

wwr_jobs = wwrEx(keyword)
lkd_jobs = lkEx(keyword)
indeed_jobs = indeedEx(keyword)
jobs = wwr_jobs + lkd_jobs + indeed_jobs

file = open(f"{keyword}.csv", "w")
file.write("Position,Company,Location,Job_Type,URL\n")
for job in jobs:
    file.write(f"\"{job['job_title']}\",\"{job['company']}\",\"{job['location']}\",\"{job['work_type']}\",\"{job['link']}\"\n")

file.close()