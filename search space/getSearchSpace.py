import json 
import pandas as pd
import numpy as np
import searchSpaceHandler 

def main():
    jsonFile = open('weka-base.json') 
    convertedFile = json.load(jsonFile) #converts data of json file into a ?list?
    repository = convertedFile.get('repository')
    print(repository)
    components = convertedFile.get('components') #now you have a list of all components
    print("There exist", len(components), "components\n")
    
    category = []
    name = []
    requiredInterface = []
    providedInterface = []
    parameters = []
    dependencies = []
    
    for elem in components:
        category.append(searchSpaceHandler.getCategory(elem))
        name.append(searchSpaceHandler.getComponentName(elem))
        requiredInterface.append(searchSpaceHandler.getRequiredInterface(elem))
        providedInterface.append(searchSpaceHandler.getProvidedInterface(elem))
        parameters.append(searchSpaceHandler.getListOfParameters(elem))
        dependencies.append(searchSpaceHandler.getDependencies(elem))
        
    data = { "category": category,
            "name": name,
            "requiredInterface": requiredInterface,
            "providedeInterface": providedInterface,
            "parameters": parameters,
            "dependencies": dependencies
            }
    myvar = pd.DataFrame(data)
    print(myvar)
    
    jsonFile.close()
    

main()