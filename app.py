import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from data_load import fetch_data
from figs import plot1, plot2, plot3
from datetime import datetime
import plotly.express as px

start_date = datetime(2022, 1, 1)
end_date = datetime.now()

commodities = {
    "Natural Gas": "NG=F",
    "Brent Oil": "BZ=F",
    "Crude Oil": "CL=F",
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F",
    "Palladium": "PA=F",
    "Platinum": "PL=F",
    "Corn": "ZC=F",
    "Soybeans": "ZS=F",
    "Wheat": "ZW=F",
    "Cotton": "CT=F",
    "Sugar": "SB=F",
    "Coffee": "KC=F",
    "Cocoa": "CC=F",
}

data_dict = fetch_data(commodities, start_date, end_date)

#df = pd.read_csv('gapminderDataFiveYear.csv')

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash_app.server


dash_app.layout = html.Div(
    [
        html.Link(rel='stylesheet', href='/static/style.css'),
        # left column
        html.Div(
            [
                html.Div(
                    [
                        html.H3('Tickers', style={'font-weight': 'bold', 'color': 'white'}),
                        html.Ul(
                            [
                                html.Li(
                                    html.A(key, href='#', id=f'ticker-{value}', className='ticker-link'),
                                    style={'padding': '5px', 'margin-left': '15px'}
                                )
                                for key, value in commodities.items()
                            ],
                            id='ticker-list',
                            style={'padding': 0}
                        ),
                    ],
                    style={'margin-bottom': '20px', 'color': '#2f4554'}
                ),
                html.Div(
                    [
                        html.Label('Start Date', style={'font-weight': 'bold', 'color': 'white'}),
                        dcc.DatePickerSingle(
                            id='start-date-picker',
                            date=start_date,
                            min_date_allowed=start_date,
                            max_date_allowed=end_date,
                            display_format='YYYY-MM-DD',
                            style={'width': '100%'},
                            persistence=True,
                            persistence_type='session'
                        ),
                    ],
                    style={'margin-bottom': '20px', 'position': 'relative'}
                ),
                html.Div(
                    [
                        html.Label('End Date', style={'font-weight': 'bold', 'color': 'white'}),
                        dcc.DatePickerSingle(
                            id='end-date-picker',
                            date=end_date,
                            min_date_allowed=start_date,
                            max_date_allowed=end_date,
                            display_format='YYYY-MM-DD',
                            style={'width': '100%'},
                            persistence=True,
                            persistence_type='session'
                        ),
                    ],
                    style={'margin-bottom': '20px', 'position': 'relative'}
                ),
            ],
            className='left-column',
            style={'width': '15%', 'background-color': '#2f4554', 'padding': '15px',
                   'border': '1px solid #c0c0c0', 'border-radius': '25px',
                   'margin': '20px'}
        ),

        # right column
        html.Div(
            [
                dcc.Dropdown(
                    id='ticker-dropdown',
                    options=[{'label': value, 'value': value} for key, value in commodities.items()],

                    clearable=False,
                    style={'display': 'none'}
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id='plot-1',
                            config={'displayModeBar': False},
                            style={'width': '49%', 'display': 'inline-block',
                                   'border': '1px solid #c0c0c0', 'border-radius': '25px', 'overflow': 'hidden', 'margin-right': '2%'}
                        ),
                        dcc.Graph(id='plot-2',
                                  style={'width': '49%', 'display': 'inline-block',
                                         'border': '1px solid #c0c0c0', 'border-radius': '25px', 'overflow': 'hidden'}
                                  ),
                    ],
                    style={'width': '100%'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='plot-3',
                                  style={'width': '50%', 'display': 'inline-block',
                                         'border': '1px solid #c0c0c0', 'border-radius': '25px', 'overflow': 'hidden',
                                         'margin-right': '0%'}
                                  ),
                        html.Div(
                            id='plot-4',
                            style={'width': '50%', 'display': 'inline-block',
                                   'border-radius': '25px', 'margin': '20px'}
                        ),
                    ],
                    style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%',
                           'align-items': 'flex-start'}
                ),
                html.Footer(
                    [
                        html.P(
                            "Disclaimer: The data provided in this application is for informational purposes only. " \
                            "Please note that the data sources used are subject to their respective terms and conditions. " \
                            "The data for this application is fetching from Yahoo Finance using the yfinance library."
                        ),
                    ],
                    style={'margin': '20px', 'text-align': 'left'}
                )

            ],
            className='right-column',
            style={'width': '80%', 'padding': '15px'}
        ),

    ],
    style={'display': 'flex', 'background-color': 'white', 'color': 'black'}
)


