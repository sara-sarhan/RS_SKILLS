import os
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash
import base64
from controller import Controller
from datetime import date
import predict
from dash import dcc, html
import warnings
import time
import pandas as pd
import numpy as np
from dash import Dash, dash_table
warnings.filterwarnings("ignore")
## Diskcache
import flask

from waitress import serve

_start_time = time.time()


def tic():
    global _start_time
    _start_time = time.time()


from datetime import datetime


def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec, 60)
    (t_hour, t_min) = divmod(t_min, 60)
    print('{}:{}:{}.'.format(t_hour, t_min, t_sec))
    tim = str(t_hour) + ":" + str(t_min) + ":" + str(t_sec)
    print(tim)
    dt = datetime.strptime(tim, '%H:%M:%S')

    return dt

server = flask.Flask(__name__)
app = dash.Dash(
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # serve_locally=False,
)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    dcc.Link('Navigate to "/page-1"', href='/page-1'),
    html.Br(),
    dcc.Link('Navigate to "/page-2"', href='/page-2'),
])

EXPERIS_LOGO = "http://health5g.eu/wp-content/uploads/2019/09/Experis-IT.png"
ctrl = Controller()
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=EXPERIS_LOGO, height="60px"), style={"margin-right": "5px"}),
                        dbc.Col(dbc.NavbarBrand("Recommendation Engine", className="ms-2",
                                                style={"color": "#4C5154", "font-size": "30px"}),
                                style={"margin-left": "5px"}),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=True,
)

uploader = dbc.Row(

    dbc.Col([


        dcc.Upload(
            id="upload-resume",
            children=html.Div(
                ["Drag and drop or click to select a resumes to upload.",

                 ],

            ),
            style={
                "width": "50%",
                "height": "60px",
                "line-height": "60px",
                "border-width": "1px",
                "border-style": "line",
                "border-radius": "10px",
                "text-align": "center",

                "background-color": "#0D6EFD",
                "color":"white",
                "margin-left": "25%",
                "margin-right": "25%",
                "margin-top": "10px",
                "margin-bottom": "10px"

            },
            multiple=True,disabled =False
        ),

        html.Div(id='output-upload'),
        html.Br(),

        dcc.Loading(id="loading-resume", children=[html.Div(id="output-resume")], type="default"),
        dbc.RadioItems(id='radio_items'),
        html.Div([

            dbc.Button(id="collapse-button"),

            dbc.Collapse(
                id="resume-collapse",

            ),

            dbc.Button("Get Jobs raccomandations", style={"text-align": "center"}, id="recommendation-btn",disabled=False,
                       n_clicks=0),
            html.Br(),
            # dcc.Input(id="input1", type="text", placeholder="write file name for saving results", style={'marginRight':'15px'}),
            html.Div(id="out-all-types"),
            dbc.Button("set folder ", style={"text-align": "center"}, id="open_directory",
                       n_clicks=0),
            html.Div(id='selected_directory'),

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("ATTENTION")),
                    dbc.ModalBody("Select folder!"),

                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close1", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                is_open=False,
            ),

        ], style={"display": "none"})

    ],
        width={"size": 10, "offset": 1}),

)
jobs_recommended = dcc.Loading(id="loading-recommendations",
                               children=[html.Div(id="recommendations")], type="default")

layout_page_1 = html.Div([
    dbc.Card(
        [

            dbc.CardBody(

                dbc.Row(
                    [
                        dbc.Col(
                            html.H1(
                                html.B("Servizio non disponibile"),
                                className="text-center mt-4 mb-5",
                                style={"color": "Purple", "text-decoration": "None", },
                            )
                        )
                    ]
                ),
            ),
        ],

        style={"height": "100%"},
    )
])

layout_page_2 = html.Div([
    navbar, uploader, html.Br(), jobs_recommended,

])

# app.layout = html.Div([navbar, uploader, html.Br(), jobs_recommended])
# "complete" layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    import json
    with open(os.path.join(os.getcwd(), "json", 'json_data_info.json')) as json_file:
        data = eval(json.load(json_file))
        stato = data['Stato']
        print(stato)
        data['stato_core'] = 'IDLE'

        json_string = json.dumps(data)

        # Directly from dictionary
        with open(os.path.join(os.getcwd(), "json", 'json_data_info.json'), 'w') as outfile:
            json.dump(json_string, outfile)

    if stato.strip().lower() == 'run':
        return layout_page_2
    elif stato.strip().lower() == 'stop':
        return layout_page_1
    else:
        return layout_index


