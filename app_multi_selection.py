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




server = flask.Flask(__name__)

app = dash.Dash(
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    # serve_locally=False,
)

# url_bar_and_content_div = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])



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
                ["Trascina e rilascia o clicca per caricare un curriculum",

                 ],       id="upload", n_clicks=0,

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
                "color": "white",
                "margin-left": "25%",
                "margin-right": "25%",
                "margin-top": "10px",
                "margin-bottom": "10px"

            },
            multiple=True, disabled =False
        ),



        html.Div(id='output-upload'),
        html.Br(),

        dcc.Loading(id="loading-resume", children=[html.Div(id="output-resume")], type="default"),
        dbc.RadioItems(id='radio_items'),


    ],
        width={"size": 10, "offset": 1}),

)
jobs_recommended = dcc.Loading(id="loading-recommendations",
                               children=[html.Div(id="recommendations"),html.Div(id="refresh")], type="default")


# layout_page_1 = html.Div([
#     dbc.Card(
#         [
#
#             dbc.CardBody(
#
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             html.H1(
#                                 html.B("Servizio non disponibile"),
#                                 className="text-center mt-4 mb-5",
#                                 style={"color": "Purple", "text-decoration": "None", },
#                             )
#                         )
#                     ]
#                 ),
#             ),
#         ],
#
#         style={"height": "100%"},
#     )
# ])

layout_page_2 = html.Div([
    uploader, html.Br(), jobs_recommended,

])


app.layout = html.Div([

    # dcc.Location(id='url', refresh=False),
    # html.Div(id='page-content')

dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [


                                dbc.Col(html.Img(src=EXPERIS_LOGO, height="60px"), style={"margin-right": "5px"}),
                                dbc.Col(dbc.NavbarBrand("Recommendation Engine", className="ms-2",
                                                        style={"color": "#4C5154", "font-size": "30px"}),width=8
                                        ),
                                # dbc.Col(html.A(html.Button('Refresh Page',
                                #                            style={'margin-bottom': '10px',
                                #                                   "fontSize": "1em",
                                #                                   "background-color": "white", "color": "black",
                                #                                   "border-radius": "10px",
                                #                                   "border": "2px solid dodgerblue"}),
                                #                href=relative_pathname),align="end",
                                #         ),


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
        ),
        layout_page_2,


])


# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def display_page(relative_pathname):
#     return html.Div([
#
#         dbc.Navbar(
#             dbc.Container(
#                 [
#                     html.A(
#                         dbc.Row(
#                             [
#
#
#                                 dbc.Col(html.Img(src=EXPERIS_LOGO, height="60px"), style={"margin-right": "5px"}),
#                                 dbc.Col(dbc.NavbarBrand("Recommendation Engine", className="ms-2",
#                                                         style={"color": "#4C5154", "font-size": "30px"}),width=8
#                                         ),
#                                 # dbc.Col(html.A(html.Button('Refresh Page',
#                                 #                            style={'margin-bottom': '10px',
#                                 #                                   "fontSize": "1em",
#                                 #                                   "background-color": "white", "color": "black",
#                                 #                                   "border-radius": "10px",
#                                 #                                   "border": "2px solid dodgerblue"}),
#                                 #                href=relative_pathname),align="end",
#                                 #         ),
#
#
#                             ],
#                             align="center",
#                             className="g-0",
#                         ),
#                         style={"textDecoration": "none"},
#                     ),
#                     dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
#                     dbc.Collapse(
#                         id="navbar-collapse",
#                         is_open=False,
#                         navbar=True,
#                     ),
#                 ]
#             ),
#             color="light",
#             dark=True,
#         ),
#         layout_page_2,
#
#
#     ])


@app.callback(
            Output('output-upload', 'children'),
            Output("upload-resume", "disabled"),
            Output("upload-resume", "style"),
    inputs= [Input('upload-resume', 'contents'),
            State('upload-resume', 'filename')]
)
def select_pdf(list_of_contents, list_of_names):
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
                    dbc.ModalHeader(dbc.ModalTitle("Attenzione"), style={"color": "white", "background-color": "#f0833c"}),
                    dbc.ModalBody("Non hai selezionato la cartella per il salvataggio dei risultati!"),
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
                                dbc.CardHeader("Curriculum da processare", style={"color":"white", "background-color": "#f0833c", "font-weight": "bold"}),
                                dbc.CardBody([
                                    html.Div([


                                        dbc.RadioItems(id='radio_items', options=[{
                                            'label': v,
                                            'value': v
                                        } for v in list_of_names], value=list_of_names[0], inline=True
                                                       , style={"margin-right": "20px", "font-weight": "bold", "font-size":"20px", "color": "dimgray"}),
                                        html.Br(),
                                    ]),

                                ]
                                )

                            ], color="light", style={"width": "100%","height":"100%"}),


                        width={"size": 6},




                    ),
                    # dbc.Col( align="center",  width={"size": 2},),
                    dbc.Col(

                        dbc.Card(
                            [
                                dbc.CardHeader("Salvataggio dei risultati",  style={"color":"white", "background-color": "#779788", "font-weight": "bold"}),
                                dbc.CardBody([
                                    html.Div([
                                        html.Div([
                                            dbc.Button('Salva i risultati in ...', id="open_directory",
                                                       n_clicks=0,
                                                       style={"text-align": "center"}, disabled=False,

                                                       # color="link",
                                                       ),
                                        ], className="d-grid gap-2"),

                                        html.Div(id='selected_directory', children='No directory selected!', style={"margin-top":"5px", "margin-bottom":"2px", "text-align": "center"}),
                                        html.Div(id="out-all-types"),
                                    ]),

                                ]
                                )

                            ], color="light", style={"width": "100%","height":"100%"}),
                        width={"size": 6},




                    ),

                ],


            ),

            html.Hr(style={"border-top": "1px dashed gray"}),

            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            html.Div(
                                html.Div(
                                    dbc.Button(html.Span([html.I(className="bi bi-search me-2"), "Analizza"]),
                                               color="primary", style={"text-align": "center", "font-weight": "bold",
                                                                       "font-size": "25px"},
                                               id="recommendationbtn", disabled=False,
                                               n_clicks=0),

                                    style={"text-align": "center", "margin-bottom": "10px"},
                                    id="recommendation-btn", n_clicks=0, className="d-grid gap-2")
                            ),

                            html.A(


                            html.Div(
                                html.Div(

                                    dbc.Button(html.Span([html.I(className="bi bi-arrow-clockwise me-2"), "Nuove analisi"]),
                                               color="danger", style={"text-align": "center", "font-weight": "bold",
                                                                       "font-size": "25px"},
                                               id="cleanbtn", disabled=False,
                                               n_clicks=0),

                                    style={"text-align": "center", "margin-bottom": "10px"},
                                    id="clean-btn", n_clicks=0, className="d-grid gap-2")
                            ), href='/', style={"text-decoration": "none"}
                            ),


                        ],



                        width={"size": 4, "offset": 4}),
                    # dbc.Col(html.Div(), md=4),

                ]
            ),


            ],
            style={"width": "100%", "margin-left": "10px", "margin-bottom": "10px", "margin-top": "10px", "padding": "10px"}, color="light")

        return [children, True, {
                "width": "50%",
                "height": "60px",
                "line-height": "60px",
                "border-width": "1px",
                "border-style": "line",
                "border-radius": "10px",
                "text-align": "center",

                "background-color": "#6c757d",
                "color": "white",
                "margin-left": "25%",
                "margin-right": "25%",
                "margin-top": "10px",
                "margin-bottom": "10px"

            }]
    else:
        return [html.Div(), False,  {
                "width": "50%",
                "height": "60px",
                "line-height": "60px",
                "border-width": "1px",
                "border-style": "line",
                "border-radius": "10px",
                "text-align": "center",

                "background-color": "#0D6EFD",
                "color": "white",
                "margin-left": "25%",
                "margin-right": "25%",
                "margin-top": "10px",
                "margin-bottom": "10px"

            },]

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
                html.Div([html.Span(value, style={"font-style": "italic", "color": "#5078b4"}),

                    dbc.Button(
                    "Mostra/Nascondi",
                    id="collapse-button",
                    className="mb-3",
                    color="info",
                    n_clicks=0,
                    style={"color": "white", "font-weight": "bold"}
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

        folder_container = html.Span(directory, style={"font-weight": "bold", "font-size":"20px", "color": "dimgray"}),


        return [folder_container, True]
    else:
        return [html.Div(), False]




@app.callback(
    Output("recommendationbtn", "disabled"),
    inputs=[Input("recommendationbtn", "n_clicks")]
)


def search(n_clicks):
    directory = ctrl.folder
    if n_clicks and directory :
        return True


@app.callback(
    Output("recommendations", "children"), Output("modal", "is_open"),
    inputs=[Input("recommendation-btn", "n_clicks"), Input("close1", "n_clicks"), State("modal", "is_open")],
)
def get_skilss(n, n2, is_open):
    directory = ctrl.folder
    print(directory)
    if (n or n2) and directory is None:
        return html.Div(), not is_open

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
            rs.sort_values(by=['scoreFinal'], ascending=False, inplace=True)

            # rs['N°'] = pd.Series(np.arange(1, rs.shape[0]+1), index=rs.index)
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
            # N°'
            subset_rs = rs[['job user', 'company user', 'namescoe','Composite Score', 'TimeScore',\
                            'DomainScore', 'SkillsScore', "scorCompany",'jobTitle', 'jobCompany', 'Post', 'Apply']]
            subset_rs.rename(columns={'job user': 'Candidate job title', 'jobCompany': 'Company post', 'company user': 'Candidate company', \
                                      'jobTitle': 'Post job title','scorCompany':'CompanyScore','namescoe':'Company type'}, inplace=True)



            os.remove(pdfnamepath)


            card = dbc.Card(
                [

                    dbc.CardBody([
                        dash_table.DataTable(
                            data=
                            subset_rs.to_dict('records'),
                            columns=
                            [{"name": i, "id": i} for i in subset_rs.columns],
                            tooltip_header={i: i for i in subset_rs.columns},
                            tooltip_data=[
                                {
                                    column: {'value': str(value), 'type': 'markdown'}
                                    for column, value in row.items()
                                } for row in subset_rs.to_dict('records')
                            ],
                            css=[{
                                'selector': '.dash-table-tooltip',
                                'rule': 'background-color: grey; font-family: monospace; color: white',

                            }],


                            # ,fill_width=False,
                            style_header={
                                'fontSize': 17,
                                # 'textDecoration': 'underline',
                                'fontWeight': "bold",
                                'backgroundColor': "#5078b4",
                                "color": "white",
                                "fontFamily": "Arial,Helvetica Neue,Helvetica,sans-serif"

                            },

                            # Overflow into ellipsis

                            style_cell={
                                'overflow': 'hidden', 'fontSize': 15,
                                'textOverflow': 'ellipsis', "width": "50%", 'maxWidth': 100,
                                "fontFamily": "Arial,Helvetica Neue,Helvetica,sans-serif"

                            },

                            tooltip_delay=0,
                            tooltip_duration=None,

                            style_data_conditional=[

                                {
                                    'if': {
                                        'column_id': 'Apply',
                                    },
                                    'backgroundColor': '#98FB98',
                                    'color': 'red', 'fontWeight': 'bold'
                                },


                            ],

                            style_cell_conditional = [

                                #{'if': {'column_id': 'N°'},
                                 #'width': '5%'},

                                {'if': {'column_id': 'Candidate company'},
                                 'width': '20%'},
                                {'if': {'column_id': 'Composite Score'},
                                 'width': '15%', 'font-weight': 'bold', "color": "#f0833c"},
                                {'if': {'column_id': 'Company post'},
                                 'width': '20%'},
                                {'if': {'column_id': 'TimeScore'},
                                 'font-weight': 'bold', "color": "#5078b4", "width": "15%"},
                                {'if': {'column_id': 'DomainScore'},
                                 'font-weight': 'bold', "color": "#5078b4"},
                                {'if': {'column_id': 'SkillsScore'},
                                 'font-weight': 'bold', "color": "#5078b4"},
                                {'if': {'column_id': 'CompanyScore'},
                                 'font-weight': 'bold', "color": "#5078b4"},
                                {'if': {'column_id': 'Post'},
                                 'width': '30%'},
                                {'if': {'column_id': 'Candidate job title'},
                                 'width': '30%'},
                                {'if': {'column_id': 'Company type'},
                                 'width': '10%'}

                            ]
                        ),

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

        return [cards, False]
    return[html.Div(), False]


if __name__ == "__main__":
    # app.run_server(debug=True, port=8052)
    # app.run_server(port=8085)
    ctrl.folder = None
    print("Running the app...")
    serve(app.server, host="0.0.0.0", port=8083)