@dash_app.callback(
    Output('ticker-dropdown', 'value'),
    [Input(f'ticker-{value}', 'n_clicks') for key, value in commodities.items()],
    [State('ticker-dropdown', 'value')]
)
def update_ticker(value, *args):
    ctx = dash.callback_context
    triggered_element = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_element:
        ticker = triggered_element.split('-')[1]
        return ticker
    return value


@dash_app.callback(
    [Output('plot-1', 'figure'),
     Output('plot-2', 'figure'),
     Output('plot-3', 'figure'),
     Output('plot-4', 'children')],
    [Input('ticker-dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_plots(ticker, start_date, end_date):
    if ticker is None:
        ticker = 'NG=F'
    #print(ticker, start_date, end_date)

    filtered_df = data_dict[ticker][
        (data_dict[ticker]['Date'] >= start_date) & (data_dict[ticker]['Date'] <= end_date)]
    ticker_name = list(commodities.keys())[list(commodities.values()).index(ticker)]
    fig1 = plot1(filtered_df, ticker_name)
    fig2 = plot2(filtered_df, ticker_name)
    fig3 = plot3(data_dict, commodities, start_date, end_date)

    frame1_color = '#2f4554' #if ticker == 'NG=F' else '#ced4da'
    frame2_color = '#2a9d8f' #if ticker == 'BZ=F' else '#ced4da'
    frame3_color = '#e9c46a' #if ticker == 'CL=F' else '#ced4da'
    frame4_color = '#f4a261' #if ticker == 'GC=F' else '#ced4da'


    current_price = "{:.4f}".format(filtered_df['Close'].iloc[-1])
    today_volume = "{:.2f}".format(filtered_df['Volume'].iloc[-1])
    week_volume = "{:.2f}".format(filtered_df['Volume'].iloc[-5:-1].sum())
    month_price = "{:.2f}".format(filtered_df['Volume'].iloc[-20:-1].sum())

    frame1_text = html.H4(['Current price', html.Br(), current_price], style={'color': 'white'})
    frame2_text = html.H4(["Today's volume", html.Br(), today_volume], style={'color': 'white'})
    frame3_text = html.H4(['Last week volume', html.Br(), week_volume], style={'color': 'white'})
    frame4_text = html.H4(['Last month volume', html.Br(), month_price], style={'color': 'white'})


    return (
        fig1,
        fig3,
        fig2,
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(frame1_text, style={'color': 'white'})
                                    ],
                                    style={'padding': '20px'}
                                )
                            ],
                            style={'width': '100%', 'background-color': frame1_color, 'border-radius': '25px', 'margin': '20px', 'text-align': 'center'}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(frame2_text, style={'color': 'white'})
                                    ],
                                    style={'padding': '20px'}
                                )
                            ],
                            style={'width': '100%', 'background-color': frame2_color, 'border-radius': '25px', 'margin': '20px', 'text-align': 'center'}
                        )
                    ],
                    style={'display': 'flex', 'flex-direction': 'column', 'width': '48%', 'align-items': 'center'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(frame3_text, style={'color': 'white'})
                                    ],
                                style={'padding': '20px'}
                                )
                            ],
                            style={'width': '100%','background-color': frame3_color, 'border-radius': '25px', 'margin': '20px', 'text-align': 'center'}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(frame4_text, style={'color': 'white'})
                                    ],
                                    style={'padding': '20px'}
                                )
                            ],
                            style={'width': '100%', 'background-color': frame4_color, 'border-radius': '25px', 'margin': '20px', 'text-align': 'center'}
                        )
                    ],
                    style={'display': 'flex', 'flex-direction': 'column', 'width': '48%'}
                )
            ],
            style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'align-items': 'center'}
        )

    )



# dash_app.layout = html.Div([
#     dcc.Graph(id='graph-with-slider'),
#     dcc.Slider(
#         id='year-slider',
#         min=df['year'].min(),
#         max=df['year'].max(),
#         value=df['year'].min(),
#         marks={str(year): str(year) for year in df['year'].unique()},
#         step=None
#     )
# ])
#
#
#
#
# @dash_app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))
#
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#
#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      size="pop", color="continent", hover_name="country",
#                      log_x=True, size_max=55, template="plotly_dark")
#
#     fig.update_layout(transition_duration=500)
#
#     return fig
#

if __name__ == '__main__':
    dash_app.run_server(debug=True)