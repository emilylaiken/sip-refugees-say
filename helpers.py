import random
import pandas as pd
import numpy as np


class MatchingAlgo:
    def __init__(self, cases, sites):
        self.cases = cases
        self.sites = sites

    # Takes community's details (city, state) and returns dict of relevant info.
    def communityInfo(self, city, state):
        comDf = self.sites[(self.sites['city'] == city) & (self.sites['state'] == state)]
        if comDf.empty:
            return None
        return comDf.iloc[0].to_dict()

    # Return all communities in a *dict dict*.
    def dictOfCommunities(self):
        comD = dict()
        for i in range(len(self.sites.index)):
            key = self.sites.iloc[i]['city'] + ", " +  self.sites.iloc[i]['state']
            comD[key] = self.communityInfo(self.sites.iloc[i]['city'], self.sites.iloc[i]['state'])
        return comD

    # Takes refugee group's name and returns dict of relevant info.
    def refugeesInfo(self):
        pass

    # Return all refugees from a particular community in a *dict dict*.
    def dictOfRefugees(self):
        pass


# Get rid of spaces in string.
def noSpace(string):
    words = string.strip().split()
    all_words = ""
    for word in words:
        all_words = all_words + word
    return all_words.lower()

def getToolTip(key):
    abbreviations={'cap':'Capacity', 'nats':'Nationalities supported', 'slang':'Staff languages', 'clang':'Community languages', 'lfs':'Large family support',
                   'sps':'Single parent support', 'num':'Number in family', 'nat':'Nationality', 'lang':'Languages spoken', 'sp':'Single Parent',
                   'score':'Community fit score'}
    return abbreviations[key]

# Randomly assigns cases to sites.
def randomize(cases, sites):
    randDictbyName, randDictbySite = dict(), dict()
    for city in sites['city']:
        key = (city, sites[sites['city'] == city].iloc[0]['state'])
        randDictbySite[key] = dict()
    for name in cases['name']:
        city = random.choice(sites['city'])
        randDictbyName[name] = city
        key = (city, sites[sites['city'] == city].iloc[0]['state'])
        randDictbySite[key][name] = None
    return randDictbyName, randDictbySite



# Placeholder for algorithm that provides real score
def randScore(groupName, groupComm):
    return random.randint(0, 100)

# Random score
def randScore():
    return random.randint(0, 100)

class RandomAlgo(MatchingAlgo):
    def __init__(self, cases, sites):
        MatchingAlgo.__init__(self, cases, sites)
        self.randDictbyName, self.randDictbySite = randomize(self.cases, self.sites)

    def refugeesInfo(self, groupName):
        refDf = self.cases[self.cases['name'] == groupName]
        if refDf.empty:
            return None
        refugeesInfo = refDf.iloc[0].to_dict()
        languages = refDf.iloc[0]['lang']
        refugeesInfo['lang'] = languages.replace(" ", "").split(",")
        #refugeesInfo['community'] = self.randDictbyName[groupName]
        refugeesInfo['score'] = randScore()
        return refugeesInfo

    def dictOfRefugees(self, city):
        key = (city, self.sites[self.sites['city'] == city].iloc[0]['state'])
        if key in self.randDictbySite:
            for name in self.randDictbySite[key]:
                self.randDictbySite[key][name] = self.refugeesInfo(name)
            return self.randDictbySite[key]
        else:
            return dict()



class CSVAlgo(MatchingAlgo):
    def __init__(self, cases, sites, output):
        MatchingAlgo.__init__(self, cases, sites)
        self.output = output

    def refugeesInfo(self, groupName):
        refDf = self.cases[self.cases['name'] == groupName]
        if refDf.empty:
            return None
        refugeesInfo = refDf.iloc[0].to_dict()
        languages = refDf.iloc[0]['lang']
        refugeesInfo['lang'] = languages.replace(" ", "").split(",")
        #for i in range(len(self.output.index)):
            #if self.output.iloc[i, 0] == groupName:
                #for j in range(len(self.output.columns)):
                    #if self.output.iloc[i, j] == 1:
                        #refugeesInfo['community'] = self.output.columns[j]
        return refugeesInfo

    def dictOfRefugees(self, city):
        refD = dict()
        #for name in self.cases['name']:
            #if self.refugeesInfo(name)['community'] == city:
                #refD[name] = self.refugeesInfo(name)
        return refD


# For testing.
def main():
    sites1 = pd.read_csv('data/sites.csv')
    cases1 = pd.read_csv('data/cases.csv')
    output1 = pd.read_csv('data/output.csv')

    csv = RandomAlgo(cases1, sites1)
    print(csv.dictOfRefugees("Los Gatos"))

if __name__ == '__main__':
    main()

