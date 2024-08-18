from dash import Dash, html, Input, Output, callback, State, dcc, ctx, dash_table
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json
import base64
import io
import plotly.express as px
import pandas as pd
import searchSpaceHandler
import runHandler
import dagHandler

# debugging and testing
pd.options.display.max_columns = None
pd.options.display.max_rows = None
# debugging and testing

# global variables
runSelector = None
run = None
uploadedFile = False
uploadedRunname = None

globalAnytimePlotData = None
globalParallelCategoriesPlotData = None

edges = {}
nodes = {}

min = 0
max = 0

overview = ""

searchspace = searchSpaceHandler.getSearchSpaceAsDF()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Visualisation tool for AutoML"

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row(html.Div([
                dbc.Row([
                    dbc.Col(html.H4("Run"), width=3),
                    dbc.Col(html.Button('i', id='btnInfoRun', n_clicks=0, className="infoButton"), width=1),
                    html.Hr(),
                ]),
                html.Div([html.H5("Select run"),
                          dcc.Dropdown(id="runSelector", options=[{"label": "Show searchspace", "value": "searchspace"},
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
                                       value="searchspace",
                                       clearable=False)]),
                html.H5("Upload run"),
                dcc.Upload(id='uploadRun', children=html.Div(['Drag and Drop or \n', html.A('Select Files')]),
                           style={
                               'width': '100%',
                               'height': '60px',
                               'lineHeight': '30px',
                               'borderWidth': '1px',
                               'borderStyle': 'dashed',
                               'borderRadius': '5px',
                               'textAlign': 'center'},
                           ),
                html.H4("Restrictions"),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H5("Performance"), width=7),
                    dbc.Col(html.Button('i', id='btnInfoPerformance', n_clicks=0, className="infoButton"), width=1),
                    html.Hr(),
                ]),
                dcc.Input(id="runRestrictions", type="number", placeholder="Define restriction (value between 0 and 1)", min=0, max=1, step=0.1, value=0),
                html.H4("Evaluation Measure"),
                html.Hr(),
                dcc.Dropdown(id="evalMeasure",
                             options=[
                                {"label": "performance", "value": "performance"},
                                {"label": "HammingLoss_min", "value": "HammingLoss_min"},
                                {"label": "HammingLoss_max", "value": "HammingLoss_max"},
                                {"label": "HammingLoss_mean", "value": "HammingLoss_mean"},
                                {"label": "HammingLoss_median", "value": "HammingLoss_median"},
                                {"label": "ExactMatch_min", "value": "ExactMatch_min"},
                                {"label": "ExactMatch_max", "value": "ExactMatch_max"},
                                {"label": "ExactMatch_mean", "value": "ExactMatch_mean"},
                                {"label": "ExactMatch_median", "value": "ExactMatch_median"},
                                {"label": "FMicroAvg_min", "value": "FMicroAvg_min"},
                                {"label": "FMicroAvg_max", "value": "FMicroAvg_max"},
                                {"label": "FMicroAvg_mean", "value": "FMicroAvg_mean"},
                                {"label": "FMicroAvg_median", "value": "FMicroAvg_median"},
                                {"label": "FMacroAvgD_min", "value": "FMacroAvgD_min"},
                                {"label": "FMacroAvgD_max", "value": "FMacroAvgD_max"},
                                {"label": "FMacroAvgD_mean", "value": "FMacroAvgD_mean"},
                                {"label": "FMacroAvgD_median", "value": "FMacroAvgD_median"},
                                {"label": "FMacroAvgL_min", "value": "FMacroAvgL_min"},
                                {"label": "FMacroAvgL_max", "value": "FMacroAvgL_max"},
                                {"label": "FMacroAvgL_mean", "value": "FMacroAvgL_mean"},
                                {"label": "FMacroAvgL_median", "value": "FMacroAvgL_median"},
                                {"label": "JaccardIndex_min", "value": "JaccardIndex_min"},
                                {"label": "JaccardIndex_max", "value": "JaccardIndex_max"},
                                {"label": "JaccardIndex_mean", "value": "JaccardIndex_mean"},
                                {"label": "JaccardIndex_median", "value": "JaccardIndex_median"},
                             ],
                             value="performance",
                             clearable=False)
            ], className='sidebar'))
        ], width=2),

        dbc.Col([
            dbc.Row([
                dbc.Col(html.H4("Directed acyclic graph (Dag)"), width=4),
                dbc.Col(html.Button('i', id='btnInfoDag', n_clicks=0, className="infoButton"), width=1),
                html.Hr()
            ]),
            dbc.Row([
                html.Div(id='solutionWarning', className='warning'),
                dbc.Col([
                    cyto.Cytoscape(
                        id='dag',
                        layout={'name': 'preset'},
                        style={'width': '100%', 'height': '400px'},
                        elements=dagHandler.getDatapoints(),
                        stylesheet=dagHandler.getStyle(),
                        responsive=True),
                ], width=6),
                dbc.Col([
                    html.H5(id='bestSolutionHeader'),
                    html.Hr(),
                    html.Div(id='bestSolution'),
                    html.H5(id='solutionHeader'),
                    html.Hr(),
                    html.Div(id='solution'),
                    html.Details([html.Summary("Click here for exceptions"), html.Div(id='exceptions')]),
                    html.Details([html.Summary("Click here for a detailed evaluation report"), html.Div(id='evalReport')])
                ], width=6)
            ]),
            dbc.Row([
                html.H4("Anytime performance plot"),
                html.Hr(),
                dcc.Graph(id='anytimePlot', figure=px.scatter())
            ]),
            dbc.Row([
                html.H4("Parallel categories plot"),
                html.Hr(),
                dcc.Graph(id='parallelPlot', figure=px.scatter())
            ])
        ], width=10),
    ]),

    html.Div(
        dbc.Row([
            dbc.Col(html.H3("Visualisation tool for AutoML", className='headline'), width=4),
            dbc.Col(html.Button('?', id='btnHelp', n_clicks=0), width=1),
            dbc.Col(html.Div([
                dcc.Slider(min, max, 1, value=min, marks=None, tooltip={"placement": "bottom", "always_visible": True}, id="slider"),
                dbc.Row([
                    dbc.Col(html.Button('|◁', id='btnMin', n_clicks=0), width=2),
                    dbc.Col(html.Button('←', id='btnBack', n_clicks=0), width=2),
                    dbc.Col(html.Button('▷', id='btnStart', n_clicks=0), width=2),
                    dbc.Col(html.Button('→', id='btnNext', n_clicks=0), width=2),
                    dbc.Col(html.Button('▷|', id='btnMax', n_clicks=0), width=2)
                ]),
            ], id='controls', style={'display': 'none'}))
        ]),
        className='footer'
    ),

    dbc.Modal(
        [
            dbc.ModalHeader(id="modal-header"),
            dbc.ModalBody([html.Div(id="modal-text"),
                           html.Div(id="modal-table")]),

        ],
        id="modal",
        scrollable=True,
        is_open=False,
        style={'white-space': 'pre-wrap'},
        size="xl"
    ),

    dbc.Modal(
        [
            dbc.ModalHeader(id="smallModal-header"),
            dbc.ModalBody(id="smallModal-text")
        ],
        id="smallModal",
        scrollable=True,
        is_open=False,
        style={'white-space': 'pre-wrap'},
    ),

    dcc.Interval(id='interval-component', interval=800, n_intervals=0, disabled=True),
])


