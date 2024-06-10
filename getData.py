#Python program to get the data of a json file

import json 
import ast

def main():
    json_file = open('best_first_747_4h.json') 
    converted_file = json.load(json_file) #converts data of json file into a ?list?
    data = converted_file[2].get('data')
    printElement(data[0])
    #printAllElements(data)
    json_file.close()

def printAllElements(data):
    for elem in data:
        printElement(elem)
        print("--------------------------------------------------------------")

def printElement(elem):
    elem_comp, elem_timestamp, elem_perf = extractInfos(elem)
    elem_comp_dict = ast.literal_eval(elem_comp) #converts string to dict
    components = getComponents(elem_comp_dict)
    print("components:", components, "\ntimestamp:", elem_timestamp, "\nperformance:", elem_perf)

def extractInfos(solution):
    components = solution.get('component_instance')
    timestamp = solution.get('timestamp_found')
    performance = solution.get('eval_value')
    return components, timestamp, performance

def getComponents(component_instance: dict):
    list = []
    elem = component_instance.get('component').get('name')
    list.append(elem)
    second_elem = component_instance.get('satisfactionOfRequiredInterfaces').get('W').get('component').get('name')
    list.append(second_elem)
    return list

main()