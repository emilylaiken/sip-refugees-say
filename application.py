from flask import Flask, redirect, render_template, request, url_for, send_file, session
import os
import pandas as pd
import numpy as np
import helpers
import json


app = Flask(__name__)

sites = pd.read_csv('data/sites.csv')
cases = pd.read_csv('data/cases.csv')
output = pd.read_csv('data/output.csv')

@app.route("/")
def index():
  # Assign by output.csv:
  csvAssignment = helpers.CSVAlgo(cases, sites, output)
  DictbySite = dict()
  for city in sites['city']:
    key = (city, sites[sites['city'] == city].iloc[0]['state'])
    DictbySite[key] = csvAssignment.dictOfRefugees(city)
  csvCommInfo = csvAssignment.dictOfCommunities()

  # Assign randomly:
  randomAssignment = helpers.RandomAlgo(cases, sites)
  for city in sites['city']:
    randomAssignment.dictOfRefugees(city)
  randAssignmentsByCommunity = randomAssignment.randDictbySite
  randCommInfo = randomAssignment.dictOfCommunities()
  commList = []
  for k, v in randCommInfo.items():
      commList.append(v['city'])

  # For CSV assignment: communities=DictbySite, comminfo=csvCommInfo
  # For random assignment: communities=randAssignmentsByCommunity, comminfo=randCommInfo
  return render_template('index.html', communities=randAssignmentsByCommunity, comminfo=randCommInfo, jCommList=json.dumps(commList))


# Run application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.jinja_env.filters['noSpace'] = helpers.noSpace
    app.run(host='0.0.0.0', port=port, debug=False)
