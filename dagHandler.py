import searchSpaceHandler

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchspace["name"].to_numpy()
allComponentFullNames = searchspace["fullName"].to_numpy()
categories = searchspace["category"].to_numpy()

x = 0
y = 0
yK = 0
iK = 1
yBS = 0
iBS = 1
yMS = 0
iMS = 1
yBM = 0
iBM = 1
yMM = 0
iMM = 1

components = []
for i in range(0, len(allComponentNames)):
    if categories[i] == "Kernel":
        x = 0
        y = yK
        if yK >= 0:
            yK = yK - iK * 60
        else:
            yK = yK + iK * 60
        iK += 1
    elif categories[i] == "BaseSLC":
        x = 300
        y = yBS
        if yBS >= 0:
            yBS = yBS - iBS * 60
        else:
            yBS = yBS + iBS * 60
        iBS += 1
    elif categories[i] == "MetaSLC":
        x = 600
        y = yMS
        if yMS >= 0:
            yMS = yMS - iMS * 60
        else:
            yMS = yMS + iMS * 60
        iMS += 1
    elif categories[i] == "BaseMLC":
        x = 900
        y = yBM
        if yBM >= 0:
            yBM = yBM - iBM * 60
        else:
            yBM = yBM + iBM * 60
        iBM += 1
    elif categories[i] == "MetaMLC":
        x = 1200
        y = yMM
        if yMM >= 0:
            yMM = yMM - iMM * 60
        else:
            yMM = yMM + iMM * 60
        iMM += 1

    components.append({'data': {'id': allComponentNames[i], 'label': allComponentNames[i]}, 'position': {'x': x, 'y': y}, 'classes': categories[i]})

connections = []
possibleComponentPartner = []

for a in range(0, len(allComponentNames)):
    temp = []
    providedInterfaces = searchspace.loc[searchspace['name'] == allComponentNames[a]]["providedInterface"].iloc[0]
    if type(providedInterfaces) is list:
        for b in range(0, len(allComponentNames)):
            requiredInterfaces = searchspace.loc[searchspace['name'] == allComponentNames[b]]["requiredInterface"].iloc[0]
            if type(requiredInterfaces) is list:
                for elemA in providedInterfaces:
                    if (elemA in requiredInterfaces or allComponentFullNames[a] in requiredInterfaces) and categories[a] != categories[b]:
                        connections.append({'data': {'id': (allComponentNames[a]+"-"+allComponentNames[b]), 'source': allComponentNames[a], 'target': allComponentNames[b], 'weight': 1}})
                        temp.append(allComponentNames[b])
    possibleComponentPartner.append(temp)

datapoints = components + connections

style = [
    {'selector': 'node', 'style': {'content': 'data(label)', 'opacity': '0'}},
    {'selector': 'edge', 'style': {'opacity': '0'}}
]


def getDatapoints():
    return datapoints


def getStyle():
    return style.copy()
