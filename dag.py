import searchSpaceHandler
import runHandler
from dash import Dash, html, Input, Output, callback, State, dcc, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json 
import base64
import io
import plotly.express as px
import pandas as pd


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Visualisation tool for AutoML"

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)
allComponentFullNames = searchSpaceHandler.getAllComponentfullNames(searchspace)
categories = searchSpaceHandler.getAllCategories(searchspace)

runSelector = None
run = None
uploadedFile = False
uploadedRunname = None

globalAnytimePlotData = None
globalParallelCategoriesPlotData = None

edges = {}
nodes = {}

#get datapoints for dag
x = 0
y = 0
yK = 0
iK = 1
yBS = 0
iBS = 1
yMS = 0
iMS = 1
yBM = 0
iBM = 1
yMM = 0
iMM = 1

components = []

for i in range(0, len(allComponentNames)):
    if categories[i] == "Kernel": 
        x = 0
        y = yK
        if yK >= 0:
            yK = yK - iK * 60
        else: 
            yK = yK + iK * 60
        iK += 1
    elif categories[i] == "BaseSLC": 
        x = 300
        y = yBS
        if yBS >= 0:
            yBS = yBS - iBS * 60
        else: 
            yBS = yBS + iBS * 60
        iBS += 1
    elif categories[i] == "MetaSLC": 
        x = 600
        y = yMS
        if yMS >= 0:
            yMS = yMS - iMS * 60
        else: 
            yMS = yMS + iMS * 60
        iMS += 1
    elif categories[i] == "BaseMLC": 
        x = 900
        y = yBM
        if yBM >= 0:
            yBM = yBM - iBM * 60
        else: 
            yBM = yBM + iBM * 60
        iBM += 1
    elif categories[i] == "MetaMLC": 
        x = 1200
        y = yMM
        if yMM >= 0:
            yMM = yMM - iMM * 60
        else: 
            yMM = yMM + iMM * 60
        iMM += 1
    
    components.append({'data': {'id': allComponentNames[i], 'label': allComponentNames[i]}, 'position': {'x': x, 'y': y}, 'classes': categories[i]})

connections = []
possibleComponentPartner = []

for a in range(0, len(allComponentNames)):
    temp = []
    providedInterfaces = searchspace.loc[searchspace['name'] == allComponentNames[a]].iat[0,4]
    if type(providedInterfaces) is list:
        for b in range(0, len(allComponentNames)):
            requiredInterfaces = searchspace.loc[searchspace['name'] == allComponentNames[b]].iat[0,3]
            if type(requiredInterfaces) is list:
                for elemA in providedInterfaces:
                    if (elemA in requiredInterfaces or allComponentFullNames[a] in requiredInterfaces) and categories[a] != categories[b]:
                        connections.append({'data': {'id':(allComponentNames[a]+"-"+allComponentNames[b]), 'source': allComponentNames[a], 'target': allComponentNames[b], 'weight':1}})
                        temp.append(allComponentNames[b])
    possibleComponentPartner.append(temp)

dataPoints = components + connections

style = [
    {'selector': 'node','style': {'content': 'data(label)', 'opacity':'0'}},
    {'selector': 'edge','style': {'opacity':'0'}}
    ]

