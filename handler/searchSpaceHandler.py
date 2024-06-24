import json 
import pandas as pd
import handler.componentHandler as componentHandler
import numpy
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
        
    data = { "category": category,
            "name": name,
            "fullName": fullName,
            "requiredInterface": requiredInterface,
            "providedeInterface": providedInterface,
            "parameters": parameters,
            "dependencies": dependencies
            }
    
    #pd.options.display.max_columns = None
    #pd.options.display.max_rows = None
    searchSpace = pd.DataFrame(data)
    return searchSpace
    
def openJsonFileFromGithub(link):
    file = requests.get(link)
    jsonFile = json.loads(file.text)
    repository = jsonFile.get('repository')
    components = jsonFile.get('components') #now you have a list of all components
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

def getAllComponentNames(searchspace):
    return searchspace["name"].to_numpy()

def getAllCategories(searchspace):
    return searchspace["category"].to_numpy()

#searchspace = getSearchSpaceAsDF()
#print(searchspace)
#printSearchSpace('weka-base.json')

def getComponentInfo(info):
    text = ""
    fullName = info.iat[0,2]
    text = text + "**Full name:** " + fullName + "\n"

    category = info.iat[0,0]
    text = text + "**Category:** " + category + "\n"
    
    requiredInterface = info.iat[0,3]
    if type(requiredInterface) is list:
        text = text + "**Required interface(s):** \n"
        for elem in requiredInterface:
            text = text + "- " + elem +"\n"
    else: 
        text = text + "**Required interface(s):** None\n"
    
    providedInterface = info.iat[0,4]
    if type(providedInterface) is list:
        text = text + "\n**Provided interface(s):**\n"
        for elem in providedInterface:
            text = text + "- " + elem +"\n"
    else: 
        text = text + "\n**Provided interface(s):** None\n"
    
    dependencies = info.iat[0,6]
    if type(dependencies) is list: 
        text = text + "\n**Dependecies:**" + str(dependencies) + "\n"
    else:
        text = text + "\n**Dependencies:** None\n"
    
    parameters = info.iat[0, 5]
    if type(parameters) is list:
        text = text + "**Parameter(s):** This component has " +  str(len(parameters)) + " parameters\n"
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
                text = text + ", refineSplits = "+ str(refineSplits)
            values = componentHandler.getParametersValues(parameters[i])
            if values != None:
                text = text + ", values = "
                for v in range(0, len(values)):
                    if v == 0:
                        text = text + "\[" + values[v]
                    else:
                        text = text + ", " + values[v]
                text = text + "\]"
            comment = componentHandler.getParameterComment(parameters[i])
            if comment != None:
                text = text + ", comment: " + comment
    else:
        text = text + "**Parameters:** This component has no parameters"
    
    return text