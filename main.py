import requests
from bs4 import BeautifulSoup


url = "https://weworkremotely.com/remote-full-time-jobs?page=1"

#모든 job의의 정보를 저장하는 리스트
all_jobs = list()

def scrape_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser", )

    #광고 태그 삭제
    for ads in soup.find_all("li", class_="feature--ad"):
        ads.decompose()

    #불필요한 featured, top100 태그 삭제
    for featured in soup.find_all("p", class_="new-listing__categories__category--featured"):
        featured.decompose()

    for top100 in soup.find_all("p", class_="new-listing__categories__category--top-company"):
        top100.decompose()

    #마지막 li는 back to jobs, 필요없음
    jobs_raw_data = soup.find("section", class_="jobs").find_all("li")[:-1]

    for job in jobs_raw_data:
        title = job.find("h4", class_="new-listing__header__title").text
        company =job.find("p", class_="new-listing__company-name").text
        #tooltip 바로 뒤 형제의 태그(여기선 <a>)의 href attribute
        url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]

        #categories div 전체를 str으로로 받고, 각 feature의 list로 변환
        categories = job.find("div", class_="new-listing__categories").text.split("  ")

        work_type = categories[0]
        paycheck = "Paycheck is unknown"
        region = "Region is unknown"

        #paycheck가 적혀있는 경우
        try:
            if ("$" in categories[1]):
                paycheck = categories[1]
                region = categories[2:]
            else:
                region = categories[1:]
        except:
            pass

        #각 job에 대한 데이터 dict 생성성
        job_data_dict = {
            "title": title,
            "company": company,
            "work_type" : work_type,
            "paycheck" : paycheck,
            "region" : region,
            "url" : f"https://weworkremotely.com{url}"
        }

        #데이터 dict를 all_jobs list에 추가
        all_jobs.append(job_data_dict)


def get_pages(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser", )
    try:
        return len(soup.find("div", class_="pagination").find_all("span", class_="page"))
    except:
        return 1

total_pages = get_pages(url)

for i in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={i+1}"
    scrape_page(url)


#확인용 print
# for job in all_jobs:
#     print(job["title"])
#     print(job["company"])
#     print(job["work_type"], job["paycheck"])
#     print(job["region"])
#     print(job["url"])
#     print("\n")
print(len(all_jobs))