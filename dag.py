import searchSpaceHandler
import runHandler
from dash import Dash, html, Input, Output, callback, State, dcc, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)
categories = searchSpaceHandler.getAllCategories(searchspace)

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
                    if elemA in requiredInterfaces and categories[a] != categories[b]:
                        connections.append({'data': {'id':(allComponentNames[a]+"-"+allComponentNames[b]), 'source': allComponentNames[a], 'target': allComponentNames[b], 'weight':1}})
                        temp.append(allComponentNames[b])
    possibleComponentPartner.append(temp)

dataPoints = components + connections

style = [
    {'selector': 'node','style': {'content': 'data(label)'}}
    ]

app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div([
            dbc.Label("Choose run:"),
            dbc.RadioItems(id="runSelector", 
                   options=[
                       {"label": "best_first_747_4h", "value": "runs/best_first_747_4h.json"},
                       {"label": "gmfs_eval", "value": "runs/gmfs_eval.json"}],
                   inline=True,
                   value= "best_first_747_4h.json"),
            dbc.Button('Start', id='btnStart', n_clicks=0, color="secondary"),
            html.Div(id='text')
            ], style={'backgroundColor':'#999999'})),
        
        dbc.Col(cyto.Cytoscape(
            id='dag',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '600px'},
            elements=dataPoints,
            stylesheet=style
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
    for sol in solutions:
        for elem in sol:
            node = "[label = \"" + elem + "\"]"
            stylesheet.append({'selector': node, 'style': {'background-color': 'black'}})
        for i in range(0, len(sol)-1):
            edge = "#"+sol[i+1]+"-"+sol[i]
            stylesheet.append({'selector': edge, 'style':{'line-color':'black'}})
            
    return stylesheet
        

@callback(Output('text', 'children'), Output('dag', 'stylesheet'), Input('btnStart', 'n_clicks'), Input('dag', 'stylesheet'), Input("runSelector", "value"))
def displayClick(n, stylesheet, runname):
    msg = "Click start to visualise run"
    if "btnStart" == ctx.triggered_id:
        msg = "This is the visualisation for " + runname
        newStyle = showSearchrun(stylesheet, runname)
        return msg, newStyle
    return msg, style
    
 

if __name__ == '__main__':
    app.run(debug=True)