max = 0
min = 0

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row(html.Div([
                html.H4("Run"),
                html.Hr(),
                html.Div("Select a preloaded run or upload a .json file of your searchrun."),
                html.Div([html.H5("Select run"),
                        dcc.Dropdown(id="runSelector", 
                            options=[
                                {"label": "Show searchspace", "value": "searchspace"},
                                {"label": "best_first_747_4h", "value": "runs/best_first_747_4h.json"},
                                {"label": "bohb_eval_407", "value": "runs/bohb_eval_407.json"},
                                {"label": "bohb_eval_409", "value": "runs/bohb_eval_409.json"},
                                {"label": "ggp_eval_407", "value": "runs/ggp_eval_407.json"},
                                {"label": "ggp_eval_409", "value": "runs/ggp_eval_409.json"},
                                {"label": "gmfs_eval", "value": "runs/gmfs_eval.json"},
                                {"label": "gmfs_eval_407", "value": "runs/gmfs_eval_407.json"},
                                {"label": "gmfs_eval_409", "value": "runs/gmfs_eval_409.json"},
                                {"label": "hblike_eval_786", "value": "runs/hblike_eval_786.json"},
                                {"label": "hblike_eval_811", "value": "runs/hblike_eval_811.json"},
                                {"label": "random_eval_138", "value": "runs/random_eval_138.json"},
                                {"label": "random_eval_151", "value": "runs/random_eval_151.json"}
                                ],
                            value= "searchspace",
                            clearable=False)]),
                html.H5("Upload run"),
                dcc.Upload(id='uploadRun', children=html.Div(['Drag and Drop or \n', html.A('Select Files')]),
                           style={
                               'width': '100%',
                               'height': '60px',
                               'lineHeight': '30px',
                               'borderWidth': '1px',
                               'borderStyle': 'dashed',
                               'borderRadius': '5px',
                               'textAlign': 'center',
                            },
                ),
                html.Div(id='uploadError'),
                html.H4("Restrictions"),
                html.Hr(),
                html.H5("Performance"),
                html.Div("Only visualise solutions with a performance greater or equal to"),
                dcc.Input(id="runRestrictions", type="number", placeholder="Define restriction (value between 0 and 1)", min=0, max=1, step=0.1, value=0),
                html.H4("Evaluation Measure"),
                html.Hr(),
                dcc.Dropdown(id="evalMeasure", 
                            options=[
                                {"label": "performance", "value": "performance"},
                                {"label": "HammingLoss_min", "value": "HammingLoss_min"},
                                {"label": "HammingLoss_max", "value": "HammingLoss_max"},
                                {"label": "HammingLoss_mean", "value": "HammingLoss_mean"},
                                {"label": "HammingLoss_median", "value": "HammingLoss_median"},
                                {"label": "ExactMatch_min", "value": "ExactMatch_min"},
                                {"label": "ExactMatch_max", "value": "ExactMatch_max"},
                                {"label": "ExactMatch_mean", "value": "ExactMatch_mean"},
                                {"label": "ExactMatch_median", "value": "ExactMatch_median"},
                                {"label": "FMicroAvg_min", "value": "FMicroAvg_min"},
                                {"label": "FMicroAvg_max", "value": "FMicroAvg_max"},
                                {"label": "FMicroAvg_mean", "value": "FMicroAvg_mean"},
                                {"label": "FMicroAvg_median", "value": "FMicroAvg_median"},
                                {"label": "FMacroAvgD_min", "value": "FMacroAvgD_min"},
                                {"label": "FMacroAvgD_max", "value": "FMacroAvgD_max"},
                                {"label": "FMacroAvgD_mean", "value": "FMacroAvgD_mean"},
                                {"label": "FMacroAvgD_median", "value": "FMacroAvgD_median"},
                                {"label": "FMacroAvgL_min", "value": "FMacroAvgL_min"},
                                {"label": "FMacroAvgL_max", "value": "FMacroAvgL_max"},
                                {"label": "FMacroAvgL_mean", "value": "FMacroAvgL_mean"},
                                {"label": "FMacroAvgL_median", "value": "FMacroAvgL_median"},
                                {"label": "JaccardIndex_min", "value": "JaccardIndex_min"},
                                {"label": "JaccardIndex_max", "value": "JaccardIndex_max"},
                                {"label": "JaccardIndex_mean", "value": "JaccardIndex_mean"},
                                {"label": "JaccardIndex_median", "value": "JaccardIndex_median"},
                                ],
                            value= "performance",
                            clearable=False)
            ], className='sidebar'))
        ], width=2),
        
        dbc.Col([
            dbc.Row([
                html.H4("Directed acyclic graph (Dag)"),
                html.Hr()
            ]),
            dbc.Row([
                dbc.Col([
                    cyto.Cytoscape(
                        id='dag',
                        layout={'name': 'preset'},
                        style={'width': '100%', 'height': '400px'},
                        elements=dataPoints,
                        stylesheet=style,
                        responsive=True),
                ], width=5),
                dbc.Col([
                    html.Div(id='solutionWarning', className='warning'),
                    html.H5(id='bestSolutionHeader'),
                    html.Hr(),
                    html.Div(id='bestSolution'),
                    html.H5("Overview"),
                    html.Hr(),
                    html.Div(id='config'),
                    html.H5(id='solutionHeader'),
                    html.Hr(),
                    html.Div(id='solution'),
                    html.Details([html.Summary("Click here for exceptions"), html.Div(id='exceptions')]),
                    html.Details([html.Summary("Click here for a detailed evaluation report"), html.Div(id='evalReport')])
                ], width=7)
            ]),
            dbc.Row([
                html.H4("Anytime performance plot"),
                html.Hr(),
                dcc.Graph(id='anytimePlot', figure=px.scatter())
            ]),
            dbc.Row([
                html.H4("Parallel categories plot"),
                html.Hr(),
                dcc.Graph(id='parallelPlot', figure=px.scatter())
            ])
        ],width=10),
    ]),
    
    html.Div(
        dbc.Row([
            dbc.Col(html.H3("Visualisation tool for AutoML", className='headline'), width=4),
            dbc.Col(html.Button('?', id='btnHelp', n_clicks=0), width=1),
            dbc.Col(html.Div([
                        dcc.Slider(min, max, 1, value=min, marks=None, tooltip={"placement": "bottom", "always_visible": True}, id="slider"),
                        dbc.Row([
                            dbc.Col(html.Button('|◁', id='btnMin', n_clicks=0), width=2),
                            dbc.Col(html.Button('←', id='btnBack', n_clicks=0), width=2),
                            dbc.Col(html.Button('▷', id='btnStart', n_clicks=0), width=2),
                            dbc.Col(html.Button('→', id='btnNext', n_clicks=0), width=2),
                            dbc.Col(html.Button('▷|', id='btnMax', n_clicks=0), width=2)
                        ]),
                    ], id='controls', style={'display':'none'}))
        ]),
        className='footer'
    ),
    
    dbc.Modal(
            [
                dbc.ModalHeader(id="modal-header"),
                dbc.ModalBody(id="modal-text"),
            ],
            id="modal",
            scrollable = True,
            is_open=False,
            style = {'white-space': 'pre-wrap'},
            size = "lg"
    ),
    
    dcc.Interval(id='interval-component', interval=800, n_intervals=0, disabled=True),
])

