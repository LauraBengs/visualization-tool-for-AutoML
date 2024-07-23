import searchSpaceHandler
import runHandler
import dash
from dash import Dash, html, Input, Output, callback, State, dcc, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json 
import base64
import io

#color names
colMain = '#353A47'
colSecond = '#8A8D91'
colThird = '#e4e5eb'
colWarning = '#F7ec59'
colDanger = '#e94f37'

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)
allComponentFullNames = searchSpaceHandler.getAllComponentfullNames(searchspace)
categories = searchSpaceHandler.getAllCategories(searchspace)

runSelector = None
run = None
uploadedFile = False
uploadedRunname = None

edges = {}
nodes = {}

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
    dbc.Row([dbc.Col(html.H3("Visualisation tool for AutoML", style={'color': colThird})),
             dbc.Col(html.Button('?', id='btnHelp', n_clicks=0, style = {'margin' : '10px',
                                                                         'padding':'10px 20px',
                                                                         'background-color':colThird, 
                                                                         'color':colMain, 
                                                                         'border':'none', 
                                                                         'border-radius':'5px'}), width=1)
             ], style={'backgroundColor': colMain}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H4("Run"),
                html.Hr(style={'borderColor':colMain}),
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
                               'white-space':'pre'
                            },
                ),
                html.Div(id='uploadError'),
                html.H4("Restrictions"),
                html.Hr(style={'borderColor':colMain}),
                html.H5("Performance"),
                dcc.Input(id="runRestrictions", type="number", placeholder="Define restriction (value between 0 and 1)", min=0, max=1, step=0.1, value=0),
                html.Div("Only visualise solutions with a performance greater or equal to this value."),
                html.H4("Comment"),
                html.Hr(style={'borderColor':colMain}),
                html.Div(id='config')
            ], style={'backgroundColor':colSecond})
        ], width=2),
        
        dbc.Col([
            dbc.Row([
                html.H4("Directed acyclic graph (Dag)"),
                html.Hr(style={'borderColor':colMain})
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
                    html.Div([
                        dcc.Slider(min, max, 1, value=min, marks=None, tooltip={"placement": "bottom", "always_visible": True}, id="slider"),
                        dbc.Row([
                            dbc.Col(dbc.Button('|◁', id='btnMin', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '50px'}), width=2),
                            dbc.Col(dbc.Button('←', id='btnBack', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=2),
                            dbc.Col(dbc.Button('▷', id='btnStart', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=2),
                            dbc.Col(dbc.Button('→', id='btnNext', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=2),
                            dbc.Col(dbc.Button('▷|', id='btnMax', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '50px'}), width=2)
                        ]),
                    ], style={'backgroundColor':colSecond}),
                ], width=5),
                dbc.Col([
                    html.Div(id='solutionWarning', style={'white-space':'pre', 'background-color':colWarning}),
                    html.H5(id='solutionHeader'),
                    html.Div(id='solution', style={'white-space':'pre'}),
                    html.Details([html.Summary("Click here for a detailed evaluation report and exceptions"), html.Div(id='solutionMoreDetails')], style={'white-space':'pre'})
                ], width=7)
            ])
        ],width=10),
    ]),
    dbc.Modal(
            [
                dbc.ModalHeader(id="modal-header"),
                dbc.ModalBody(id="modal-text"),
            ],
            id="modal",
            scrollable = True,
            is_open=False,
            style = {'white-space': 'pre'},
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
        performance = "##### Performance \n - Given by the colour of a node \n - Yellow: Performance <= 0.33 \n - Orange: Performance <= 0.66 \n - Red: Performance <= 0.66 \n - Darkred: Performance > 0.9 \n - Grey: No performance value available \n"
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

def showSearchrun(stylesheet, run, runname, restrictions, length):    
    if runname == "searchspace":
        stylesheet = [
            {'selector': 'node','style': {'content': 'data(label)'}},
            {'selector': '.Kernel', 'style': { 'background-color': '#EC9F05'}},
            {'selector': '.BaseSLC', 'style': { 'background-color': '#4A6C6F'}},
            {'selector': '.MetaSLC', 'style': { 'background-color': '#A1C084'}},
            {'selector': '.BaseMLC', 'style': { 'background-color': '#A63446'}},
            {'selector': '.MetaMLC', 'style': { 'background-color': '#D89A9E'}},
            {'selector':'edge', 'style':{'line-color':'#adaaaa'}}]
        return stylesheet
   
    solutions = runHandler.getAllComponentSolutions(run)
    performances = runHandler.getPerformances(run)
    valids = runHandler.getAllValid(run)
    
    for s in range(0, length):
        solComponents = solutions[s]
        solPerformance = performances[s]
        isValid = valids[s]
        
        if isValid == False:
            continue
        
        color = ""
        opacity = "0"
        if solPerformance == None:
            color = ""
            if restrictions == 0:
                opacity = "1"
        else:
            solPerformance = float(solPerformance)
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
            
    return stylesheet

def getSolutionDetails(run, runname, length):
    warning = ""
    infoDetails = "An evaluation report as well as exceptions will be provided here."
    info = "Please click start, skip to the next timstep or drag the slider to get infos about a specifc solution candidate."
    if runname == "searchspace":
        info = "Infos about the solution candidate at timestep x will be provided here."
    if length != 0 and runname != "searchspace":
        isValid, timestamp, components, parameterValues, performance, exceptions = runHandler.getSolutionDetails(run, length)
        info = "Timestamp: " + str(timestamp) + "Components: " + str(components) + "\nParameterValues: " + str(parameterValues) + "\nPerformance value: " + str(performance) 
        infoDetails = "Exceptions: " + str(exceptions)
        if not isValid:
            warning = "Warning: This solution is not valid according to our definition and is therefore not being visualised in the dag.\n(The solution probably consists of two or more components belonging to the same category)."
    return info, infoDetails, warning
        

@callback(Output('solutionWarning','children'), Output('uploadError', 'children'), Output('uploadRun', 'contents'), Output('solutionHeader', 'children'), Output("solution", "children"), Output('solutionMoreDetails', 'children'), Output("btnStart", "children"), Output('config', 'children'), Output('dag', 'stylesheet'), Output("slider", "max"), Output("slider", "value"), Output('interval-component', 'disabled'), Output('interval-component', 'n_intervals'),
          Input('uploadRun', 'contents'), Input("btnStart", "children"), Input("btnNext", 'n_clicks'), Input('btnBack', 'n_clicks'), Input("btnMin", "n_clicks"), Input("btnMax", "n_clicks"), Input('btnStart', 'n_clicks'), Input("runSelector", "value"), Input("runRestrictions", "value"), Input("slider", "value"), Input('interval-component', 'n_intervals'),
          State('uploadRun', 'filename'), State("slider", "min"), State("slider", "max"), State('interval-component', 'disabled'))
def dag(upload, btnStartSymbol, n1, n2, n3, n4, n5, runname, restrictions, currValue, intervalValue, uploadName, min, max, disabled):
    global edges
    global nodes
    edges = {}
    nodes = {}
    newStyle = style.copy()
    info = ""
    infoMoreDetails = ""
    solutionHeader = "Details about solution candidate at timestep "
    runLength = 0
    global run
    global runSelector
    global uploadedFile
    global uploadedRunname
    uploadError = ""
    msg = ""
    warning = ""

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
        else:
            uploadError = "Please upload a .json file"
            return warning, uploadError, upload, solutionHeader, info, infoMoreDetails, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue
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
    elif uploadedFile:
        runname = uploadedRunname
    
    if restrictions == None:
        msg = "Please enter a valid restriction (value between 0 and 1)"
        return warning, uploadError, upload, solutionHeader, info, infoMoreDetails, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue
    
    if runname != "searchspace":
        runLength = runHandler.getRunLength(run)
    
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
    
    if restrictions == 0: 
        msg = "This is the dag for \"" + runname +"\" with no restrictions at timestep " + str(currValue)
    else: 
        msg = "This is the dag for \"" + runname +"\" with restriction \"performance >= " + str(restrictions) +"\" at timestep " + str(currValue)
    
    solutionHeader += str(currValue)
    
    if runname == "searchspace":
        msg = "This is the dag showing all components and possible connections for our searchspace"
        solutionHeader = "Details about solution candidate at timestep x"

    intervalValue = currValue
    
    if restrictions != None:
        newStyle = showSearchrun(newStyle, run, runname, restrictions, currValue)
        info, infoMoreDetails, warning = getSolutionDetails(run, runname, currValue)
    
    return warning, uploadError, upload, solutionHeader, info, infoMoreDetails, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue

if __name__ == '__main__':
    app.run(debug=True)