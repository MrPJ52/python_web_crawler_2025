from flask import Flask, render_template, request
from crawler_wanted import Job, CrawlerWanted

app = Flask("JobScrapper")


db = dict()


@app.route("/")
def home():
    return render_template("home.html", name = "Park")

@app.route("/testing")
def testing():
    return "Testing..."

@app.route("/search")
def search():
    keyword = request.args.get("keyword")

    if keyword in db:
        jobs_list = db[keyword]
    else:
        crawler = CrawlerWanted(keyword)
        crawler.find_jobs()
        jobs_list = crawler.jobs_list
        db[keyword] = jobs_list
    
    return render_template("search.html", keyword = keyword, jobs = jobs_list)


app.run(host="0.0.0.0", debug=True)