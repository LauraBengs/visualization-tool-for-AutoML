import searchSpaceHandler
from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

data_points = []

searchspace = searchSpaceHandler.getSearchSpaceAsDF()

print(searchspace)