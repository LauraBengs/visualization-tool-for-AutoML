import json 
import pandas as pd
import componentHandler
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
    requiredInterface = []
    providedInterface = []
    parameters = []
    dependencies = []
    
    searchSpaceLinks = ['https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/weka-base.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/weka-meta.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/meka-base.json', 'https://raw.githubusercontent.com/mwever/tpami-automlc/master/searchspace/meka-meta.json']
    
    for link in searchSpaceLinks:
        category, name, requiredInterface, providedInterface, parameters, dependencies = addData(link, category, name, requiredInterface, providedInterface, parameters, dependencies)
        
    data = { "category": category,
            "name": name,
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

def addData(link, category, name, requiredInterface, providedInterface, parameters, dependencies):
    _, components, _ = openJsonFileFromGithub(link)
    for elem in components:
        category.append(componentHandler.getCategory(elem))
        name.append(componentHandler.getComponentName(elem))
        requiredInterface.append(componentHandler.getRequiredInterface(elem))
        providedInterface.append(componentHandler.getProvidedInterface(elem))
        parameters.append(componentHandler.getListOfParameters(elem))
        dependencies.append(componentHandler.getDependencies(elem))
    return category, name, requiredInterface, providedInterface, parameters, dependencies

def getAllComponentNames(searchspace):
    return searchspace["name"].to_numpy()

def getAllCategories(searchspace):
    return searchspace["category"].to_numpy()

#print(getSearchSpaceAsDF())
#printSearchSpace('weka-base.json')