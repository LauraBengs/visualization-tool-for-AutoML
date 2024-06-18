import searchSpaceHandler
from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

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
        id='searchspace',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '600px'},
        elements=dataPoints,
        stylesheet=style
    )
])

if __name__ == '__main__':
    app.run(debug=True)