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
        yK += 100
    elif categories[i] == "BaseSLC": 
        x = 300
        y = yBS
        yBS += 100
    elif categories[i] == "MetaSLC": 
        x = 600
        y = yMS
        yMS += 100
    elif categories[i] == "BaseMLC": 
        x = 900
        y = yBM
        yBM += 100
    elif categories[i] == "MetaMLC": 
        x = 1200
        y = yMM
        yMM += 100
    
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
                html.H3("Choose run"),
                dbc.RadioItems(id="runSelector", 
                    options=[
                        {"label": "best_first_747_4h", "value": "runs/best_first_747_4h.json"},
                        {"label": "gmfs_eval", "value": "runs/gmfs_eval.json"}],
                    inline=True,
                    value= "runs/best_first_747_4h.json"),
                dbc.Button('Start', id='btnStart', n_clicks=0, color="secondary"),
                html.Div(id='text')
            ], style={'backgroundColor':'#999999'}),
                
            html.Div([
                html.H3("Help"),
                html.H4("Performance"),
                html.Ul([
                    html.Li("Given by the colour of a node"),
                    html.Li("Yellow: Performance <= 0.33"),
                    html.Li("Orange: Performance <= 0.66"),
                    html.Li("Red: Performance > 0.66"),
                    html.Li("Grey: No performance value available")]),
                html.H4("Edge thickness"),
                html.Ul([
                    html.Li("Corresponds to how often a connection has been used in a solution"),
                    html.Li("Black: connections has been used more than 10 times")]),
                
            ], style={'backgroundColor':'#666666'})]),
        
        
        dbc.Col(cyto.Cytoscape(
            id='dag',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '600px'},
            elements=dataPoints,
            stylesheet=style,
            responsive=True
        ), width=8)    
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
     
@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Input('dag', 'tapNodeData'), State("modal", "is_open"))
def toggle_modal(data, is_open): 
    if data is not None:
        header, text = getInfosForModal(data)
        modalHeader = dcc.Markdown("#### " + header)
        modalText = dcc.Markdown(text)
        return not is_open, modalHeader, modalText
    return is_open, '', ''

def showSearchrun(stylesheet, runname):
    run = runHandler.getRunAsDF(runname)
    solutions = runHandler.getAllComponentSolutions(run)
    performances = runHandler.getPerformances(run)
    for s in range(0, len(solutions)):
        solComponents = solutions[s]
        solPerformance = performances[s]
        color = ""
        opacity = "1"
        if solPerformance == None:
            color = ""
        else:
            solPerformance = float(solPerformance)
            if solPerformance <= 0.33: color = "yellow"
            elif solPerformance <= 0.66: color = "orange"
            else: color = "red"
        
        for elem in solComponents:
            node = "[label = \"" + elem + "\"]"
            stylesheet.append({'selector': node, 'style': {'background-color': color, 'opacity':opacity}})
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
        

@callback(Output('text', 'children'), Output('dag', 'stylesheet'), Input('btnStart', 'n_clicks'), Input('dag', 'stylesheet'), Input("runSelector", "value"))
def displayClick(n, stylesheet, runname):
    msg = "Click start to visualise run"
    if "btnStart" == ctx.triggered_id:
        global edges
        edges = {}
        msg = "This is the visualisation for " + runname
        newStyle = showSearchrun(stylesheet, runname)
        return msg, newStyle
    return msg, style
    
 

if __name__ == '__main__':
    app.run(debug=True)