def getInfosForModal(data):
    modalHeader = data['label']
    component = searchspace.loc[searchspace['name'] == modalHeader]
    modalText = searchSpaceHandler.getComponentInfo(component)
    return modalHeader, modalText

@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Input('btnHelp', 'n_clicks'), Input('dag', 'tapNodeData'), State("modal", "is_open"))
def toggle_modal(n, data, is_open):
    if "btnHelp" == ctx.triggered_id:
        modalHeader = dcc.Markdown("#### ❔ Help/ Explanation")
        performance = "##### Performance \n - Given by the colour of a node \n - Maximisation: Yellow (<= 0.33), Orange (<= 0.66), Red (<= 0.66), Darkred (> 0.9) \n - Minimisation: blue \n - Grey: No performance value available \n"
        edge = "##### Edges \n - Thickness corresponds to how often a connection has been used in a solution \n - Color black: connection has been used more than 10 times \n"
        filter = "##### Filter \n Solution candidates that contain two or more components from one categorie will not be visualised. \n A corresponding message about why a solution candidate is not being visualised can be found in the details section."
        modalText = dcc.Markdown(performance + edge + filter)
        return not is_open, modalHeader, modalText
    elif data is not None:
        header, text = getInfosForModal(data)
        modalHeader = dcc.Markdown("#### " + header)
        modalText = dcc.Markdown(text)
        return not is_open, modalHeader, modalText
    return is_open, '', ''

