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
    parameterValues = []
    performance = []
    exceptions = []
    
    for element in data:
        elemTimestamp = getTimestamp(element)
        timestamps.append(elemTimestamp)
        elemComponents, elemParameterValues = getComponents(element)
        components.append(elemComponents)
        parameterValues.append(elemParameterValues)
        elemPerformance = getPerformanceValue(element)
        performance.append(elemPerformance)
        elementException = getException(element)
        exceptions.append(elementException)
    
    pandaData = {"timestamp": timestamps, 
                 "components": components,
                 "parameterValues": parameterValues,
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
    components, parameterValues = getComponents(element)
    print("components:", components)
    print("parameterValues:", parameterValues)
    #if len(components) != 2: print(components)
    performance = getPerformanceValue(element)
    print("performance:", performance)
    exception = getException(element)
    print("exception:", exception)

def getComponents(element):
    componentsList = []
    parameterValues = []
    label = ''
    if element == None: return componentsList
    components = element.get('component_instance')
    componentsDict = ast.literal_eval(components.replace("null", "None")) #converts string to dict
    elem = componentsDict.get('component').get('name')
    parameter = componentsDict.get('parameterValues')
    if elem == None or elem == {}: return componentsList
    elemCleaned = componentHandler.cleanName(elem)
    componentsList.append(elemCleaned)
    parameterValues.append(parameter)
    nextComponent = componentsDict.get('satisfactionOfRequiredInterfaces')
    nextComponentExists = True
    if nextComponent == {} or nextComponent == None: nextComponentExists = False
    else: label = str(nextComponent)[2] #info if we need W or B
    while nextComponentExists == True:
        elem = nextComponent.get(label).get('component').get('name')
        elemCleaned = componentHandler.cleanName(elem)
        componentsList.append(elemCleaned)
        parameter = nextComponent.get(label).get('parameterValues')
        parameterValues.append(parameter)
        nextComponent = nextComponent.get(label).get('satisfactionOfRequiredInterfaces')
        if nextComponent == {} or nextComponent == None: nextComponentExists = False
        else: label = str(nextComponent)[2]
    return componentsList, parameterValues

def isSolutionValid(componentsList, searchspace):
    valid = True
    allCategories = []
    for elem in componentsList:
        info = searchspace.loc[searchspace['name'] == elem]
        category = info.iat[0,0]
        allCategories.append(category)
    if len(set(allCategories)) != len(allCategories):
        valid = False
    return valid

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

def getAllExceptions(run):
    exceptions = run["exceptions"].to_numpy()
    return exceptions

def getAllTimestamps(run):
    timestamps = run["timestamp"].to_numpy()
    return timestamps

def getAllParameterValues(run):
    parameterValues = run["parameterValues"].to_numpy()
    return parameterValues

def getRunLength(runname):
    run = getRunAsDF(runname)
    length = len(run.index)
    return length

def getSolutionDetails(runname, timestep):
    run = getRunAsDF(runname)
    timestamp = None
    components = None
    parameterValues = None
    performance = None
    exceptions = None
    
    allTimestamps = getAllTimestamps(run)
    allSolutions = getAllComponentSolutions(run)
    allParameterValues = getAllParameterValues(run)
    allPerformances = getPerformances(run)
    allExceptions = getAllExceptions(run)
    
    
    if timestep != 0:
        timestamp = allTimestamps[timestep-1]
        components = allSolutions[timestep-1]
        parameterValues = allParameterValues[timestep-1]
        performance = allPerformances[timestep-1]
        exceptions = allExceptions[timestep-1]
        
    
    return timestamp, components, parameterValues, performance, exceptions

######################## This part can be deleted, i just tested a few things and used the code for debugging #####################################
#runname = 'runs/best_first_747_4h.json'
#runname = 'runs/bohb_eval_407.json'
#runname = 'runs/random_eval_138.json'
#run = getRunAsDF(runname)
#printSearchrun(runname)
#print(run)
#print(getRunLength(run))
#run.to_excel("table.xlsx")
#comp = getAllComponentSolutions(run)
#print(comp)
#print(getPerformances(run))

def percentageValidtoIncorrect():
    import searchSpaceHandler
    searchspace = searchSpaceHandler.getSearchSpaceAsDF()
    runnames = ["runs/best_first_747_4h.json", "runs/bohb_eval_407.json", "runs/bohb_eval_409.json", "runs/ggp_eval_407.json", "runs/ggp_eval_409.json", "runs/gmfs_eval.json", "runs/gmfs_eval_407.json", "runs/gmfs_eval_409.json", "runs/hblike_eval_786.json", "runs/hblike_eval_811.json", "runs/random_eval_138.json", "runs/random_eval_151.json"]
    for elem in runnames:
        print(elem)
        run = getRunAsDF(elem)
        comp = getAllComponentSolutions(run)
        validSolutions = 0
        falseSolutions = 0
        for elem in comp:
            valid = isSolutionValid(elem, searchspace)
            if valid: validSolutions += 1
            else: falseSolutions += 1
        print("valid solutions: " + str(validSolutions))
        print("incorrect solutions: " + str(falseSolutions))
        score = falseSolutions / (falseSolutions + validSolutions)
        print("percentage of incorrect solutions: " + str(score))
        print("\n")

percentageValidtoIncorrect()