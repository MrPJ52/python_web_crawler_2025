import time
import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


######## Job Class ########
class Job:
    def __init__(self, title, company, reward, url):
        self.title = title
        self.company = company
        self.reward = reward
        self.url = url


######## Job Crawler Class ########
class CrawlerWanted:
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs_list = list()

    ######## Find Method ########
    def find_jobs(self):
        #### Get html from website ####
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.wanted.co.kr/search?query=" + self.keyword + "&tab=position")
        time.sleep(2)

        #### Scroll to the end of Page ####
        last_time = time.time()
        last_height = page.evaluate('document.body.scrollHeight')
        while True:
            page.keyboard.down("End")
            current_time = time.time()
            new_height = page.evaluate('document.body.scrollHeight')
            # Check if there is no update in body for 3 sec
            if current_time - last_time > 3:
                new_height = page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    last_time = time.time()

        soup = BeautifulSoup(page.content(), "html.parser")

        p.stop()

        #### Find jobs data from html soup
        jobs_raw_data = soup.find_all("div", role="listitem")
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

    ######## Print Method ########
    def print_jobs(self):
        print(f"Jobs for {self.keyword}:\n")
        for job_info in self.jobs_list:
            print(job_info.title)
            print(job_info.company)
            print(job_info.reward)
            print(job_info.url, "\n")

        print(f"total {self.keyword} jobs: {len(self.jobs_list)}\n")

    ######## Export to CSV Method ########
    def export_csv(self):
        file = open("wanted_"+self.keyword+".csv", mode="w", encoding="UTF-8-sig", newline="")
        writter = csv.writer(file)
        writter.writerow(self.jobs_list[0].__dict__.keys())

        for job_info in self.jobs_list:
            writter.writerow([job_info.title, job_info.company, job_info.reward, job_info.url])


######## Testing ########
# keywords = [
#     "flutter",
#     "python",
#     "golang"
# ]

# for keyword in keywords:
#     crawling = CrawlerWanted(keyword)
#     crawling.find_jobs()
#     crawling.export_csv()