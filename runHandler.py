import json
import ast
import pandas as pd
import componentHandler
import searchSpaceHandler

measurements = ["evalTime_n", "FMicroAvg_n", "ExactMatch_n", "FMacroAvgD_n", "FMacroAvgL_n",
                "evalTime_max", "evalTime_min", "FMicroAvg_max", "FMicroAvg_min", "HammingLoss_n",
                "evalTime_mean", "ExactMatch_max", "ExactMatch_min", "FMacroAvgD_max", "FMacroAvgD_min",
                "FMacroAvgL_max", "FMacroAvgL_min", "FMicroAvg_mean", "JaccardIndex_n", "ExactMatch_mean",
                "FMacroAvgD_mean", "FMacroAvgL_mean", "HammingLoss_max", "HammingLoss_min", "evalTime_median",
                "FMicroAvg_median", "HammingLoss_mean", "JaccardIndex_max", "JaccardIndex_min", "ExactMatch_median",
                "FMacroAvgD_median", "FMacroAvgL_median", "JaccardIndex_mean", "HammingLoss_median", "JaccardIndex_median"]


def getRunAsDF(data, searchspace):
    timestamps = []
    components = []
    kernelList = []
    baseSLCList = []
    metaSLCList = []
    baseMLCList = []
    metaMLCList = []
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
        elemTimestamp = element.get('timestamp_found')
        timestamps.append(elemTimestamp)
        elemComponents, elemParameterValues = getComponents(element)
        components.append(elemComponents)
        parameterValues.append(elemParameterValues)
        kernel, baseSLC, metaSLC, baseMLC, metaMLC = getComponentsPerCategory(elemComponents, searchspace)
        kernelList.append(kernel)
        baseSLCList.append(baseSLC)
        metaSLCList.append(metaSLC)
        baseMLCList.append(baseMLC)
        metaMLCList.append(metaMLC)
        elemPerformance = element.get('eval_value')
        performance.append(elemPerformance)
        elementException = element.get('exception')
        exceptions.append(elementException)
        isValid = isSolutionValid(elemComponents, searchspace)
        valid.append(isValid)
        elementMeasure = element.get('measure')
        measure.append(elementMeasure)
        evalReportExist, evalTime_n, FMicroAvg_n, ExactMatch_n, FMacroAvgD_n, FMacroAvgL_n, evalTime_max, evalTime_min, FMicroAvg_max, FMicroAvg_min, HammingLoss_n, evalTime_mean, ExactMatch_max, ExactMatch_min, FMacroAvgD_max, FMacroAvgD_min, FMacroAvgL_max, FMacroAvgL_min, FMicroAvg_mean, JaccardIndex_n, ExactMatch_mean, FMacroAvgD_mean, FMacroAvgL_mean, HammingLoss_max, HammingLoss_min, evalTime_median, FMicroAvg_median, HammingLoss_mean, JaccardIndex_max, JaccardIndex_min, ExactMatch_median, FMacroAvgD_median, FMacroAvgL_median, JaccardIndex_mean, HammingLoss_median, JaccardIndex_median = getEvalReport(
            element)
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
                 "kernel": kernelList,
                 "baseSLC": baseSLCList,
                 "metaSLC": metaSLCList,
                 "baseMLC": baseMLCList,
                 "metaMLC": metaMLCList,
                 "parameterValues": parameterValues,
                 "performance": performance,
                 "exceptions": exceptions,
                 "valid": valid,
                 "measure": measure,
                 "evalReportExists": evalReportExists,
                 "evalTime_n": evalTime_nList,
                 "FMicroAvg_n": FMicroAvg_nList,
                 "ExactMatch_n": ExactMatch_nList,
                 "FMacroAvgD_n": FMacroAvgD_nList,
                 "FMacroAvgL_n": FMacroAvgL_nList,
                 "evalTime_max": evalTime_maxList,
                 "evalTime_min": evalTime_minList,
                 "FMicroAvg_max": FMicroAvg_maxList,
                 "FMicroAvg_min": FMicroAvg_minList,
                 "HammingLoss_n": HammingLoss_nList,
                 "evalTime_mean": evalTime_meanList,
                 "ExactMatch_max": ExactMatch_maxList,
                 "ExactMatch_min": ExactMatch_minList,
                 "FMacroAvgD_max": FMacroAvgD_maxList,
                 "FMacroAvgD_min": FMacroAvgD_minList,
                 "FMacroAvgL_max": FMacroAvgL_maxList,
                 "FMacroAvgL_min": FMacroAvgL_minList,
                 "FMicroAvg_mean": FMicroAvg_meanList,
                 "JaccardIndex_n": JaccardIndex_nList,
                 "ExactMatch_mean": ExactMatch_meanList,
                 "FMacroAvgD_mean": FMacroAvgD_meanList,
                 "FMacroAvgL_mean": FMacroAvgL_meanList,
                 "HammingLoss_max": HammingLoss_maxList,
                 "HammingLoss_min": HammingLoss_minList,
                 "evalTime_median": evalTime_medianList,
                 "FMicroAvg_median": FMicroAvg_medianList,
                 "HammingLoss_mean": HammingLoss_meanList,
                 "JaccardIndex_max": JaccardIndex_maxList,
                 "JaccardIndex_min": JaccardIndex_minList,
                 "ExactMatch_median": ExactMatch_medianList,
                 "FMacroAvgD_median": FMacroAvgD_medianList,
                 "FMacroAvgL_median": FMacroAvgL_medianList,
                 "JaccardIndex_mean": JaccardIndex_meanList,
                 "HammingLoss_median": HammingLoss_medianList,
                 "JaccardIndex_median": JaccardIndex_medianList}

    run = pd.DataFrame(pandaData)
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
    kernel = None
    baseSLC = None
    metaSLC = None
    baseMLC = None
    metaMLC = None
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


def getMeasure(element):
    return element.get('measure')


def getEvalReport(element):
    evalReport = element.get('evaluation_report')
    evalReportExists = False

    report = {measure: None for measure in measurements}

    if evalReport is not None:
        evalReportExists = True
        evalReportDict = ast.literal_eval(evalReport)
        for measure in measurements:
            report[measure] = evalReportDict.get(measure)

    return evalReportExists, *report.values()


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

    return evalExists, *report.values()
