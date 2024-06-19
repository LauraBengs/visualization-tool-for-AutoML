# this file provides some basic functions to handle the searchspace descriptions

import numpy as np

def getComponentFullName(component):
    fullName = component.get('name')
    return fullName

def getComponentName(component):
    fullName = getComponentFullName(component)
    splitName = fullName.split(".")
    if splitName == []:
            raise Exception("Could not get component name due to an empty list")
    name = splitName[len(splitName)-1]
    return name

def getCategory(component):
    category = np.nan
    fullName = getComponentFullName(component)
    splitName = fullName.split(".")
    if "supportVector" in splitName:
        return "Kernel"
    if "weka" in splitName:
        if "meta" in splitName:
            category = "MetaSLC"
        else:
            category = "BaseSLC"
    if "meka" in splitName:
        if "meta" in splitName:
            category = "MetaMLC"
        else: 
            category = "BaseMLC"
    return category

def getRequiredInterface(component):
    requiredInterface = component.get('requiredInterface')
    if requiredInterface != [] and requiredInterface != None:
        return requiredInterface
    else: 
        return np.nan

def getProvidedInterface(component):
    providedInterface = component.get('providedInterface')
    if providedInterface != [] and providedInterface != None:
        return providedInterface
    else:
        return np.nan

def getListOfParameters(component):
    parameters = component.get('parameter')
    if parameters != [] and parameters != None:
        return parameters
    else: 
        return np.nan

def getDependencies(component):
    dependencies = component.get('dependencies')
    if dependencies != [] and dependencies != None:
        return dependencies
    else:
        return np.nan
    
def printComponent(component):
    print("componentFullName:", getComponentFullName(component))
    print("componentName:", getComponentName(component))
    print("requiredInterface:", getRequiredInterface(component))
    print("providedInterface:", getProvidedInterface(component))
    parameters  = getListOfParameters(component)
    if type(parameters) is list:
        print("This component has", len(parameters), "parameters")
        for i in range(0, len(parameters)):
            print("parameter", i)
            printParameter(parameters[i])
            print("\n")
    else: 
        print("This component has no parameters")
    print("dependencies:", getDependencies(component))

def getParameterName(parameter):
    parameterName = parameter.get('name')
    return parameterName

def getParameterComment(parameter):
    parameterComment = parameter.get('comment')
    return parameterComment

def getParameterType(parameter):
    parameterType = parameter.get('type')
    return parameterType

def getParameterDefault(parameter):
    parameterDefault = parameter.get('default')
    return parameterDefault

def getParameterMin(parameter):
    parameterMin = parameter.get('min')
    return parameterMin

def getParameterMax(parameter):
    parameterMax = parameter.get('max')
    return parameterMax

def getParamterMinIntervall(parameter):
    parameterMinInterval = parameter.get('minInterval')
    return parameterMinInterval

def getParameterRefineSplits(parameter):
    parameterRefineSplits = parameter.get('refineSplits')
    return parameterRefineSplits

def getParametersValues(parameter):
    parameterValues = parameter.get('values')
    return parameterValues
    
def printParameter(parameter):
    print("parameterName:", getParameterName(parameter))
    parameterType = getParameterType(parameter)
    print("parameterType:", parameterType)
    print("parameterDefault:", getParameterDefault(parameter))
    if parameterType == "double" or parameterType == "int":
        print("parameterMin:", getParameterMin)
        print("parameterMax:", getParameterMax(parameter))
        print("parameterMinInterval:", getParamterMinIntervall(parameter))
        print("parameterRefineSplits:", getParameterRefineSplits(parameter))