def getInfosForModal(data, currValue):
    componentName = data['label']
    component = searchspace.loc[searchspace['name'] == componentName]
    generalInfo = searchSpaceHandler.getComponentInfo(component)
    runInfo = None

    if runSelector != "searchspace":
        componentCategory = searchSpaceHandler.getComponentCategory(componentName, searchspace)

        info = run.copy()
        info = info.iloc[:currValue+1]
        info = info[info.valid == True]
        info = info[info[componentCategory] == componentName]

        parameterList = searchSpaceHandler.getComponentParameters(componentName, searchspace)
        if parameterList != []:
            newData = {}
            for parameter in parameterList:
                newData[parameter] = []

            for i in range(0, runHandler.getRunLength(info)):
                componentsList = info["components"].values[i]
                index = componentsList.index(componentName)
                parameterValues = info["parameterValues"].values[i]
                componentParameterValues = parameterValues[index]
                for parameter in parameterList:
                    parameterValue = componentParameterValues.get(parameter)
                    newData[parameter].append(parameterValue)

            for parameter in parameterList:
                dataToBeAdded = newData[parameter]
                info.insert(8, parameter, dataToBeAdded, True)

        info = info[["timestamp", "performance", "kernel", "baseSLC", "metaSLC", "baseMLC", "metaMLC"] + parameterList + ["exceptions"]]
        timesteps = list(info.index.values)
        info.insert(0, "timestep", timesteps, True)
        runInfo = dash_table.DataTable(info.to_dict("records"), [{"name": i, "id": i} for i in info.columns], style_cell={'textAlign': 'left'})

    return componentName, generalInfo, runInfo


