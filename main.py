from flask import Flask
from crawler_wanted import Job, CrawlerWanted

app = Flask("JobScraper")

@app.route("/")
def home():
    return "Hello, world!"

app.run(debug=True)