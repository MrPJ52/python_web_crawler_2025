import time
import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class Job:
    def __init__(self, title, company, reward, url):
        self.title = title
        self.company = company
        self.reward = reward
        self.url = url


class JobPageWanted:
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs_list = list()

        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.wanted.co.kr/search?query=" + self.keyword + "&tab=position")
        time.sleep(2)

        last_time = time.time()
        last_height = page.evaluate('document.body.scrollHeight')
        while True:
            page.keyboard.down("End")
            current_time = time.time()
            new_height = page.evaluate('document.body.scrollHeight')
            if current_time - last_time > 1:
                new_height = page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    last_time = time.time()

        self.soup = BeautifulSoup(page.content(), "html.parser")

        p.stop()

    def find_jobs(self):
        jobs_raw_data = self.soup.find_all("div", role="listitem")
        cnt = 0
        err_cnt = 0
        for job in jobs_raw_data:
            try:
                title = job.find("strong", class_="JobCard_title__HBpZf").text.strip()
                company = job.find("span", class_="JobCard_companyName__N1YrF").text.strip()
                reward = job.find("span", class_="JobCard_reward__cNlG5").text.strip()
                url = "https://www.wanted.co.kr" + job.find("a")["href"]
                self.jobs_list.append(Job(title, company, reward, url))
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
            print(job_info.reward)
            print(job_info.url, "\n")

        print(f"total {self.keyword} jobs: {len(self.jobs_list)}\n")

    def export_csv(self):
        file = open("jobs_for_"+self.keyword+".csv", mode="w", encoding="utf-8", newline="")
        writter = csv.writer(file)
        writter.writerow(self.jobs_list[0].__dict__.keys())

        for job_info in self.jobs_list:
            writter.writerow([job_info.title, job_info.company, job_info.reward, job_info.url])

    
job_page_flutter = JobPageWanted("flutter")
job_page_flutter.find_jobs()
job_page_flutter.export_csv()

job_page_python = JobPageWanted("python")
job_page_python.find_jobs()
job_page_python.export_csv()