@callback(Output("modal", "is_open"), Output("modal-header", "children"), Output("modal-text", "children"), Output("modal-table", "children"),
          Input('dag', 'tapNodeData'),
          State("modal", "is_open"), State("slider", "value"))
def toggle_modal(data, is_open, currValue):
    triggeredID = ctx.triggered_id

    if triggeredID == "dag" and data is not None:
        header, generalInfo, runInfo = getInfosForModal(data, currValue)
        modalHeader = dcc.Markdown("#### " + header)
        if runSelector != "searchspace":
            modalText = dcc.Markdown(generalInfo + "\n\n ---")
        else:
            modalText = dcc.Markdown(generalInfo)
        return not is_open, modalHeader, modalText, runInfo

    return is_open, '', '', ''


@callback(Output("smallModal", "is_open"), Output('smallModal-header', 'children'), Output('smallModal-text', 'children'),
          Input('btnInfoDag', 'n_clicks'), Input('btnHelp', 'n_clicks'), Input('btnInfoRun', 'n_clicks'), Input('btnInfoPerformance', 'n_clicks'),
          State('modal', 'is_open'))
def documentation(n1, n2, n3, n4, is_open):
    global overview
    triggeredID = ctx.triggered_id

    if triggeredID == "btnInfoDag":
        modalHeader = dcc.Markdown("#### Directed acyclic graph (Dag)")
        modalText = dcc.Markdown(overview)
        return not is_open, modalHeader, modalText

    elif triggeredID == "btnHelp":
        modalHeader = dcc.Markdown("#### ❔ Help/ Explanation")
        performance = "##### Performance \n - Given by the colour of a node \n - Maximisation: yellow to darkred \n - Minimisation: blue \n - Grey: No performance value available \n"
        edge = "##### Edges \n - Thickness corresponds to how often a connection has been used in a solution \n - Color black: connection has been used more than 10 times \n"
        filter = "##### Filter \n Solution candidates that contain two or more components from one categorie will not be visualised. \n A corresponding message about why a solution candidate is not being visualised can be found in the details section."
        modalText = dcc.Markdown(performance + edge + filter)
        return not is_open, modalHeader, modalText

    elif triggeredID == "btnInfoRun":
        modalHeader = "Run"
        modalText = "Select a preloaded run or upload a .json file of your searchrun."
        return not is_open, modalHeader, modalText

    elif triggeredID == "btnInfoPerformance":
        modalHeader = "Performance"
        modalText = "Only visualise solutions with a performance greater or equal to the following value."
        return not is_open, modalHeader, modalText

    return is_open, "", ""


