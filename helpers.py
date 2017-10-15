import pandas as pd
from flask import redirect, render_template, request, session, url_for
import sys

# Read sites CSV into pandas dataframe
sites = pd.read_csv('data/sites.csv')
cases = pd.read_csv('data/cases.csv')
output = pd.read_csv('data/output.csv')

# Takes refugee group's name and returns dict of relevant info
def refugeesInfo(groupName):
    languages = cases[cases["name"] == groupName].iloc[0]["languages"]
    refugeesInfo = cases[cases["name"] == groupName].iloc[0].to_dict()
    refugeesInfo["languages"] = languages.replace(" ", "").split(",")
    return refugeesInfo

# Takes community name and returns dict of relevant info
def getFromCommunity(city, state):
	rightCity = sites["city"] == city
	rightState = sites["state"] == state
	dic = sites[rightCity & rightState].to_dict(orient="index")[0]
	print(dic, file=sys.stderr)
	return dic
