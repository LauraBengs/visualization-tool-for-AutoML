import json 

def main():
    jsonFile = open('weka-base.json') 
    convertedFile = json.load(jsonFile) #converts data of json file into a ?list?
    repository = convertedFile.get('repository')
    print(repository)
    components = convertedFile.get('components') #now you have a list of all components
    print("There exist", len(components), "components\n")
    for i in range(0, len(components)):
        print("component", i)
        getInfoComponent(components[i])
        print("\n")
    jsonFile.close()
    
def getInfoComponent(component):
    componentName = component.get('name')
    print("componentName:", componentName)
    requiredInterface = component.get('requiredInterface')
    if requiredInterface != []:
        print("requiredInterface:", requiredInterface)
    else: print("requiredInterface: None")
    providedInterface = component.get('providedInterface')
    print("providedInterface:", providedInterface)
    parameters = component.get('parameter')
    print("This component has", len(parameters), "parameters")
    for i in range(0, len(parameters)):
        print("parameter", i)
        getInfoParameter(parameters[i])
    dependencies = component.get('dependencies')
    print("dependencies:", dependencies)
    #print(component)
    
def getInfoParameter(parameter):
    parameterName = parameter.get('name')
    print("     parameterName:", parameterName)
    parameterType = parameter.get('type')
    print("     parameterType:", parameterType)
    parameterDefault = parameter.get('default')
    print("     parameterDefault:", parameterDefault)
    if parameterType == "double" or parameterType == "int":
        parameterMin = parameter.get('min')
        print("     parameterMin:", parameterMin)
        parameterMax = parameter.get('max')
        print("     parameterMax:", parameterMax)
        parameterMinInterval = parameter.get('minInterval')
        print("     parameterMinInterval:", parameterMinInterval)
        parameterRefineSplits = parameter.get('refineSplits')
        print("     parameterRefineSplits:", parameterRefineSplits)
    
main()