def showSearchrun(stylesheet, run, restrictions, length, evalMeasure):
    solutions = run["components"].to_numpy()
    performances = run[evalMeasure].to_numpy()
    valids = run["valid"].to_numpy()

    minimisation = evalMeasure in ["HammingLoss_min", "HammingLoss_max", "HammingLoss_mean", "HammingLoss_median"]
    bestSolution = None
    if minimisation:
        bestPerformance = 1
    else:
        bestPerformance = 0
    bestFound = 0

    for s in range(length+1):
        solComponents = solutions[s]
        solPerformance = performances[s]
        isValid = valids[s]

        if not isValid:
            continue

        visualise = False
        if (pd.isna(solPerformance) and restrictions == 0) or solPerformance >= restrictions:
            visualise = True

        if visualise:
            for elem in solComponents:
                global nodes
                color = ""

                currentBestPerformance = nodes.get(elem)

                if currentBestPerformance == None:
                    nodes[elem] = solPerformance
                elif pd.isna(currentBestPerformance):
                    nodes.update({elem: solPerformance})
                elif solPerformance > currentBestPerformance:
                    nodes.update({elem: solPerformance})

                currentBestPerformance = nodes.get(elem)
                if not pd.isna(currentBestPerformance):
                    color = dagHandler.getNodeColor(currentBestPerformance, minimisation)

                node = "[label = \"" + elem + "\"]"
                stylesheet.append({'selector': node, 'style': {'background-color': color, 'opacity': "1"}})

            for i in range(0, len(solComponents)-1):
                edge = "#"+solComponents[i+1]+"-"+solComponents[i]
                global edges
                currentWeight = edges.get(edge)
                if currentWeight == None:
                    edges[edge] = 1
                    stylesheet.append({'selector': edge, 'style': {'opacity': '1', 'width': str(edges[edge]), 'target-arrow-shape': 'triangle', 'curve-style': 'bezier'}})
                else:
                    newWeight = currentWeight + 2
                    if newWeight >= 20:
                        stylesheet.append({'selector': edge, 'style': {'opacity': '1', 'width': '20', 'line-color': 'black', 'target-arrow-shape': 'triangle', 'target-arrow-color': 'black', 'curve-style': 'bezier'}})
                    else:
                        edges.update({edge: newWeight})
                        stylesheet.append({'selector': edge, 'style': {'opacity': '1', 'width': str(edges[edge]), 'target-arrow-shape': 'triangle',  'curve-style': 'bezier'}})

            if not pd.isna(solPerformance):
                if (minimisation and solPerformance < bestPerformance) or (not minimisation and solPerformance > bestPerformance):
                    bestPerformance = solPerformance
                    bestSolution = solComponents
                    bestFound = s

    return stylesheet, bestSolution, bestPerformance, bestFound


def getSolutionDetails(run, length):
    warning = None
    exceptions = None
    evaluation = None
    info = None

    isValid, timestamp, components, parameterValues, performance, solExceptions = runHandler.getSolutionDetails(run, length)

    if not isValid:
        warning = "This solution is not valid according to our definition and is therefore not being visualised in the dag. (The solution probably consists of two or more components belonging to the same category)."

    if pd.isna(performance):
        performance = None
    info = "Timestamp: " + str(timestamp) + "\nComponents: " + str(components) + "\nParameter values: " + str(parameterValues) + "\nOptimisation value: " + str(performance)

    if pd.isna(solExceptions):
        exceptions = "There are no exceptions for this solution."
    else:
        exceptions = str(solExceptions)

    evalExists, evalReport = runHandler.getDetailedEvaluationReport(run, length)
    if evalExists:
        measurements = "Measurements:"
        for measure in runHandler.dimensions:
            measurements += "\n- " + measure + ": " + str(evalReport[measure])

        time = "Times:"
        for measure in runHandler.times:
            time += "\n- " + measure + ": " + str(evalReport[measure])

        minimisation = "Minimisation:"
        for measure in runHandler.minimisation:
            minimisation += "\n- " + measure + ": " + str(evalReport[measure])

        maximisation = "Maximisation:"
        for measure in runHandler.maximisation:
            maximisation += "\n- " + measure + ": " + str(evalReport[measure])

        evaluation = measurements + "\n\n" + time + "\n\n" + minimisation + "\n\n" + maximisation
        evaluation = dcc.Markdown(evaluation)
    else:
        evaluation = "There does not exist a detailed evaluation report."

    return info, exceptions, warning, evaluation


