import searchSpaceHandler
import matplotlib as mpl
import numpy as np

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

distance = 50

components = []
for i in range(0, len(allComponentNames)):
    if categories[i] == "kernel":
        x = 0
        y = yK
        if yK >= 0:
            yK = yK - iK * distance
        else:
            yK = yK + iK * distance
        iK += 1
    elif categories[i] == "baseSLC":
        x = 350
        y = yBS
        if yBS >= 0:
            yBS = yBS - iBS * distance
        else:
            yBS = yBS + iBS * distance
        iBS += 1
    elif categories[i] == "metaSLC":
        x = 700
        y = yMS
        if yMS >= 0:
            yMS = yMS - iMS * distance
        else:
            yMS = yMS + iMS * distance
        iMS += 1
    elif categories[i] == "baseMLC":
        x = 1050
        y = yBM
        if yBM >= 0:
            yBM = yBM - iBM * distance
        else:
            yBM = yBM + iBM * distance
        iBM += 1
    elif categories[i] == "metaMLC":
        x = 1400
        y = yMM
        if yMM >= 0:
            yMM = yMM - iMM * distance
        else:
            yMM = yMM + iMM * distance
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

stylesheetSearchspace = [{'selector': 'node', 'style': {'content': 'data(label)'}},
                         {'selector': '.kernel', 'style': {'background-color': '#EC9F05'}},
                         {'selector': '.baseSLC', 'style': {'background-color': '#4A6C6F'}},
                         {'selector': '.metaSLC', 'style': {'background-color': '#A1C084'}},
                         {'selector': '.baseMLC', 'style': {'background-color': '#A63446'}},
                         {'selector': '.metaMLC', 'style': {'background-color': '#D89A9E'}},
                         {'selector': 'edge', 'style': {'line-color': '#adaaaa'}}]


def getDatapoints():
    return datapoints


def getStyle():
    return style.copy()


def colorFader(c1, c2, mix=0):
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def getNodeColor(solPerformance, minimisation):
    if minimisation:
        color = colorFader('lightskyblue', 'darkblue', solPerformance)
    else:
        color = colorFader('yellow', 'darkred', solPerformance)
    return color
