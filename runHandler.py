#Python program to get the data of a json file

import json 
import ast
import pandas as pd
import numpy
import componentHandler

pd.set_option('display.max_columns', 500)

def getRunAsDF(data, searchspace):
    timestamps = []
    components = []
    parameterValues = []
    performance = []
    exceptions = []
    valid = []
    measure = []
    evalReportExists = []
    evalTime_nList = []
    FMicroAvg_nList = []
    ExactMatch_nList = []
    FMacroAvgD_nList = []
    FMacroAvgL_nList = []
    evalTime_maxList = []
    evalTime_minList = []
    FMicroAvg_maxList = []
    FMicroAvg_minList = []
    HammingLoss_nList = []
    evalTime_meanList = []
    ExactMatch_maxList = []
    ExactMatch_minList = []
    FMacroAvgD_maxList = []
    FMacroAvgD_minList = []
    FMacroAvgL_maxList = []
    FMacroAvgL_minList = []
    FMicroAvg_meanList = []
    JaccardIndex_nList = []
    ExactMatch_meanList = []
    FMacroAvgD_meanList = []
    FMacroAvgL_meanList = []
    HammingLoss_maxList = []
    HammingLoss_minList = []
    evalTime_medianList = []
    FMicroAvg_medianList = []
    HammingLoss_meanList = []
    JaccardIndex_maxList = []
    JaccardIndex_minList = []
    ExactMatch_medianList = []
    FMacroAvgD_medianList = []
    FMacroAvgL_medianList = []
    JaccardIndex_meanList = []
    HammingLoss_medianList = []
    JaccardIndex_medianList = []
    
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
        isValid = isSolutionValid(elemComponents, searchspace)
        valid.append(isValid)
        elementMeasure = getMeasure(element)
        measure.append(elementMeasure)
        evalReportExist, evalTime_n, FMicroAvg_n, ExactMatch_n, FMacroAvgD_n, FMacroAvgL_n, evalTime_max, evalTime_min, FMicroAvg_max, FMicroAvg_min, HammingLoss_n, evalTime_mean, ExactMatch_max, ExactMatch_min, FMacroAvgD_max, FMacroAvgD_min, FMacroAvgL_max, FMacroAvgL_min, FMicroAvg_mean, JaccardIndex_n, ExactMatch_mean, FMacroAvgD_mean, FMacroAvgL_mean, HammingLoss_max, HammingLoss_min, evalTime_median, FMicroAvg_median, HammingLoss_mean, JaccardIndex_max, JaccardIndex_min, ExactMatch_median, FMacroAvgD_median, FMacroAvgL_median, JaccardIndex_mean, HammingLoss_median, JaccardIndex_median = getEvalReport(element)
        evalReportExists.append(evalReportExist)
        evalTime_nList.append(evalTime_n)
        FMicroAvg_nList.append(FMicroAvg_n)
        ExactMatch_nList.append(ExactMatch_n)
        FMacroAvgD_nList.append(FMacroAvgD_n)
        FMacroAvgL_nList.append(FMacroAvgL_n)
        evalTime_maxList.append(evalTime_max)
        evalTime_minList.append(evalTime_min)
        FMicroAvg_maxList.append(FMicroAvg_max)
        FMicroAvg_minList.append(FMicroAvg_min)
        HammingLoss_nList.append(HammingLoss_n)
        evalTime_meanList.append(evalTime_mean)
        ExactMatch_maxList.append(ExactMatch_max)
        ExactMatch_minList.append(ExactMatch_min)
        FMacroAvgD_maxList.append(FMacroAvgD_max)
        FMacroAvgD_minList.append(FMacroAvgD_min)
        FMacroAvgL_maxList.append(FMacroAvgL_max)
        FMacroAvgL_minList.append(FMacroAvgL_min)
        FMicroAvg_meanList.append(FMicroAvg_mean)
        JaccardIndex_nList.append(JaccardIndex_n)
        ExactMatch_meanList.append(ExactMatch_mean)
        FMacroAvgD_meanList.append(FMacroAvgD_mean)
        FMacroAvgL_meanList.append(FMacroAvgL_mean)
        HammingLoss_maxList.append(HammingLoss_max)
        HammingLoss_minList.append(HammingLoss_min)
        evalTime_medianList.append(evalTime_median)
        FMicroAvg_medianList.append(FMicroAvg_median)
        HammingLoss_meanList.append(HammingLoss_mean)
        JaccardIndex_maxList.append(JaccardIndex_max)
        JaccardIndex_minList.append(JaccardIndex_min)
        ExactMatch_medianList.append(ExactMatch_median)
        FMacroAvgD_medianList.append(FMacroAvgD_median)
        FMacroAvgL_medianList.append(FMacroAvgL_median)
        JaccardIndex_meanList.append(JaccardIndex_mean)
        HammingLoss_medianList.append(HammingLoss_median)
        JaccardIndex_medianList.append(JaccardIndex_median)
        
    pandaData = {"timestamp": timestamps, 
                 "components": components,
                 "parameterValues": parameterValues,
                 "performance": performance,
                 "exceptions": exceptions,
                 "valid": valid,
                 "measure": measure,
                 "evalReportExists": evalReportExists,
                 "evalTime_nList": evalTime_nList,
                 "FMicroAvg_nList": FMicroAvg_nList,
                 "ExactMatch_nList": ExactMatch_nList,
                 "FMacroAvgD_nList": FMacroAvgD_nList,
                 "FMacroAvgL_nList": FMacroAvgL_nList,
                 "evalTime_maxList": evalTime_maxList,
                 "evalTime_minList": evalTime_minList,
                 "FMicroAvg_maxList": FMicroAvg_maxList,
                 "FMicroAvg_minList": FMicroAvg_minList,
                 "HammingLoss_nList": HammingLoss_nList,
                 "evalTime_meanList": evalTime_meanList,
                 "ExactMatch_maxList": ExactMatch_maxList,
                 "ExactMatch_minList": ExactMatch_minList,
                 "FMacroAvgD_maxList": FMacroAvgD_maxList,
                 "FMacroAvgD_minList": FMacroAvgD_minList,
                 "FMacroAvgL_maxList": FMacroAvgL_maxList,
                 "FMacroAvgL_minList": FMacroAvgL_minList,
                 "FMicroAvg_meanList": FMicroAvg_meanList,
                 "JaccardIndex_nList": JaccardIndex_nList,
                 "ExactMatch_meanList": ExactMatch_meanList,
                 "FMacroAvgD_meanList": FMacroAvgD_meanList,
                 "FMacroAvgL_meanList": FMacroAvgL_meanList,
                 "HammingLoss_maxList": HammingLoss_maxList,
                 "HammingLoss_minList": HammingLoss_minList,
                 "evalTime_medianList": evalTime_medianList,
                 "FMicroAvg_medianList": FMicroAvg_medianList,
                 "HammingLoss_meanList": HammingLoss_meanList,
                 "JaccardIndex_maxList": JaccardIndex_maxList,
                 "JaccardIndex_minList": JaccardIndex_minList,
                 "ExactMatch_medianList": ExactMatch_medianList,
                 "FMacroAvgD_medianList": FMacroAvgD_medianList,
                 "FMacroAvgL_medianList": FMacroAvgL_medianList,
                 "JaccardIndex_meanList": JaccardIndex_meanList,
                 "HammingLoss_medianList": HammingLoss_medianList,
                 "JaccardIndex_mediaList": JaccardIndex_medianList}
                    
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

