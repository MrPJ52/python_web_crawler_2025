from flask import Flask, render_template, request, redirect, send_file
from crawler_wanted import Job, CrawlerWanted

app = Flask("JobScrapper")
app.config["JSON_AS_ASCII"] = False

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
    
    if (keyword == "") or (keyword == None):
        return redirect("/")


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
    keyword = request.args.get("keyword")
    
    if (keyword == "") or (keyword == None):
        return redirect("/")
    
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")

    crawler = CrawlerWanted(keyword)
    crawler.jobs_list = db[keyword]
    crawler.export_csv()
    return send_file("wanted_"+keyword+".csv", as_attachment=True)


app.run(host="0.0.0.0", debug=True)