
from flask import Flask, redirect, render_template, request, url_for, send_file, session
import os
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
	# read sites CSV into pandas dataframe
	sites = pd.DataFrame()
	# read cases CSV into pandas dataframe
	cases = pd.DataFrame()
	# pass two dataframes to front end
	return render_template("map.html", sites=sites.to_html(), cases=cases.to_html())

# Run application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
