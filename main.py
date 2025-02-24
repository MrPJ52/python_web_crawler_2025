from crawler_wanted import Job, CrawlerWanted


keywords = [
    "flutter",
    "python",
    "golang"
]

for keyword in keywords:
    crawling = CrawlerWanted(keyword)
    crawling.find_jobs()
    crawling.export_csv()