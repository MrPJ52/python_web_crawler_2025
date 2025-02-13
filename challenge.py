import requests
from bs4 import BeautifulSoup

keywords = [
    "flutter",
    "python",
    "golang"
]

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
        self.url = "https://remoteok.com/remote-" + self.keyword + "-jobs"
        response = requests.get(self.url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        })
        self.soup = BeautifulSoup(response.content, "html.parser")
        self.jobs_list = list()
    
    def find_jobs(self):
        jobs_raw_data = self.soup.find("table", id="jobsboard").find_all("tr", class_="job")
        for job in jobs_raw_data:
            title = job.find("h2", itemprop="title").text.strip()
            company = job.find("h3", itemprop = "name").text.strip()
            location = job.find("div", class_="location").text.strip()
            paycheck = job.find("div", class_="location").next_sibling.text.strip()[:-1]
            url = "https://remoteok.com"+job.find("a", class_="preventLink")["href"]
            self.jobs_list.append(Job(title, company, location, paycheck, url))
    
    def print_jobs(self):
        print(f"Jobs for {self.keyword}:\n")
        for job_info in self.jobs_list:
            print(job_info.title)
            print(job_info.company)
            print(job_info.location, job_info.paycheck)
            print(job_info.url, "\n")
        
        print(f"total jobs: {len(self.jobs_list)}\n")


JobPage_flutter = JobPage(keywords[0])
JobPage_flutter.find_jobs()
JobPage_flutter.print_jobs()