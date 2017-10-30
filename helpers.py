import random
import pandas as pd


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
        return None

    # Return all refugees from a particular community in a *dict dict*.
    def dictOfRefugees(self):
        return None

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



class RandomAlgo(MatchingAlgo):
    def __init__(self, cases, sites):
        MatchingAlgo.__init__(self, cases, sites)
        self.randDictbyName, self.randDictbySite = randomize(self.cases, self.sites)

    def refugeesInfo(self, groupName):
        refDf = self.cases[self.cases['name'] == groupName]
        if refDf.empty:
            return None
        refugeesInfo = refDf.iloc[0].to_dict()
        languages = refDf.iloc[0]['languages']
        refugeesInfo['languages'] = languages.replace(" ", "").split(",")
        refugeesInfo['community'] = self.randDictbyName[groupName]
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
        languages = refDf.iloc[0]['languages']
        refugeesInfo['languages'] = languages.replace(" ", "").split(",")
        for i in range(len(self.output.index)):
            if self.output.iloc[i, 0] == groupName:
                for j in range(len(self.output.columns)):
                    if self.output.iloc[i, j] == 1:
                        refugeesInfo['community'] = self.output.columns[j]
        return refugeesInfo

    def dictOfRefugees(self, city):
        refD = dict()
        for name in self.cases['name']:
            if self.refugeesInfo(name)['community'] == city:
                refD[name] = self.refugeesInfo(name)
        return refD


# For testing.
def main():
    sites1 = pd.read_csv('data/sites.csv')
    cases1 = pd.read_csv('data/cases.csv')
    output1 = pd.read_csv('data/output.csv')

    csv = CSVAlgo(cases1, sites1, output1)

    print(csv.refugeesInfo('Queen Finale Doshi-Velez'))
    print("")
    print(csv.communityInfo('Bismarck', 'ND'))
    print("")
    print(csv.dictOfCommunities())
    print("")
    print(csv.dictOfRefugees('Cambridge'))

if __name__ == '__main__':
    main()