def createPlots(currValue):
    anytimePlot = px.scatter()
    anytimePlot = px.line(globalAnytimePlotData, y="performance", line_shape='hv')
    anytimePlot.add_vline(x=currValue, line_color="red")
    parallelPlot = px.scatter()
    parallelPlot = px.parallel_categories(globalParallelCategoriesPlotData, dimensions=["kernel", "baseSLC", "metaSLC", "baseMLC", "metaMLC"])
    return anytimePlot, parallelPlot


def getPlotData():
    anytimePlotData = run.copy()
    anytimePlotData = anytimePlotData[anytimePlotData.valid == True]
    anytimePlotData = anytimePlotData["performance"]
    anytimePlotData = anytimePlotData.fillna(0)
    anytimePlotData = anytimePlotData.apply(lambda x: float(x))
    anytimePlotData = anytimePlotData.cummax()
    parallelCategoriesPlotData = run.copy()
    parallelCategoriesPlotData = parallelCategoriesPlotData[parallelCategoriesPlotData.valid == True]
    parallelCategoriesPlotData = parallelCategoriesPlotData[["kernel", "baseSLC", "metaSLC", "baseMLC", "metaMLC"]]
    parallelCategoriesPlotData = parallelCategoriesPlotData.fillna("Not used")
    return anytimePlotData, parallelCategoriesPlotData


@callback(Output('bestSolution', 'children'), Output('bestSolutionHeader', 'children'), Output('controls', 'style'), Output('parallelPlot', 'figure'), Output('anytimePlot', 'figure'), Output('evalReport', 'children'), Output('solutionWarning', 'children'), Output('uploadRun', 'contents'), Output('solutionHeader', 'children'), Output("solution", "children"), Output('exceptions', 'children'), Output("btnStart", "children"), Output('dag', 'stylesheet'), Output("slider", "max"), Output("slider", "value"), Output('interval-component', 'disabled'), Output('interval-component', 'n_intervals'),
          Input('evalMeasure', 'value'), Input('uploadRun', 'contents'), Input("btnStart", "children"), Input("btnNext", 'n_clicks'), Input('btnBack', 'n_clicks'), Input("btnMin", "n_clicks"), Input("btnMax", "n_clicks"), Input('btnStart', 'n_clicks'), Input("runSelector", "value"), Input("runRestrictions", "value"), Input("slider", "value"), Input('interval-component', 'n_intervals'),
          State('uploadRun', 'filename'), State("slider", "min"), State("slider", "max"), State('interval-component', 'disabled'))
