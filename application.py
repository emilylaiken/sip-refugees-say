
from flask import Flask, redirect, render_template, request, url_for, send_file, session
import os
import pandas as pd
import numpy as np
import helpers


app = Flask(__name__)

@app.route("/")
def index():
  sites_df = pd.read_csv('data/sites.csv')
  cases_df = pd.read_csv('data/cases.csv')
  output_df = pd.read_csv('data/output.csv')

  cases = cases_df['name']
  communities = list(zip(sites_df['state'].values.tolist(),sites_df['city'].values.tolist()))
  def assign_case(groupName):
    return communities[np.random.randint(0, len(communities))]
  # Make assignments, keep lists by community
  assignments_by_community = {}
  for community in communities:
    assignments_by_community[community] = []
  for case in cases:
    community = assign_case(case)
    assignments_by_community[community].append(case)
  # pass two dataframes to front end
  return render_template('index.html', communities=assignments_by_community)


# Run application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