def showSearchrun(stylesheet, run, runname, restrictions, length, evalMeasure):    
    if runname == "searchspace":
        stylesheet = [
            {'selector': 'node','style': {'content': 'data(label)'}},
            {'selector': '.Kernel', 'style': { 'background-color': '#EC9F05'}},
            {'selector': '.BaseSLC', 'style': { 'background-color': '#4A6C6F'}},
            {'selector': '.MetaSLC', 'style': { 'background-color': '#A1C084'}},
            {'selector': '.BaseMLC', 'style': { 'background-color': '#A63446'}},
            {'selector': '.MetaMLC', 'style': { 'background-color': '#D89A9E'}},
            {'selector':'edge', 'style':{'line-color':'#adaaaa'}}]
        return stylesheet, None, 0, 0
   
    solutions = runHandler.getAllComponentSolutions(run)
    performances = run[evalMeasure].to_numpy()
    valids = runHandler.getAllValid(run)
    
    minimisation = evalMeasure in ["HammingLoss_min", "HammingLoss_max", "HammingLoss_mean", "HammingLoss_median"]
    bestSolution = None
    if minimisation:
        bestPerformance = 1
    else: 
        bestPerformance = 0
    bestFound = 0

    for s in range(length+1):
        solComponents = solutions[s]
        solPerformance = performances[s]
        isValid = valids[s]
        
        if isValid == False:
            continue
        
        color = ""
        opacity = "0"
        if solPerformance == None or pd.isna(solPerformance):
            color = ""
            if restrictions == 0:
                opacity = "1"
        else:
            solPerformance = float(solPerformance)
            
            if minimisation:
                #minimisation
                if solPerformance >= 0.67: color = "lightskyblue"
                elif solPerformance >= 0.34 : color = "dodgerblue"
                elif solPerformance >= 0.1: color = "blue"
                else: color = "darkblue"
            else:
                #maximisation
                if solPerformance <= 0.33: color = "yellow"
                elif solPerformance <= 0.66: color = "orange"
                elif solPerformance <= 0.9: color = "red"
                else: color = "darkred"
            
            if solPerformance >= restrictions:
                opacity = "1"
        
        for elem in solComponents:
            global nodes
            currentColor = nodes.get(elem)
            if currentColor == None:
                nodes[elem] = color
                node = "[label = \"" + elem + "\"]"
                stylesheet.append({'selector': node, 'style': {'background-color': color, 'opacity':opacity}})
            elif (currentColor != color and currentColor != "darkred") and (color == "darkred" or color == "red" or (color == "orange" and currentColor != "red") or (color == "yellow" and currentColor == "")):
                nodes.update({elem: color})
                node = "[label = \"" + elem + "\"]"
                stylesheet.append({'selector': node, 'style': {'background-color': color, 'opacity':opacity}})                    
            
        if opacity != "0":
            if type(solPerformance) == float:
                if (minimisation and solPerformance < bestPerformance) or (not minimisation and solPerformance > bestPerformance):
                    bestPerformance = solPerformance
                    bestSolution = solComponents
                    bestFound = s
            for i in range(0, len(solComponents)-1):
                edge = "#"+solComponents[i+1]+"-"+solComponents[i]
                global edges
                currentWeight = edges.get(edge)
                if currentWeight == None:
                    edges[edge] = 1
                    stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width': str(edges[edge]), 'target-arrow-shape' : 'triangle',  'curve-style': 'bezier'}})
                else:
                    newWeight = currentWeight +2
                    if newWeight >= 20:
                        stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width':'20', 'line-color': 'black', 'target-arrow-shape' : 'triangle',  'target-arrow-color': 'black', 'curve-style': 'bezier'}})
                    else:
                        edges.update({edge: newWeight})
                        stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width': str(edges[edge]), 'target-arrow-shape' : 'triangle',  'curve-style': 'bezier'}})

    return stylesheet, bestSolution, bestPerformance, bestFound

