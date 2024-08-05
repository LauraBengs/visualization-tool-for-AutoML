import json
import pandas as pd
import componentHandler
import requests


def printSearchSpace(link):
    repository, components, numComponents = openJsonFileFromGithub(link)
    print("repository:", repository, "\nnumber of components:", numComponents, "\n")
    for i in range(0, len(components)):
        print("component", i)
        componentHandler.printComponent(components[i])
        print("---------------------------------------------------")


def getSearchSpaceAsDF():
    category = []
    name = []
    fullName = []
    requiredInterface = []
    providedInterface = []
    parameters = []
    dependencies = []

    searchSpaceLinks = ['https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/weka-base.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/weka-meta.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/meka-base.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/meka-meta.json']

    for link in searchSpaceLinks:
        category, name, fullName, requiredInterface, providedInterface, parameters, dependencies = addData(link, category, name, fullName, requiredInterface, providedInterface, parameters, dependencies)

    data = {"category": category,
            "name": name,
            "fullName": fullName,
            "requiredInterface": requiredInterface,
            "providedInterface": providedInterface,
            "parameters": parameters,
            "dependencies": dependencies
            }

    searchSpace = pd.DataFrame(data)
    return searchSpace


def openJsonFileFromGithub(link):
    file = requests.get(link)
    jsonFile = json.loads(file.text)
    repository = jsonFile.get('repository')
    components = jsonFile.get('components')
    numComponents = len(components)
    return repository, components, numComponents


def addData(link, category, name, fullName, requiredInterface, providedInterface, parameters, dependencies):
    _, components, _ = openJsonFileFromGithub(link)
    for elem in components:
        category.append(componentHandler.getCategory(elem))
        name.append(componentHandler.getComponentName(elem))
        fullName.append(componentHandler.getComponentFullName(elem))
        requiredInterface.append(componentHandler.getRequiredInterface(elem))
        providedInterface.append(componentHandler.getProvidedInterface(elem))
        parameters.append(componentHandler.getListOfParameters(elem))
        dependencies.append(componentHandler.getDependencies(elem))
    return category, name, fullName, requiredInterface, providedInterface, parameters, dependencies


def getComponentInfo(info):
    text = ""
    fullName = info["fullName"].iloc[0]
    text = text + "**Full name:** " + fullName + "\n"

    category = info["category"].iloc[0]
    text = text + "**Category:** " + category + "\n"

    requiredInterface = info["requiredInterface"].iloc[0]
    if type(requiredInterface) is list:
        text = text + "**Required interface(s):** \n"
        for elem in requiredInterface:
            text = text + "- " + elem + "\n"
    else:
        text = text + "**Required interface(s):** None\n"

    providedInterface = info["providedInterface"].iloc[0]
    if type(providedInterface) is list:
        text = text + "\n**Provided interface(s):**\n"
        for elem in providedInterface:
            text = text + "- " + elem + "\n"
    else:
        text = text + "\n**Provided interface(s):** None\n"

    dependencies = info["dependencies"].iloc[0]
    if type(dependencies) is list:
        text = text + "\n**Dependecies:**" + str(dependencies) + "\n"
    else:
        text = text + "\n**Dependencies:** None\n"

    parameters = info["parameters"].iloc[0]
    if type(parameters) is list:
        text = text + "**Parameter(s):** This component has " + str(len(parameters)) + " parameters\n"
        for i in range(0, len(parameters)):
            text = text + "\n- Parameter " + str(i+1) + ": name = " + componentHandler.getParameterName(parameters[i])
            parameterType = componentHandler.getParameterType(parameters[i])
            if parameterType != None:
                text = text + ", type = " + parameterType
            default = componentHandler.getParameterDefault(parameters[i])
            if default != None:
                text = text + ", default = " + str(default)
            min = componentHandler.getParameterMin(parameters[i])
            if min != None:
                text = text + ", min =  " + str(min)
            max = componentHandler.getParameterMax(parameters[i])
            if max != None:
                text = text + ", max = " + str(max)
            minInterval = componentHandler.getParamterMinIntervall(parameters[i])
            if minInterval != None:
                text = text + ", minInterval = " + str(minInterval)
            refineSplits = componentHandler.getParameterRefineSplits(parameters[i])
            if refineSplits != None:
                text = text + ", refineSplits = " + str(refineSplits)
            values = componentHandler.getParametersValues(parameters[i])
            if values != None:
                text = text + ", values = "
                for v in range(0, len(values)):
                    if v == 0:
                        text = text + r"\[" + values[v]
                    else:
                        text = text + ", " + values[v]
                text = text + r"\]"
            comment = componentHandler.getParameterComment(parameters[i])
            if comment != None:
                text = text + ", comment: " + comment
    else:
        text = text + "**Parameters:** This component has no parameters"

    return text


def getComponentCategory(componentName, searchspace):
    row = searchspace[searchspace.name == componentName]
    category = row['category'].iloc[0]
    return category
