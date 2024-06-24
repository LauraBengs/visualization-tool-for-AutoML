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
                        connections.append({'data': {'source': allComponentNames[a], 'target': allComponentNames[b], 'weight':1}})
                        temp.append(allComponentNames[b])
    possibleComponentPartner.append(temp)

dataPoints = components + connections

style = [
    {'selector': 'node','style': {'content': 'data(label)'}}
    ]

app.layout = html.Div([
    dbc.Button('Start', id='btnStart', n_clicks=0, color="secondary"),
    html.Div(id='text'),
    cyto.Cytoscape(
        id='dag',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        elements=dataPoints,
        stylesheet=style
    ),
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

def showSearchrun(stylesheet):
    run = runHandler.getRunAsDF('runs/gmfs_eval.json')
    solutions = runHandler.getAllComponentSolutions(run)
    for sol in solutions:
        for elem in sol:
            sel = "[label = \"" + elem + "\"]"
            stylesheet.append({'selector': sel, 'style': {'background-color': '#FF4136'}})
    return stylesheet
        

@callback(Output('text', 'children'), Output('dag', 'stylesheet'), Input('btnStart', 'n_clicks'), Input('dag', 'stylesheet'))
def displayClick(n, stylesheet):
   if n is None or n == 0:
       return "Not clicked", stylesheet
   else:
       newStyle = showSearchrun(stylesheet)
       return f"Button was clicked {n} times", newStyle

if __name__ == '__main__':
    app.run(debug=True)