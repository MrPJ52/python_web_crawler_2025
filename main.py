from flask import Flask, render_template
from crawler_wanted import Job, CrawlerWanted

app = Flask("JobScraper")

@app.route("/")
def home():
    return render_template("home.html", name = "Park")

@app.route("/testing")
def testing():
    return "Testing..."

#### if replit, run("0.0.0.0")
app.run(debug=True)