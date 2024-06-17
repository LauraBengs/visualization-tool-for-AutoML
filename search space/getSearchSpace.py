import json 
import pandas as pd
import numpy as np
import searchSpaceHandler 

def getSearchSpace():
    category = []
    name = []
    requiredInterface = []
    providedInterface = []
    parameters = []
    dependencies = []
    
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('search space/weka-base.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('search space/weka-meta.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('search space/meka-base.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
    category, name, requiredInterface, providedInterface, parameters, dependencies = addData('search space/meka-meta.json', category, name, requiredInterface, providedInterface, parameters, dependencies)
        
    data = { "category": category,
            "name": name,
            "requiredInterface": requiredInterface,
            "providedeInterface": providedInterface,
            "parameters": parameters,
            "dependencies": dependencies
            }
    
    #pd.options.display.max_columns = None
    #pd.options.display.max_rows = None
    allComponents = pd.DataFrame(data)
    print(allComponents)
    
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
        category.append(searchSpaceHandler.getCategory(elem))
        name.append(searchSpaceHandler.getComponentName(elem))
        requiredInterface.append(searchSpaceHandler.getRequiredInterface(elem))
        providedInterface.append(searchSpaceHandler.getProvidedInterface(elem))
        parameters.append(searchSpaceHandler.getListOfParameters(elem))
        dependencies.append(searchSpaceHandler.getDependencies(elem))
    return category, name, requiredInterface, providedInterface, parameters, dependencies

getSearchSpace()