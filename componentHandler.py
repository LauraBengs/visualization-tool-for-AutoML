import numpy as np


def getComponentFullName(component):
    fullName = component.get('name')
    return fullName


def getComponentName(component):
    fullName = getComponentFullName(component)
    name = cleanName(fullName)
    return name


def cleanName(fullName):
    splitName = fullName.split(".")
    if splitName == []:
        raise Exception("Could not get component name due to an empty list")
    name = splitName[len(splitName)-1]
    return name


def getCategory(component):
    category = np.nan
    providedInterfaces = getProvidedInterface(component)
    if providedInterfaces == []:
        raise Exception("Could not get component category due to an empty list")
    if "K" in providedInterfaces:
        return "Kernel"
    if "MetaClassifier" in providedInterfaces:
        category = "MetaSLC"
    if "BaseClassifier" in providedInterfaces:
        category = "BaseSLC"
    if "BasicMLClassifier" in providedInterfaces:
        category = "BaseMLC"
    if "MetaMLClassifier" in providedInterfaces:
        category = "MetaMLC"

    return category


def getRequiredInterface(component):
    interfaces = component.get('requiredInterface')
    if interfaces == [] or interfaces == None:
        return np.nan
    requiredInterface = []
    for elem in interfaces:
        requiredInterface.append(elem.get('name'))
    return requiredInterface


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
    parameters = getListOfParameters(component)
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
