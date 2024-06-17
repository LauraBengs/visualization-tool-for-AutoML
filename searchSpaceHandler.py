import json 
import pandas as pd
import componentHandler
import numpy

def printSearchSpace(file):
    repository, components, numComponents = openJsonFile(file)
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
    
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('weka-base.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('weka-meta.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('meka-base.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('meka-meta.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
        
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
    
def openJsonFile(filename):
    jsonFile = open(filename) 
    convertedFile = json.load(jsonFile) #converts data of json file into a ?list?
    repository = convertedFile.get('repository')
    components = convertedFile.get('components') #now you have a list of all components
    numComponents = len(components)
    jsonFile.close()
    return repository, components, numComponents

def addData(filename, category, name, requiredInterface, providedInterface, parameters, dependencies):
    _, components, _ = openJsonFile(filename)
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

#print(getSearchSpaceAsDF())
#printSearchSpace('weka-base.json')