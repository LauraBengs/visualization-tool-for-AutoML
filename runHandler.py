import json
import ast
import pandas as pd
import componentHandler
import searchSpaceHandler
import numpy as np

dimensions = ["evalTime_n", "FMicroAvg_n", "ExactMatch_n", "FMacroAvgD_n", "FMacroAvgL_n", "HammingLoss_n", "JaccardIndex_n"]
times = ["evalTime_max", "evalTime_min", "evalTime_mean",  "evalTime_median"]
minimisation = ["HammingLoss_max", "HammingLoss_min", "HammingLoss_mean", "HammingLoss_median"]
maximisation = ["FMicroAvg_max", "FMicroAvg_min", "ExactMatch_max", "ExactMatch_min", "FMacroAvgD_max", "FMacroAvgD_min", "FMacroAvgL_max",
                "FMacroAvgL_min", "FMicroAvg_mean",  "ExactMatch_mean", "FMacroAvgD_mean", "FMacroAvgL_mean", "FMicroAvg_median",  "JaccardIndex_max",
                "JaccardIndex_min", "ExactMatch_median", "FMacroAvgD_median", "FMacroAvgL_median", "JaccardIndex_mean",  "JaccardIndex_median"]
measurements = dimensions + times + minimisation + maximisation


def getRunAsDF(data, searchspace):
    dataDict = {"timestamp": [],
                "components": [],
                "kernel": [],
                "baseSLC": [],
                "metaSLC": [],
                "baseMLC": [],
                "metaMLC": [],
                "parameterValues": [],
                "performance": [],
                "exceptions": [],
                "valid": [],
                "measure": [],
                "evalReportExists": []
                }

    for measure in measurements:
        dataDict[measure] = []

    for element in data:
        elemTimestamp = element.get('timestamp_found')
        dataDict["timestamp"].append(elemTimestamp)

        elemComponents, elemParameterValues = getComponents(element)
        dataDict["components"].append(elemComponents)
        dataDict["parameterValues"].append(elemParameterValues)

        kernel, baseSLC, metaSLC, baseMLC, metaMLC = getComponentsPerCategory(elemComponents, searchspace)
        dataDict["kernel"].append(kernel)
        dataDict["baseSLC"].append(baseSLC)
        dataDict["metaSLC"].append(metaSLC)
        dataDict["baseMLC"].append(baseMLC)
        dataDict["metaMLC"].append(metaMLC)

        elemPerformance = element.get('eval_value')
        if elemPerformance == None:
            elemPerformance = np.nan
        dataDict["performance"].append(float(elemPerformance))

        elemException = element.get('exception')
        if elemException == None:
            elemException = np.nan
        dataDict["exceptions"].append(elemException)

        isValid = isSolutionValid(elemComponents, searchspace)
        dataDict["valid"].append(isValid)

        elemMeasure = element.get('measure')
        if elemMeasure == None:
            elemMeasure = np.nan
        dataDict["measure"].append(elemMeasure)

        evalReportExist, evalReport = getEvalReport(element)
        dataDict["evalReportExists"].append(evalReportExist)

        for measure in measurements:
            dataDict[measure].append(evalReport[measure])

    run = pd.DataFrame(dataDict)
    return run


def printSearchrun(runname):
    jsonFile = open(runname)
    convertedFile = json.load(jsonFile)
    data = convertedFile[2].get('data')
    for element in data:
        printElement(element)
        print("--------------------------------------------------------------")


def printElement(element):
    timestamp = element.get('timestamp_found')
    print("timestamp:", timestamp)
    components, parameterValues = getComponents(element)
    print("components:", components)
    print("parameterValues:", parameterValues)
    performance = element.get('eval_value')
    print("performance:", performance)
    exception = element.get('exception')
    print("exception:", exception)


def getComponents(element):
    componentsList = []
    parameterValues = []
    label = ''
    if element == None:
        return componentsList
    components = element.get('component_instance')
    componentsDict = ast.literal_eval(components.replace("null", "None"))  # converts string to dict
    elem = componentsDict.get('component').get('name')
    parameter = componentsDict.get('parameterValues')
    if elem == None or elem == {}:
        return componentsList
    elemCleaned = componentHandler.cleanName(elem)
    componentsList.append(elemCleaned)
    parameterValues.append(parameter)
    nextComponent = componentsDict.get('satisfactionOfRequiredInterfaces')
    nextComponentExists = True
    if nextComponent == {} or nextComponent == None:
        nextComponentExists = False
    else:
        label = str(nextComponent)[2]  # info if we need W or B
    while nextComponentExists == True:
        elem = nextComponent.get(label).get('component').get('name')
        elemCleaned = componentHandler.cleanName(elem)
        componentsList.append(elemCleaned)
        parameter = nextComponent.get(label).get('parameterValues')
        parameterValues.append(parameter)
        nextComponent = nextComponent.get(label).get('satisfactionOfRequiredInterfaces')
        if nextComponent == {} or nextComponent == None:
            nextComponentExists = False
        else:
            label = str(nextComponent)[2]
    return componentsList, parameterValues


def getComponentsPerCategory(elemComponents, searchspace):
    kernel = np.nan
    baseSLC = np.nan
    metaSLC = np.nan
    baseMLC = np.nan
    metaMLC = np.nan
    for component in elemComponents:
        category = searchSpaceHandler.getComponentCategory(component, searchspace)
        if category == "Kernel":
            kernel = component
        elif category == "BaseSLC":
            baseSLC = component
        elif category == "MetaSLC":
            metaSLC = component
        elif category == "BaseMLC":
            baseMLC = component
        elif category == "MetaMLC":
            metaMLC = component
    return kernel, baseSLC, metaSLC, baseMLC, metaMLC


def isSolutionValid(componentsList, searchspace):
    valid = True
    allCategories = []
    for elem in componentsList:
        info = searchspace.loc[searchspace['name'] == elem]
        category = info.iat[0, 0]
        allCategories.append(category)
    if len(set(allCategories)) != len(allCategories):
        valid = False
    return valid


def getEvalReport(element):
    evalReport = element.get('evaluation_report')
    evalReportExists = False

    report = {measure: None for measure in measurements}

    if evalReport is not None:
        evalReportExists = True
        evalReportDict = ast.literal_eval(evalReport)
        for measure in measurements:
            report[measure] = evalReportDict.get(measure)

    return evalReportExists, report


def getRunLength(run):
    length = len(run.index)
    return length


def getSolutionDetails(run, timestep):
    if timestep < 0:
        raise Exception("Index out of bounds")
    else:
        isValid = run["valid"][timestep]
        timestamp = run["timestamp"][timestep]
        components = run["components"][timestep]
        parameterValues = run["parameterValues"][timestep]
        performance = run["performance"][timestep]
        exceptions = run["exceptions"][timestep]

    return isValid, timestamp, components, parameterValues, performance, exceptions


def getDetailedEvaluationReport(run, timestep):
    evalExists = run["evalReportExists"][timestep]

    report = {measure: None for measure in measurements}

    if timestep != 0 and evalExists:
        for measure in measurements:
            report[measure] = run[measure][timestep]

    return evalExists, report
