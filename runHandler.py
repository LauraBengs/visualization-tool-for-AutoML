#Python program to get the data of a json file

import json 
import ast
import pandas as pd
import numpy
import componentHandler

def getRunAsDF(runname):
    jsonFile = open(runname) 
    convertedFile = json.load(jsonFile) #converts data of json file into a ?list?
    data = convertedFile[2].get('data')
    jsonFile.close()
    
    timestamps = []
    components = []
    performance = []
    exceptions = []
    
    for element in data:
        elemTimestamp = getTimestamp(element)
        timestamps.append(elemTimestamp)
        elemComponents = getComponents(element)
        #print(elemComponents)
        #print("---------------")
        components.append(elemComponents)
        elemPerformance = getPerformanceValue(element)
        performance.append(elemPerformance)
        elementException = getException(element)
        exceptions.append(elementException)
    
    pandaData = {"timestamp": timestamps, 
                 "components": components,
                 "performance": performance,
                 "exceptions": exceptions}
    
    run = pd.DataFrame(pandaData)
    return run

def printSearchrun(runname):
    jsonFile = open(runname) 
    convertedFile = json.load(jsonFile) #converts data of json file into a ?list?
    data = convertedFile[2].get('data')
    for element in data:
        printElement(element)
        print("--------------------------------------------------------------")
    
def printElement(element):
    timestamp = getTimestamp(element)
    print("timestamp:", timestamp)
    components = getComponents(element)
    print("components:", components)
    #if len(components) != 2: print(components)
    performance = getPerformanceValue(element)
    print("performance:", performance)
    exception = getException(element)
    print("exception:", exception)

def getComponents(element):
    componentsList = []
    label = ''
    if element == None: return componentsList
    components = element.get('component_instance')
    componentsDict = ast.literal_eval(components.replace("null", "None")) #converts string to dict
    elem = componentsDict.get('component').get('name')
    if elem == None or elem == {}: return componentsList
    elemCleaned = componentHandler.cleanName(elem)
    componentsList.append(elemCleaned)
    nextComponent = componentsDict.get('satisfactionOfRequiredInterfaces')
    nextComponentExists = True
    if nextComponent == {} or nextComponent == None: nextComponentExists = False
    else: label = str(nextComponent)[2] #info if we need W or B
    while nextComponentExists == True:
        elem = nextComponent.get(label).get('component').get('name')
        elemCleaned = componentHandler.cleanName(elem)
        componentsList.append(elemCleaned)
        nextComponent = nextComponent.get(label).get('satisfactionOfRequiredInterfaces')
        if nextComponent == {} or nextComponent == None: nextComponentExists = False
        else: label = str(nextComponent)[2]
    return componentsList

def getTimestamp(element):
    return element.get('timestamp_found')

def getPerformanceValue(element):
    return element.get('eval_value')

def getException(element):
    return element.get('exception')

def getAllComponentSolutions(run):
    solutions = run["components"].to_numpy()
    return solutions

def getPerformances(run):
    performances = run["performance"].to_numpy()
    return performances

def getRunLength(run):
    length = len(run.index)
    return length

#run = getRunAsDF('runs/best_first_747_4h.json')
#run = getRunAsDF('runs/bohb_eval_407.json')
#print(run)
#print(getRunLength(run))
#run.to_excel("table.xlsx")
#comp = getAllComponentSolutions(run)
#print(comp)
#print(getPerformances(run))