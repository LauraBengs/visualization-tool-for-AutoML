import searchSpaceHandler
from dash import Dash, html, dcc, Input, Output, callback, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dataPoints = []

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)
categories = searchSpaceHandler.getAllCategories(searchspace)

x = 0
y = 0

for i in range(0, len(allComponentNames)):
    dataPoints.append({'data': {'id': str(i), 'label': allComponentNames[i]}, 'position': {'x': x, 'y': y}, 'classes': categories[i]})
    x += 200
    if x == 2000:
        x = 0
        y += 100
        
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
            is_open=False,
        )
])
 
@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Input('components', 'tapNodeData'), State("modal", "is_open"))
def toggle_modal(data, is_open): 
    if data is not None:
        modalHeader = data['label']
        modalText = "Soon more info about this component will be available!"
        return not is_open, modalHeader, modalText
    return is_open, '', ''

if __name__ == '__main__':
    app.run(debug=True)