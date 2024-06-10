#Python program to get the data of a json file

import json 
import ast

def main():
    json_file = open('best_first_747_4h.json') 
    converted_file = json.load(json_file) #converts data of json file into a ?list?
    data = converted_file[2].get('data')
    #printElement(data[0])
    printAllElements(data)
    json_file.close()

def printAllElements(data):
    for element in data:
        printElement(element)
        print("--------------------------------------------------------------")

def printElement(element):
    timestamp = getTimestamp(element)
    components = getComponents(element)
    performance = getPerformanceValue(element)
    print("timestamp:", timestamp,"\ncomponents:", components, "\nperformance:", performance)

def getComponents(element):
    components = element.get('component_instance')
    comp_dict = ast.literal_eval(components) #converts string to dict
    list_of_components = []
    elem = comp_dict.get('component').get('name')
    list_of_components.append(elem)
    second_elem = comp_dict.get('satisfactionOfRequiredInterfaces').get('W').get('component').get('name')
    list_of_components.append(second_elem)
    return components

def getTimestamp(element):
    return element.get('timestamp_found')

def getPerformanceValue(element):
    return element.get('eval_value')

main()