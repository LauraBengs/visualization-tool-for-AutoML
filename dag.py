import searchSpaceHandler
from dash import Dash, html, Input, Output, callback, State, dcc
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
                        connections.append({'data': {'source': allComponentNames[a], 'target': allComponentNames[b]}})
                        temp.append(allComponentNames[b])
    possibleComponentPartner.append(temp)

dataPoints = components + connections

style = [
    {'selector': 'node','style': {'content': 'data(label)'}},
    {'selector': '.Kernel', 'style': { 'background-color': '#EC9F05'}},
    {'selector': '.BaseSLC', 'style': { 'background-color': '#4A6C6F'}},
    {'selector': '.MetaSLC', 'style': { 'background-color': '#A1C084'}},
    {'selector': '.BaseMLC', 'style': { 'background-color': '#A63446'}},
    {'selector': '.MetaMLC', 'style': { 'background-color': '#D89A9E'}}
    ]

app.layout = html.Div([
    cyto.Cytoscape(
        id='components',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        elements=dataPoints,
        stylesheet=style
    ),
    html.P(id='ClickedComponent'),
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
     
@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Input('components', 'tapNodeData'), State("modal", "is_open"))
def toggle_modal(data, is_open): 
    if data is not None:
        header, text = getInfosForModal(data)
        modalHeader = dcc.Markdown("#### " + header)
        modalText = dcc.Markdown(text)
        return not is_open, modalHeader, modalText
    return is_open, '', ''

if __name__ == '__main__':
    app.run(debug=True)