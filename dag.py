import searchSpaceHandler
import runHandler
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

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Run configurator"),
                dbc.Row([
                dbc.Col([
                    html.Div([html.H4("Choose run"),
                        dbc.RadioItems(id="runSelector", 
                            options=[
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
                            value= "runs/best_first_747_4h.json")])]),
                dbc.Col([
                    html.Div([html.H4("Restrictions"),
                        dbc.RadioItems(id="runRestrictions", 
                            options=[
                                {"label": "Show everything", "value": "all"},
                                {"label": "Performance >= 0.33", "value": "0.33"},
                                {"label": "Performance >= 0.66", "value": "0.66"},
                                {"label": "Performance > 0.9", "value": "0.9"}],
                            value= "all")])])]),
                html.Div([dbc.Button('Show graph', id='btnStart', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width': '90%'})]),
                          #dbc.Button('Start visualisation', id='btnVis', n_clicks=0, color="secondary")]),
                html.Div(id='text')
            ], style={'backgroundColor':'#999999'}),
        ]),
        
        
        dbc.Col(cyto.Cytoscape(
            id='dag',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '600px'},
            elements=dataPoints,
            stylesheet=style,
            responsive=True
        ), width=7),
        
        dbc.Col(dbc.Button('?', id='btnHelp', n_clicks=0, color="secondary", style = {'margin' : '10px', 'width':'40px'}), width=1)    
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
    )
])
 
 
def getInfosForModal(data):
    modalHeader = data['label']
    component = searchspace.loc[searchspace['name'] == modalHeader]
    modalText = searchSpaceHandler.getComponentInfo(component)
    return modalHeader, modalText
     
@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Input('btnHelp', 'n_clicks'), Input('dag', 'tapNodeData'), State("modal", "is_open"))
def toggle_modal(n, data, is_open): 
    if data is not None:
        header, text = getInfosForModal(data)
        modalHeader = dcc.Markdown("#### " + header)
        modalText = dcc.Markdown(text)
        return not is_open, modalHeader, modalText
    elif "btnHelp" == ctx.triggered_id:
        modalHeader = dcc.Markdown("#### ❔ Help/ Explanation")
        performance = "##### Performance \n - Given by the colour of a node \n - Yellow: Performance <= 0.33 \n - Orange: Performance <= 0.66 \n - Red: Performance <= 0.66 \n - Darkred: Performance > 0.9 \n - Grey: No performance value available \n"
        edge = "##### Edge thickness \n - Corresponds to how often a connection has been used in a solution \n - Black: connection has been used more than 10 times"
        modalText = dcc.Markdown(performance + edge)
        return not is_open, modalHeader, modalText
    return is_open, '', ''

def showSearchrun(stylesheet, runname, restrictions):
    run = runHandler.getRunAsDF(runname)
    solutions = runHandler.getAllComponentSolutions(run)
    performances = runHandler.getPerformances(run)
    for s in range(0, len(solutions)):
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
                    stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width': str(edges[edge])}})
                else:
                    newWeight = currentWeight +2
                    if newWeight >= 20:
                        stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width':'20', 'line-color': 'black'}})
                    else:
                        edges.update({edge: newWeight})
                        stylesheet.append({'selector': edge, 'style':{'opacity':'1', 'width': str(edges[edge])}})
            
    return stylesheet
        

@callback(Output('text', 'children'), Output('dag', 'stylesheet'), Input('btnStart', 'n_clicks'), Input('dag', 'stylesheet'), Input("runSelector", "value"), Input("runRestrictions", "value"))
def dag(n, stylesheet, runname, restrictions):
    msg = "Click \"Show graph\" to visualise run"
    if "btnStart" == ctx.triggered_id:
        global edges
        global nodes
        edges = {}
        nodes = {}
        if restrictions == "all": msg = "This is the dag for \"" + runname +"\" with no restrictions"
        else: msg = "This is the dag for \"" + runname +"\" with restrictions \"" + restrictions +"\""
        newStyle = showSearchrun(stylesheet, runname, restrictions)
        return msg, newStyle
    return msg, style


if __name__ == '__main__':
    app.run(debug=True)