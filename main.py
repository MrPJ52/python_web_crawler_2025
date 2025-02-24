from flask import Flask, render_template, request, redirect, send_file
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
    try:
        #### Keep the keyword small letter without space character
        keyword = request.args.get("keyword").strip().lower()
        if keyword == "":
            raise
    #### Error occurs when keyword is "" or None
    except:
        return redirect("/")

    #### Find Database first to make website faster
    if keyword in db:
        jobs_list = db[keyword]
    else:
        crawler = CrawlerWanted(keyword)
        crawler.find_jobs()
        jobs_list = crawler.jobs_list
        db[keyword] = jobs_list
    
    return render_template("search.html", keyword = keyword, jobs = jobs_list)

@app.route("/export")
def export():
    try:
        keyword = request.args.get("keyword").strip().lower()
        if keyword == "":
            raise
    except:
        return redirect("/")
    
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    crawler = CrawlerWanted(keyword)
    crawler.jobs_list = db[keyword]
    crawler.export_csv()
    return send_file("wanted_"+keyword+".csv", as_attachment=True)


app.run(host="0.0.0.0", debug=True)