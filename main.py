from flask import Flask, render_template
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
    return render_template("search.html")


app.run(host="0.0.0.0", debug=True)