def interactions(evalMeasure, upload, btnStartSymbol, n1, n2, n3, n4, n5, runname, restrictions, currValue, intervalValue, uploadName, min, max, disabled):
    global edges
    global nodes
    edges = {}
    nodes = {}
    newStyle = dagHandler.getStyle()
    info = ""
    exceptions = ""
    solutionHeader = "Details about solution candidate at timestep "
    bestSolutionHeader = "Best solution until timestep "
    bestSolution = "No valid solution has been found yet."
    runLength = 0
    global run
    global runSelector
    global uploadedFile
    global uploadedRunname
    msg = ""
    warning = None
    measure = None
    evaluation = ""
    anytimePlot = px.scatter()
    parallelPlot = px.scatter()
    global globalAnytimePlotData
    global globalParallelCategoriesPlotData
    controlsStyle = {'display': 'block'}
    global overview

    if upload != None:
        if ".json" in uploadName:
            _, content_string = upload.split(',')
            decoded = base64.b64decode(content_string)
            convertedFile = json.load(io.StringIO(decoded.decode('utf-8')))
            data = convertedFile[2].get('data')
            run = runHandler.getRunAsDF(data, searchspace)
            uploadedRunname = uploadName
            uploadedFile = True
            runname = uploadName
            globalAnytimePlotData, globalParallelCategoriesPlotData = getPlotData()
        else:
            warning = "Please upload a .json file"
            return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, upload, solutionHeader, info, exceptions, btnStartSymbol, newStyle, runLength, currValue, disabled, intervalValue
        upload = None
    elif runname != "searchspace" and runname != runSelector:
        jsonFile = open(runname)
        convertedFile = json.load(jsonFile)
        data = convertedFile[2].get('data')
        jsonFile.close()
        run = runHandler.getRunAsDF(data, searchspace)
        runSelector = runname
        uploadedFile = False
        uploadedRunname = None
        globalAnytimePlotData, globalParallelCategoriesPlotData = getPlotData()
    elif uploadedFile:
        runname = uploadedRunname
    elif runname == "searchspace" and runname != runSelector:
        run = None
        runSelector = runname
        uploadedFile = False
        uploadedRunname = None

    if restrictions == None:
        warning = "Please enter a valid restriction (value: between 0 and 1, steps: 0.1)"
        return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, upload, solutionHeader, info, exceptions, btnStartSymbol, newStyle, runLength, currValue, disabled, intervalValue

    if runname == "searchspace":
        controlsStyle = {'display': 'none'}
        msg = "This is the dag showing all components and possible connections for this searchspace."
        solutionHeader += "x"
        bestSolutionHeader += "x"
        bestSolution = "Infos about the best found solution until timestep x will be provided here."
        info = "Infos about the solution candidate at timestep x will be provided here."
        exceptions = "Infos about exceptions will be provided here."
        evaluation = "A detailed evaluation report will be provided here."
        newStyle = dagHandler.stylesheetSearchspace
    else:
        runLength = runHandler.getRunLength(run)-1

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

        msg = "\n- Run: This is the dag for \"" + runname + "\" at timestep " + str(currValue) + "."
        if restrictions == 0:
            msg += "\n- Restrictions: No restrictions have been selected."
        else:
            msg += "\n- Restrictions: Only solutions with a \"performance >= " + str(restrictions) + " are being visualised."

        measure = run.loc[0, "measure"]
        if pd.isna(measure):
            msg += "\n- Optimisation: We assume maximisation of the performance value, as there is no info available what measure we are optimising for."
            if evalMeasure != "performance":
                warning = "Please be aware that currently \"" + evalMeasure + "\" is selected as evaluation measure and this measure was not used as optimisation value. The colors of the dag could therefore be misleading in the interpretation. Please select \"performance\" for interpretation."
        else:
            msg += "\n- Optimisation: In this searchrun we are optimising for \"" + str(measure) + "\". Therefore we want to maximise the performance value."
            if evalMeasure != "performance" and (measure not in evalMeasure):
                warning = "Please be aware that currently \"" + evalMeasure + "\" is selected as evaluation measure and this measure was not used as optimisation value. The colors of the dag could therefore be misleading in the interpretation. Please select \"performance\" for interpretation."
        msg += "\n- Evaluation measure: Currently \"" + evalMeasure + "\" is selected as evaluation measure, hence "
        if evalMeasure in ["HammingLoss_min", "HammingLoss_max", "HammingLoss_mean", "HammingLoss_median"]:
            msg += "smaller values are better."
        else:
            msg += "greater values are better."

        solutionHeader += str(currValue)
        bestSolutionHeader += str(currValue) + " using " + evalMeasure + " as evaluation value"

        newStyle, bestSol, bestPerformance, bestFound = showSearchrun(newStyle, run, restrictions, currValue, evalMeasure)
        if bestSol != None:
            bestSolution = "Found at timestep " + str(bestFound)
            _, timestamp, components, parameterValues, performance, _ = runHandler.getSolutionDetails(run, bestFound)
            bestSolution += "\nTimestamp: " + str(timestamp) + "\nComponents: " + str(components) + "\nParameterValues: " + str(parameterValues) + "\nEvaluation value: " + str(bestPerformance) + "\nOptimisation value: " + str(performance)

        info, exceptions, solutionWarning, evaluation = getSolutionDetails(run, currValue)
        if warning != None and solutionWarning != None:
            warning += "\n\n" + solutionWarning
        elif warning == None and solutionWarning != None:
            warning = solutionWarning

        anytimePlot, parallelPlot = createPlots(currValue)

    intervalValue = currValue

    overview = msg

    return bestSolution, bestSolutionHeader, controlsStyle, parallelPlot, anytimePlot, evaluation, warning, upload, solutionHeader, info, exceptions, btnStartSymbol, newStyle, runLength, currValue, disabled, intervalValue


if __name__ == '__main__':
    app.run(debug=True)