# Page 1 callbacks
@app.callback(Output('output-state', 'children'),
              Input('submit-button', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    return f'The Button has been pressed {n_clicks} times. \
            Input 1 is {input1} and Input 2 is {input2}'


# Page 2 callbacks
@app.callback(Output('page-2-display-value', 'children'),
              Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'


@app.callback(
    Output('output-upload', 'children'),
            Output("upload-resume", "disabled")
            ,
    inputs=[Input('upload-resume', 'contents'),
            State('upload-resume', 'filename')]
)
def selct_pdf(list_of_contents, list_of_names):
    if list_of_contents is not None:
        content_type, content_string = list_of_contents[0].split(',')
        # ctrl.set_filename (list_of_names)

        dizlist = {}
        for contents, filename in zip(list_of_contents, list_of_names):
            content_type, content_string = contents.split(',')

            dizlist[filename] = contents

            if 'pdf' in content_type:
                decoded_resume = base64.b64decode(content_string)
                global name

                resume_uploaded = os.path.join(os.getcwd(), filename)

            with open(resume_uploaded, "wb") as resume:
                resume.write(decoded_resume)
        ctrl.set_contents(dizlist)
        children = dbc.Card([

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("ATTENTION")),
                    dbc.ModalBody("No folder selected!"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close1", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                is_open=False,
            ),

            dbc.Row(
                [
                    dbc.Col(

                        dbc.Card(
                            [
                                dbc.CardHeader("Resumes"),
                                dbc.CardBody([
                                    html.Div([


                                        dbc.RadioItems(id='radio_items', options=[{
                                            'label': v,
                                            'value': v
                                        } for v in list_of_names], value=list_of_names[0], inline=True
                                                       , style={"margin-right": "20px"}),  #
                                        html.Br(),
                                    ]),

                                ]
                                )

                            ], color="light", style={"width": "100%","height":"100%"}),


                        width={"size": 5},




                    ),
                    dbc.Col( align="center",  width={"size": 2},),
                    dbc.Col(

                        dbc.Card(
                            [
                                dbc.CardHeader("Destination folder results"),
                                dbc.CardBody([
                                    html.Div([
                                        dbc.Button('Select the directory to store the results', id="open_directory",
                                                   n_clicks=0,
                                                   style={"text-align": "center"},disabled=False,
                                                   # color="link",
                                                   ),
                                        html.Br(),

                                        html.Div(id='selected_directory', children='No directory selected!'),
                                        html.Div(id="out-all-types"),
                                    ]),

                                ]
                                )

                            ], color="light", style={"width": "100%","height":"100%"}),
                        width={"size": 5},




                    ),

                ],
                className="g-0",

            ),

            html.Br(),

            dbc.Row(
                [
                    dbc.Col(html.Div(), md=4),
                    dbc.Col(html.Div(
                        html.Div(
                        dbc.Button("Search", color="success", style={"text-align": "center","margin-bottom": "10px"},
                                   id="recommendationbtn", disabled=False,
                                   n_clicks=0),

                        #
                        #

                                 style={"text-align": "center", "margin-bottom": "10px"},
                                 id="recommendation-btn", n_clicks=0)
                    ), md=4),
                    dbc.Col(html.Div(), md=4),

                ]
            ),


            ],
            style={"width": "100%", "margin-left": "10px","margin-bottom": "10px" ,"margin-top": "10px", 'margin-bottom': '10px', "padding": "10px"}, color="light")

        return [children,True]
    else:
        return [html.Div(),False]

#

@app.callback(output=Output('output-resume', 'children'),
              inputs=[
                  Input('radio_items', 'value'), ])
def update_items(value):
    if value is not None:
        ctrl.folder = None
        diz = ctrl.get_contents()
        content_string = diz[value]
        resume_card = dbc.Card([
            dbc.CardHeader(
                html.Div([value, dbc.Button(
                    "Show/Hide",
                    id="collapse-button",
                    className="mb-3",
                    color="info",
                    n_clicks=0,
                ), ], className="d-flex w-100 justify-content-between")

            ),

            dbc.Collapse(

                dbc.CardBody(
                    [

                        html.ObjectEl(data=content_string,
                                      type='application/pdf',
                                      width="100%", height="1000px"
                                      )
                    ]
                ),

                id="resume-collapse",
                is_open=True,
            )

        ],
            style={"width": "100%", "margin-left": "10px"}, color="light")
        return resume_card
    else:
        return html.Div()


@app.callback(
    output=Output("resume-collapse", "is_open"),
    inputs=
    [Input("collapse-button", "n_clicks"), State("resume-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("out-all-types", "children"),
    inputs=[
        Input("input1", "value")]
)
def set_namesresults(input1):
    ctrl.set_filenameresult(input1)
    return html.Div()


@app.callback(

    Output(component_id='selected_directory', component_property='children'),
     Output('open_directory','disabled'),
    inputs=[Input(component_id='open_directory', component_property='n_clicks'),
            ]
)
def set_folder(n):
    if n:

        import tkinter
        from tkinter import filedialog

        root = tkinter.Tk()
        # root.withdraw()

        directory = filedialog.askdirectory()

        # root.mainloop()
        root.destroy()

        ctrl.folder = directory

        container = html.Div([ html.Br(),html.H5("Folder selected:" +directory, className="me-1")], style={"margin-bottom": "5px"})
       # html.Span(directory)], style = {"margin-bottom": "5px"})

        # return html.H5("Folder selected: " + directory,
        #              style={'width': '50%', 'display': 'inline-block', \
        #                      'text-align': 'left'}),
        return [container,True]
    else:
        return [html.Div(),False]


@app.callback(

    Output("recommendations", "children"), Output("modal", "is_open"), Output("recommendationbtn", "disabled"),
    inputs=[Input("recommendation-btn", "n_clicks"), Input("close1", "n_clicks"), State("modal", "is_open")],

)
def get_skilss(n, n2, is_open):
    directory = ctrl.folder
    print(directory)
    if (n or n2) and directory is None:
        return html.Div(), not is_open, False

    if n and directory is not None:

        files = list(ctrl.get_contents().keys())

        global skillsner, category
        today = date.today()

        d1 = today.strftime("%d-%m-%Y")
        namer = ctrl.get_filenameresult()

        cards = []
        for pdfnamepath in files:
            name = pdfnamepath.replace("pdf", ' ')
            folder = directory.split('/') + ['skills_' + namer + "_" + name + "_" + str(d1) + '.xlsx']

            folder[0] = folder[0] + '/'

            path = os.path.join(*folder)

            rs = predict.main(pdfnamepath, path)

            rs['N°'] = pd.Series(np.arange(1, rs.shape[0]+1), index=rs.index)
            rs['Composite Score'] = rs['scoreFinal'].astype('float').round(2).apply(lambda x: int(x*100)).astype('str').map("{}%".format)
            rs['TimeScore'] = rs['scoreTime'].astype('float').round(2).apply(lambda x: int(x*100)).astype('str').map("{}%".format)
            rs['DomainScore'] = rs['scoreDom'].astype('float').round(2).apply(lambda x: int(x*100)).astype('str').map("{}%".format)
            rs['SkillsScore'] = rs['scoreSkills'].astype('float').round(2).apply(lambda x: int(x*100)).astype('str').map("{}%".format)
            rs['Post'] = rs['jobDescription'].apply(lambda x: x[:200]).map("{}...".format)
            rs['scorCompany'] = rs['scorCompany'].astype('float').round(2).apply(lambda x: int(x * 100)).astype(
                'str').map("{}%".format)

            rs.reset_index(inplace=True)

           # print(rs['company user'].values.tolist())

            # (scoreTime*scoreDomain + scoreSkills)/2

            subset_rs = rs[['N°','job user', 'company user', 'Composite Score', 'TimeScore',\
                            'DomainScore', 'SkillsScore', "scorCompany",'namescoe','jobTitle', 'jobCompany', 'Post','Apply']]
            subset_rs.rename(columns={'job user': 'Candidate job title', 'jobCompany': 'Company post', 'company user': 'Candidate company', \
                                      'jobTitle': 'Post job title','scorCompany':'CompanyScore','namescoe':'TypeCompany'}, inplace=True)

            os.remove(pdfnamepath)


            card = dbc.Card(
                [

                    dbc.CardBody([
                        dash_table.DataTable(
                            subset_rs.to_dict('records'),
                            [{"name": i, "id": i} for i in subset_rs.columns],
                            # style header
                            style_header={'backgroundColor': 'rgba(60, 90, 162, .25)',
                                          'fontWeight': 'bold', "border": "1px solid gray"},
                            style_table={'overflowX': 'scroll'},
                            style_data={'border': '1px solid gray'},

                            style_cell={


                                'minWidth': '120px', 'width': '150px', 'maxWidth': '180px',

                                'textOverflow': 'ellipsis',
                            },
                            style_data_conditional=[

                                {
                                    'if': {
                                        'column_id': 'Apply',
                                    },
                                    'backgroundColor': '#98FB98',
                                    'color': 'red','fontWeight': 'bold'
                                }]
                        )

                        # dbc.Table.from_dataframe(
                        #
                        #     subset_rs, striped=True, bordered=False, hover=True, index=False,
                        #     color='light',
                        #     size='sm'
                        #
                        #
                        # )

                    ]
                    )

                ], color="light", style={"width": "100%"})

            cards.append(html.Div([dbc.Row(dbc.Col(card, width={"size": 12})), html.Br()], style={"margin-left": "10px", "margin-right": "10px"}))

        return [cards, False,True]
    return[ html.Div(), False,False]


if __name__ == "__main__":
    # app.run_server(debug=True, port=8052)
    # app.run_server(port=8085)
    ctrl.folder = None
    print("Running the app...")
    serve(app.server, host="0.0.0.0", port=8083)
