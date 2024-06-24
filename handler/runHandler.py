#Python program to get the data of a json file

import json 
import ast
import pandas as pd
import numpy
import handler.componentHandler as componentHandler

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
    components = element.get('component_instance')
    componentsDict = ast.literal_eval(components) #converts string to dict
    componentsList = []
    elem = componentsDict.get('component').get('name')
    elemCleaned = componentHandler.cleanName(elem)
    componentsList.append(elemCleaned)
    nextComponent = componentsDict.get('satisfactionOfRequiredInterfaces')
    nextComponentExists = True
    if nextComponent == {} or nextComponent == None: nextComponentExists = False
    while nextComponentExists == True:
        elem = nextComponent.get('W').get('component').get('name')
        elemCleaned = componentHandler.cleanName(elem)
        componentsList.append(elemCleaned)
        nextComponent = nextComponent.get('W').get('component').get('satisfactionOfRequiredInterfaces')
        if nextComponent == {} or nextComponent == None: nextComponentExists = False
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

run = getRunAsDF('runs/gmfs_eval.json')
print(getPerformances(run))