def getSolutionDetails(run, runname, length):
    warning = None
    exceptions = "Infos about exceptions will be provided here."
    evaluation = "A detailed evaluation report will be provided here."
    info = None
    if runname == "searchspace":
        info = "Infos about the solution candidate at timestep x will be provided here."
    if runname != "searchspace":
        isValid, timestamp, components, parameterValues, performance, solExceptions = runHandler.getSolutionDetails(run, (length+1))
        timestamp = pd.to_datetime(int(timestamp), utc=True, unit='ms')
        info = "Timestamp: " + str(timestamp) + "\nComponents: " + str(components) + "\nParameter values: " + str(parameterValues) + "\nOptimisation value: " + str(performance) 
        exceptions = str(solExceptions)
        if not isValid:
            warning = "This solution is not valid according to our definition and is therefore not being visualised in the dag. (The solution probably consists of two or more components belonging to the same category)."
        evalExists, evalTime_n, FMicroAvg_n, ExactMatch_n, FMacroAvgD_n, FMacroAvgL_n, evalTime_max, evalTime_min, FMicroAvg_max, FMicroAvg_min, HammingLoss_n, evalTime_mean, ExactMatch_max, ExactMatch_min, FMacroAvgD_max, FMacroAvgD_min, FMacroAvgL_max, FMacroAvgL_min, FMicroAvg_mean, JaccardIndex_n, ExactMatch_mean, FMacroAvgD_mean, FMacroAvgL_mean, HammingLoss_max, HammingLoss_min, evalTime_median, FMicroAvg_median, HammingLoss_mean, JaccardIndex_max, JaccardIndex_min, ExactMatch_median, FMacroAvgD_median, FMacroAvgL_median, JaccardIndex_mean, HammingLoss_median, JaccardIndex_median = runHandler.getDetailedEvaluationReport(run, length)
        if evalExists:
            measurements = "Measurements:\n- evalTime_n: " + str(evalTime_n) +"\n- FMicroAvg_n: " + str(FMicroAvg_n) + "\n- ExactMatch_n: " + str(ExactMatch_n) + "\n- FMacroAvgD_n: " + str(FMacroAvgD_n) + "\n- FMacroAvgL_n: " + str(FMacroAvgL_n) + "\n- HammingLoss_n: " + str(HammingLoss_n) + "\n- JaccardIndex_n: " + str(JaccardIndex_n)
            time = "Times:\n- evalTime_min: " + str(evalTime_min) + "\n- evalTime_max: " + str(evalTime_max) + "\n- evalTime_mean: " + str(evalTime_mean) + "\n- evalTime_median: " + str(evalTime_median)
            minimisation = "Minimisation:\n- HammingLoss_min: " + str(HammingLoss_min) + "\n- HammingLoss_max: " + str(HammingLoss_max) + "\n- HammingLoss_mean: " + str(HammingLoss_mean) + "\n- HammingLoss_median: " + str(HammingLoss_median)
            maximisation = "Maximisation:\n- ExactMatch_min: " + str(ExactMatch_min) + "\n- ExactMatch_max: " + str(ExactMatch_max)+ "\n- ExactMatch_mean: " + str(ExactMatch_mean)+ "\n- ExactMatch_median: " + str(ExactMatch_median) + "\n- FMicroAvg_min: " + str(FMicroAvg_min)+ "\n- FMicroAvg_max: " + str(FMicroAvg_max) + "\n- FMicroAvg_mean: " + str(FMicroAvg_mean) + "\n- FMicroAvg_median: " + str(FMicroAvg_median)+ "\n- FMacroAvgD_min: " + str(FMacroAvgD_min)+ "\n- FMacroAvgD_max: " + str(FMacroAvgD_max) + "\n- FMacroAvgD_mean: " + str(FMacroAvgD_mean) + "\n- FMacroAvgD_median: " + str(FMacroAvgD_median)+ "\n- FMacroAvgL_min: " + str(FMacroAvgL_min) + "\n- FMacroAvgL_max: " + str(FMacroAvgL_max) + "\n- FMacroAvgL_mean: " + str(FMacroAvgL_mean)+ "\n- FMacroAvgL_median: " + str(FMacroAvgL_median)+ "\n- JaccardIndex_min: " + str(JaccardIndex_min) + "\n- JaccardIndex_max: " + str(JaccardIndex_max) + "\n- JaccardIndex_mean: " + str(JaccardIndex_mean) + "\n- JaccardIndex_median: " + str(JaccardIndex_median) 
            evaluation = measurements + "\n\n" + time + "\n\n" + minimisation + "\n\n" + maximisation
            evaluation = dcc.Markdown(evaluation)
        else: 
            evaluation = "There does not exist a detailed evaluation report."
    return info, exceptions, warning, evaluation

def createPlots(currValue, runLength):
    anytimePlot = px.scatter()
    #anytimePlotData = globalAnytimePlotData.drop(index=range(currValue, runLength))
    anytimePlot = px.line(globalAnytimePlotData, y="performance", line_shape='hv')
    parallelPlot = px.scatter()
    parallelPlot = px.parallel_categories(globalParallelCategoriesPlotData, dimensions=["kernel", "baseSLC", "metaSLC", "baseMLC", "metaMLC"])
    return anytimePlot, parallelPlot

