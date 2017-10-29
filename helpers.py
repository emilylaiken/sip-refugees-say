import pandas as pd
from flask import redirect, render_template, request, session, url_for
import sys

# Read sites CSV into pandas dataframe
sites = pd.read_csv('data/sites.csv')
cases = pd.read_csv('data/cases.csv')
output = pd.read_csv('data/output.csv')

# Takes refugee group's name and returns dict of relevant info.
def refugeesInfo(groupName):
    refDf = cases[cases['name'] == groupName]
    if refDf.empty:
        return None
    refugeesInfo = refDf.iloc[0].to_dict()
    languages = refDf.iloc[0]['languages']
    refugeesInfo['languages'] = languages.replace(" ", "").split(",")
    for i in range(len(output.index)):
        if output.iloc[i, 0] == groupName:
            for j in range(len(output.columns)):
                if output.iloc[i, j] == 1:
                    refugeesInfo['community'] = output.columns[j]
    return refugeesInfo

# Takes community's details (city, state) and returns dict of relevant info.
def communityInfo(city, state):
    comDf = sites[(sites['city'] == city) & (sites['state'] == state)]
    if comDf.empty:
        return None
    return comDf.iloc[0].to_dict()

# Return all communities in a dict list.
def listOfCommunities():
    comList = []
    for i in range(len(sites.index)):
        comList.append(communityInfo(sites.iloc[i]['city'],sites.iloc[i]['state']))
    return comList

# Return all refugees from a particular community in a dict list.
def listOfRefugees(city):
    refList = []
    for name in cases['name']:
        if refugeesInfo(name)['community'] == city:
            refList.append(refugeesInfo(name))
    return refList

def assign_case(groupName):
    if refugeesInfo(groupName) is None:
        return None
    else:
        return listOfCommunities[np.ranodm.rand*len(listOfCommunities)]['city']

def main():
    print(list(zip(sites['state'].values.tolist(),sites['city'].values.tolist())))

if __name__ == '__main__':
    main()




