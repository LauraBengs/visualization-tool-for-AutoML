import searchSpaceHandler
import runHandler
import dash
from dash import Dash, html, Input, Output, callback, State, dcc, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)
allComponentFullNames = searchSpaceHandler.getAllComponentfullNames(searchspace)
categories = searchSpaceHandler.getAllCategories(searchspace)

edges = {}
nodes = {}

x = 0
y = 0
yK = 0
yBS = 0
yMS = 0
yBM = 0
yMM = 0

components = []

for i in range(0, len(allComponentNames)):
    if categories[i] == "Kernel": 
        x = 0
        y = yK
        yK += 60
    elif categories[i] == "BaseSLC": 
        x = 300
        y = yBS
        yBS += 60
    elif categories[i] == "MetaSLC": 
        x = 600
        y = yMS
        yMS += 60
    elif categories[i] == "BaseMLC": 
        x = 900
        y = yBM
        yBM += 60
    elif categories[i] == "MetaMLC": 
        x = 1200
        y = yMM
        yMM += 60
    
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
            dbc.Row([
                html.H3("Visualisation configurator"),
                    html.Div([html.H4("Choose run"),
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
                    html.Div([html.H4("Restrictions"),
                        dcc.Dropdown(id="runRestrictions", 
                            options=[
                                {"label": "Show everything", "value": "all"},
                                {"label": "Performance >= 0.33", "value": "0.33"},
                                {"label": "Performance >= 0.66", "value": "0.66"},
                                {"label": "Performance > 0.9", "value": "0.9"}],
                            value= "all",
                            clearable=False)]),
                html.H3("Comment"),
                html.Div(id='config')
            ], style={'backgroundColor':'#999999'})
        ]),
        
        dbc.Col(html.Div([
            dbc.Row([
                dbc.Col(dbc.Button('|◁', id='btnMin', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '50px'}), width=1),
                dbc.Col(dbc.Button('←', id='btnBack', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=1),
                dbc.Col(dbc.Button('▷', id='btnStart', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=1),
                dbc.Col(dbc.Button('→', id='btnNext', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '40px'}), width=1),
                dbc.Col(dbc.Button('▷|', id='btnMax', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '50px'}), width=1),
                dbc.Col(html.Div(dcc.Slider(min, max, 1, 
                           value=min,
                           marks=None,
                           tooltip={"placement": "bottom", "always_visible": True},
                           id="slider"
            )), style = {'margin' : '20px'})], style={'backgroundColor':'#878787'}),
            html.Div(id="temp"),
            cyto.Cytoscape(
                id='dag',
                layout={'name': 'preset'},
                style={'width': '100%', 'height': '600px'},
                elements=dataPoints,
                stylesheet=style,
                responsive=True
            )]),width=7),
        
        dbc.Col(dbc.Button('?', id='btnHelp', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width':'40px'}), width=1)    
    ]),
    dbc.Row([
                html.H4("Details about solution candidate"),
                html.Div(id='solution')
            ], style={'backgroundColor':'#878787'}),
    
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
        edge = "##### Edges \n - Thickness corresponds to how often a connection has been used in a solution \n - Color black: connection has been used more than 10 times"
        modalText = dcc.Markdown(performance + edge)
        return not is_open, modalHeader, modalText
    elif data is not None:
        header, text = getInfosForModal(data)
        modalHeader = dcc.Markdown("#### " + header)
        modalText = dcc.Markdown(text)
        return not is_open, modalHeader, modalText
    return is_open, '', ''

def showSearchrun(stylesheet, runname, restrictions, length):
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
    run = runHandler.getRunAsDF(runname)
    solutions = runHandler.getAllComponentSolutions(run)
    performances = runHandler.getPerformances(run)
    for s in range(0, length):
        solComponents = solutions[s]
        solPerformance = performances[s]
        color = ""
        opacity = "0"
        if solPerformance == None:
            color = ""
            if restrictions == "all":
                opacity = "1"
        else:
            solPerformance = float(solPerformance)
            if solPerformance <= 0.33: color = "yellow"
            elif solPerformance <= 0.66: color = "orange"
            elif solPerformance <= 0.9: color = "red"
            else: color = "darkred"
            
            if (restrictions == "all") or (restrictions == "0.66" and solPerformance >= 0.66) or (restrictions == "0.33" and solPerformance >= 0.33) or (restrictions == "0.9" and solPerformance > 0.9):
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

def getSolutionDetails(runname, length):
    info = ""        
    if length != 0 and runname != "searchspace":
        timestamp, components, parameterValues, performance, exceptions = runHandler.getSolutionDetails(runname, length)
        info = "Timestamp: "+ str(timestamp) +"\nComponents: " + str(components) + "\nParameterValues: " + str(parameterValues) + "\nPerformance value: " + str(performance) +"\nExceptions: " + str(exceptions)
    return info
        

@callback(Output("solution", "children"), Output("btnStart", "children"), Output('config', 'children'), Output('dag', 'stylesheet'), Output("slider", "max"), Output("slider", "value"), Output('interval-component', 'disabled'), Output('interval-component', 'n_intervals'),
          Input("btnStart", "children"), Input("btnNext", 'n_clicks'), Input('btnBack', 'n_clicks'), Input("btnMin", "n_clicks"), Input("btnMax", "n_clicks"), Input('btnStart', 'n_clicks'), Input("runSelector", "value"), Input("runRestrictions", "value"), Input("slider", "value"), Input('interval-component', 'n_intervals'),
          State("slider", "min"), State("slider", "max"), State('interval-component', 'disabled'))
def dag(btnStartSymbol, n1, n2, n3, n4, n5, runname, restrictions, currValue, intervalValue, min, max, disabled):
    global edges
    global nodes
    edges = {}
    nodes = {}
    newStyle = style.copy()
    
    if runname == "searchspace":
        runLength = 0
    else:
        runLength = runHandler.getRunLength(runname)
    
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
    
    if restrictions == "all": 
        msg = "This is the dag for \"" + runname +"\" with no restrictions at timestep " + str(currValue)
    else: 
        msg = "This is the dag for \"" + runname +"\" with restrictions \"" + restrictions +"\" at timestep" + str(currValue)
    
    if runname == "searchspace":
        msg = "This is the dag showing all components and possible connections for our searchspace"
    
    newStyle = showSearchrun(newStyle, runname, restrictions, currValue)
    intervalValue = currValue
    info = getSolutionDetails(runname, currValue)
    
    return info, btnStartSymbol, msg, newStyle, runLength, currValue, disabled, intervalValue

if __name__ == '__main__':
    app.run(debug=True)