def getPlotData():
    anytimePlotData = run.copy()
    anytimePlotData = anytimePlotData[anytimePlotData.valid == True]
    anytimePlotData = anytimePlotData["performance"]
    anytimePlotData.replace(to_replace=[None], value=0, inplace=True)
    anytimePlotData = anytimePlotData.apply(lambda x: float(x))
    anytimePlotData = anytimePlotData.cummax()
    parallelCategoriesPlotData = run.copy()
    parallelCategoriesPlotData = parallelCategoriesPlotData[parallelCategoriesPlotData.valid == True]
    parallelCategoriesPlotData = parallelCategoriesPlotData[["kernel", "baseSLC", "metaSLC", "baseMLC", "metaMLC"]]
    parallelCategoriesPlotData.replace(to_replace=[None], value="Not used", inplace=True)
    return anytimePlotData, parallelCategoriesPlotData
    
@callback(Output('bestSolution', 'children'), Output('bestSolutionHeader', 'children'), Output('controls', 'style'), Output('parallelPlot', 'figure'), Output('anytimePlot', 'figure'), Output('evalReport', 'children'), Output('solutionWarning','children'), Output('uploadError', 'children'), Output('uploadRun', 'contents'), Output('solutionHeader', 'children'), Output("solution", "children"), Output('exceptions', 'children'), Output("btnStart", "children"), Output('config', 'children'), Output('dag', 'stylesheet'), Output("slider", "max"), Output("slider", "value"), Output('interval-component', 'disabled'), Output('interval-component', 'n_intervals'),
          Input('evalMeasure', 'value'), Input('uploadRun', 'contents'), Input("btnStart", "children"), Input("btnNext", 'n_clicks'), Input('btnBack', 'n_clicks'), Input("btnMin", "n_clicks"), Input("btnMax", "n_clicks"), Input('btnStart', 'n_clicks'), Input("runSelector", "value"), Input("runRestrictions", "value"), Input("slider", "value"), Input('interval-component', 'n_intervals'),
          State('uploadRun', 'filename'), State("slider", "min"), State("slider", "max"), State('interval-component', 'disabled'))