def getMeasure(element):
    return element.get('measure')

def getEvalReport(element):
    evalReport = element.get('evaluation_report')
    evalReportExist = False
    evalTime_n = None
    FMicroAvg_n = None
    ExactMatch_n = None
    FMacroAvgD_n = None
    FMacroAvgL_n = None
    evalTime_max = None
    evalTime_min = None
    FMicroAvg_max = None
    FMicroAvg_min = None
    HammingLoss_n = None
    evalTime_mean = None
    ExactMatch_max = None
    ExactMatch_min = None
    FMacroAvgD_max = None
    FMacroAvgD_min = None
    FMacroAvgL_max = None
    FMacroAvgL_min = None
    FMicroAvg_mean = None
    JaccardIndex_n = None
    ExactMatch_mean = None
    FMacroAvgD_mean = None
    FMacroAvgL_mean = None
    HammingLoss_max = None
    HammingLoss_min = None
    evalTime_median = None
    FMicroAvg_median = None
    HammingLoss_mean = None
    JaccardIndex_max = None
    JaccardIndex_min = None
    ExactMatch_median = None
    FMacroAvgD_median = None
    FMacroAvgL_median = None
    JaccardIndex_mean = None
    HammingLoss_median = None
    JaccardIndex_median = None
    if evalReport != None:
        evalReportExist = True
        evalReportDict = ast.literal_eval(evalReport)
        evalTime_n = evalReportDict.get("evalTime_n")
        FMicroAvg_n = evalReportDict.get("FMicroAvg_n")
        ExactMatch_n = evalReportDict.get("ExactMatch_n")
        FMacroAvgD_n = evalReportDict.get("FMacroAvgD_n")
        FMacroAvgL_n = evalReportDict.get("FMacroAvgL_n")
        evalTime_max = evalReportDict.get("evalTime_max")
        evalTime_min = evalReportDict.get("evalTime_min")
        FMicroAvg_max = evalReportDict.get("FMicroAvg_max")
        FMicroAvg_min = evalReportDict.get("FMicroAvg_min")
        HammingLoss_n = evalReportDict.get("HammingLoss_n")
        evalTime_mean = evalReportDict.get("evalTime_mean")
        ExactMatch_max = evalReportDict.get("ExactMatch_max")
        ExactMatch_min = evalReportDict.get("ExactMatch_min")
        FMacroAvgD_max = evalReportDict.get("FMacroAvgD_max")
        FMacroAvgD_min = evalReportDict.get("FMacroAvgD_min")
        FMacroAvgL_max = evalReportDict.get("FMacroAvgL_max")
        FMacroAvgL_min = evalReportDict.get("FMacroAvgL_min")
        FMicroAvg_mean = evalReportDict.get("FMicroAvg_mean")
        JaccardIndex_n = evalReportDict.get("JaccardIndex_n")
        ExactMatch_mean = evalReportDict.get("ExactMatch_mean")
        FMacroAvgD_mean = evalReportDict.get("FMacroAvgD_mean")
        FMacroAvgL_mean = evalReportDict.get("FMacroAvgL_mean")
        HammingLoss_max = evalReportDict.get("HammingLoss_max")
        HammingLoss_min = evalReportDict.get("HammingLoss_min")
        evalTime_median = evalReportDict.get("evalTime_median")
        FMicroAvg_median = evalReportDict.get("FMicroAvg_median")
        HammingLoss_mean = evalReportDict.get("HammingLoss_mean")
        JaccardIndex_max = evalReportDict.get("JaccardIndex_max")
        JaccardIndex_min = evalReportDict.get("JaccardIndex_min")
        ExactMatch_median = evalReportDict.get("ExactMatch_median")
        FMacroAvgD_median = evalReportDict.get("FMacroAvgD_median")
        FMacroAvgL_median = evalReportDict.get("FMacroAvgL_median")
        JaccardIndex_mean = evalReportDict.get("JaccardIndex_mean")
        HammingLoss_median = evalReportDict.get("HammingLoss_median")
        JaccardIndex_median = evalReportDict.get("JaccardIndex_median")
    return evalReportExist, evalTime_n, FMicroAvg_n, ExactMatch_n, FMacroAvgD_n, FMacroAvgL_n, evalTime_max, evalTime_min, FMicroAvg_max, FMicroAvg_min, HammingLoss_n, evalTime_mean, ExactMatch_max, ExactMatch_min, FMacroAvgD_max, FMacroAvgD_min, FMacroAvgL_max, FMacroAvgL_min, FMicroAvg_mean, JaccardIndex_n, ExactMatch_mean, FMacroAvgD_mean, FMacroAvgL_mean, HammingLoss_max, HammingLoss_min, evalTime_median, FMicroAvg_median, HammingLoss_mean, JaccardIndex_max, JaccardIndex_min, ExactMatch_median, FMacroAvgD_median, FMacroAvgL_median, JaccardIndex_mean, HammingLoss_median, JaccardIndex_median

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

def getAllValid(run):
    valid = run["valid"].to_numpy()
    return valid

def getRunLength(run):
    length = len(run.index)
    return length

def getSolutionDetails(run, timestep):
    valids = getAllValid(run)

    isValid = None
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
        isValid = valids[timestep-1]
        timestamp = allTimestamps[timestep-1]
        components = allSolutions[timestep-1]
        parameterValues = allParameterValues[timestep-1]
        performance = allPerformances[timestep-1]
        exceptions = allExceptions[timestep-1]
        
    
    return isValid, timestamp, components, parameterValues, performance, exceptions

######################## This part can be deleted, i just tested a few things and used the code for debugging #####################################
def test():
    import searchSpaceHandler
    searchspace = searchSpaceHandler.getSearchSpaceAsDF()
    #runname = "runs/bohb_eval_407.json"
    runname = "runs/best_first_747_4h.json"
    jsonFile = open(runname) 
    convertedFile = json.load(jsonFile)
    data = convertedFile[2].get('data')
    jsonFile.close()
    df = getRunAsDF(data, searchspace)
    print(df)
    #print(getEvalReport(data[2]))
    
test()