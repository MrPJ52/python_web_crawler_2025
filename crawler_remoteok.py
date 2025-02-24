import time
import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class Job:
    def __init__(self, title, company, location, paycheck, url):
        self.title = title
        self.company = company
        self.location = location
        self.paycheck = paycheck
        self.url = url

class JobPage:
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs_list = list()
        self.url = "https://remoteok.com/remote-" + self.keyword + "-jobs"
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(self.url)
        time.sleep(2)

        last_time = time.time()
        last_height = page.evaluate('document.body.scrollHeight')
        while True:
            page.keyboard.down("End")
            current_time = time.time()
            new_height = page.evaluate('document.body.scrollHeight')
            if current_time - last_time > 3:
                new_height = page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    last_time = time.time()

        self.soup = BeautifulSoup(page.content(), "html.parser")

        p.stop()
    
    def find_jobs(self):
        jobs_raw_data = self.soup.find("table", id="jobsboard").find_all("tr", class_="job")
        cnt = 0
        err_cnt = 0
        for job in jobs_raw_data:
            try:
                title = job.find("h2", itemprop="title").text.strip()
                company = job.find("h3", itemprop = "name").text.strip()
                location = job.find("div", class_="location").text.strip()
                paycheck = job.find("div", class_="location").next_sibling.text.strip()[:-1]
                url = "https://remoteok.com"+job.find("a", class_="preventLink")["href"]
                self.jobs_list.append(Job(title, company, location, paycheck, url))
                cnt += 1
            except:
                err_cnt += 1
                continue
        
        print(f"Scraping for {self.keyword} is done.\n Found {cnt} jobs, {err_cnt} errors occured.\n")
        
    def print_jobs(self):
        print(f"Jobs for {self.keyword}:\n")
        for job_info in self.jobs_list:
            print(job_info.title)
            print(job_info.company)
            print(job_info.location, job_info.paycheck)
            print(job_info.url, "\n")
        
        print(f"total {self.keyword} jobs: {len(self.jobs_list)}\n")
    
    def export_csv(self):
        file = open("remoteok_"+self.keyword+".csv", mode="w", encoding="utf-8", newline="")
        writter = csv.writer(file)
        writter.writerow(self.jobs_list[0].__dict__.keys())

        for job_info in self.jobs_list:
            writter.writerow([job_info.title, job_info.company, job_info.location, job_info.paycheck, job_info.url])




keywords = [
    "flutter",
    "python",
    "golang"
]

for keyword in keywords:
    crawling = JobPage(keyword)
    crawling.find_jobs()
    crawling.export_csv()