def dag(evalMeasure, upload, btnStartSymbol, n1, n2, n3, n4, n5, runname, restrictions, currValue, intervalValue, uploadName, min, max, disabled):
    global edges
    global nodes
    edges = {}
    nodes = {}
    newStyle = style.copy()
    info = ""
    exceptions = ""
    solutionHeader = "Details about solution candidate at timestep "
    bestSolutionHeader = "Best solution until timestep "
    bestSolution = "No valid solution has been found yet."
    runLength = 0
    global run
    global runSelector
    global uploadedFile
    global uploadedRunname
    uploadError = ""
    msg = ""
    warning = None
    measure = None
    evaluation = ""
    anytimePlot = px.scatter()
    parallelPlot = px.scatter()
    global globalAnytimePlotData
    global globalParallelCategoriesPlotData
    controlsStyle = {'display': 'block'}
    
    if runname == "searchspace":
        controlsStyle = {'display': 'none'}

    if upload != None:
        if ".json" in uploadName:
            content_type, content_string = upload.split(',')
            decoded = base64.b64decode(content_string)
            convertedFile = json.load(io.StringIO(decoded.decode('utf-8')))
            data = convertedFile[2].get('data')
            run = runHandler.getRunAsDF(data, searchspace)
            uploadedRunname = uploadName
            uploadedFile = True
            runname = uploadName
            globalAnytimePlotData, globalParallelCategoriesPlotData = getPlotData()
        else:
            uploadError = "Please upload a .json file"
            return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, uploadError, upload, solutionHeader, info, exceptions, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue
        upload = None
    elif runname != "searchspace" and runname != runSelector:
        jsonFile = open(runname) 
        convertedFile = json.load(jsonFile)
        data = convertedFile[2].get('data')
        jsonFile.close()
        run = runHandler.getRunAsDF(data, searchspace)
        runSelector = runname
        uploadedFile = False
        uploadedRunname = None
        globalAnytimePlotData, globalParallelCategoriesPlotData = getPlotData()
    elif uploadedFile:
        runname = uploadedRunname
    
    if restrictions == None:
        msg = "Please enter a valid restriction (value between 0 and 1)"
        return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, uploadError, upload, solutionHeader, info, exceptions, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue
    
    if runname != "searchspace":
        runLength = runHandler.getRunLength(run)-1
    
        if "btnStart" == ctx.triggered_id and disabled:
            disabled = False 
            btnStartSymbol = "||"
        elif "btnStart" == ctx.triggered_id and not disabled:
            disabled = True
            btnStartSymbol = "▷"
        elif "btnNext" == ctx.triggered_id and currValue < max: 
            currValue += 1
            intervalValue = currValue
            disabled = True
            btnStartSymbol = "▷"
        elif "btnBack" == ctx.triggered_id and currValue > min: 
            currValue -= 1
            intervalValue = currValue
            disabled = True
            btnStartSymbol = "▷"
        elif "btnMin" == ctx.triggered_id or max != runLength: 
            currValue = min
            intervalValue = currValue
            disabled = True
            btnStartSymbol = "▷"
        elif "btnMax" == ctx.triggered_id: 
            currValue = max
            intervalValue = currValue
            disabled = True
            btnStartSymbol = "▷"
        
        if not disabled and intervalValue <= max:
            currValue = intervalValue
        elif not disabled and intervalValue > max:
            disabled = True
    
    if runname != "searchspace":
        if restrictions == 0: 
            msg = "This is the dag for \"" + runname +"\" with no restrictions at timestep " + str(currValue) + "."
        else: 
            msg = "This is the dag for \"" + runname +"\" with restriction \"performance >= " + str(restrictions) +"\" at timestep " + str(currValue) + "."
        measure = run.loc[0, "measure"]
        if measure == None:
            msg += "\nThere is no info available what measure we are optimising for. We assume maximisation of the performance value."
            if evalMeasure != "performance":
                warning = "Please be aware that currently \"" + evalMeasure + "\" is selected as evaluation measure and this measure was not used as optimisation value. The colors of the dag could therefore be misleading in the interpretation. Please select \"performance\" for interpretation."
        else:
            msg += "\nIn this searchrun we are optimising for \"" + str(measure) + "\". Therefore we want to maximise the performance value."
            if evalMeasure != "performance" and (measure not in evalMeasure):
                warning = "Please be aware that currently \"" + evalMeasure + "\" is selected as evaluation measure and this measure was not used as optimisation value. The colors of the dag could therefore be misleading in the interpretation. Please select \"performance\" for interpretation."
        msg += " Currently \"" + evalMeasure + "\" is selected as evaluation measure, hence we want to "
        if evalMeasure in ["HammingLoss_min", "HammingLoss_max", "HammingLoss_mean", "HammingLoss_median"]:
            msg += "minimise."
        else:
            msg += "maximise."
        solutionHeader += str(currValue)
        bestSolutionHeader += str(currValue) + " using " + evalMeasure + " as evaluation value"
    else:
        msg = "This is the dag showing all components and possible connections for our searchspace."
        solutionHeader += "x"
        bestSolutionHeader += "x"
        bestSolution = "Infos about the best found solution until timestep x will be provided here."

    intervalValue = currValue
    
    if restrictions != None:
        newStyle, bestSol, bestPerformance, bestFound = showSearchrun(newStyle, run, runname, restrictions, currValue, evalMeasure)
        if bestSol != None:
            bestSolution = "Found at timestep " + str(bestFound)
            isValid, timestamp, components, parameterValues, performance, solExceptions = runHandler.getSolutionDetails(run, (bestFound+1))
            timestamp = pd.to_datetime(int(timestamp), utc=True, unit='ms')
            bestSolution += "\nTimestamp: " + str(timestamp) + "\nComponents: " + str(components) + "\nParameterValues: " + str(parameterValues) + "\nEvaluation value: " + str(bestPerformance) +"\nOptimisation value: " + str(performance)
        info, exceptions, solutionWarning, evaluation = getSolutionDetails(run, runname, currValue)
        if warning != None and solutionWarning != None:
            warning += "\n\n" + solutionWarning
        elif warning == None and solutionWarning != None:
            warning = solutionWarning
        if runname != "searchspace":
            anytimePlot, parallelPlot = createPlots(currValue, runLength)
    
    return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, uploadError, upload, solutionHeader, info, exceptions, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue

if __name__ == '__main__':
    app.run(debug=True)