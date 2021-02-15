import numpy as np
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    mars_dict = client.mars_db.mars.find_one()
    return render_template("index.html", mars_dict = mars_dict)


@app.route("/scrape")
def scraper():
    scrape_dict = scrape_mars.scrape()


    # Connect to a database. Will create one if not already available.
    db = client.mars_db

    # Drops collection if available to remove duplicates
    db.mars.drop()
    # Creates a collection in the database and inserts two documents
    db.mars.insert_one(
        scrape_dict
    )
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)