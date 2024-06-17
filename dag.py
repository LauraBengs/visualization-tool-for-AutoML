import searchSpaceHandler
from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

dataPoints = []

searchspace = searchSpaceHandler.getSearchSpaceAsDF()
allComponentNames = searchSpaceHandler.getAllComponentNames(searchspace)

x = 0
y = 0

for i in range(0, len(allComponentNames)):
    dataPoints.append({'data': {'id': str(i), 'label': allComponentNames[i]}, 'position': {'x': x, 'y': y}})
    x += 200
    if x == 2000:
        x = 0
        y += 100
        
style = [{'selector': 'node','style': {'content': 'data(label)'}}]

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