from flask import Flask, render_template, request
from crawler_wanted import Job, CrawlerWanted

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("home.html", name = "Park")

@app.route("/testing")
def testing():
    return "Testing..."

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    crawler = CrawlerWanted(keyword)
    crawler.find_jobs()
    jobs_list = crawler.jobs_list
    return render_template("search.html", keyword = keyword, jobs = jobs_list)


app.run(host="0.0.0.0", debug=True)