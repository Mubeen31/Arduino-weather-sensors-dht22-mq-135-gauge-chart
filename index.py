import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from google.oauth2 import service_account
import pandas_gbq as pd1
import plotly.graph_objs as go

app = dash.Dash(__name__, )
server = app.server

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 4000,
                 n_intervals=0),

    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('sensor.png'),
                     style={'height': '30px'},
                     className='title_image'
                     ),
            html.Div('ARDUINO WEATHER SENSORS',
                     className='title_text')
        ], className='title_row')
    ], className='bg_title'),

    html.Div([
        html.Div([

            html.Div([
                html.Div([
                    dcc.Graph(id='gauge_chart1',
                              config={'displayModeBar': False},
                              className='temperature_gauge'),
                    html.Div(id='value1')
                ], className='chart_value'),

                html.Div([
                    dcc.Graph(id='gauge_chart2',
                              config={'displayModeBar': False},
                              className='temperature_gauge'),
                    html.Div(id='value2')
                ], className='chart_value')
            ], className='gauge_chart_column')

        ], className='gauge_chart'),

        html.Div([
            html.Div([
                dcc.Graph(id='line_chart1',
                          config={'displayModeBar': False},
                          className='line_chart_layout'),
                dcc.Graph(id='line_chart2',
                          config={'displayModeBar': False},
                          className='line_chart_layout'),
            ], className='line_chart_column')
        ], className='line_chart')
    ], className='chart_row')
])


@app.callback(Output('gauge_chart1', 'figure'),
              [Input('update_value', 'n_intervals')])
def update_confirmed(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     OutsideTemperature
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_temp = df['OutsideTemperature'].head(1).iloc[0]

    return {
        'data': [go.Indicator(
            mode='gauge',
            value=get_temp,
            title={'text': 'Temperature'},
            gauge={'axis': {'range': [None, 15], 'visible': False},

                   'bar': {'color': '#1EEC11', 'thickness': 1},

                   'steps': [{'range': [0, 20], 'color': 'gray'}],

                   'threshold': {'line': {'color': 'white', 'width': 4},
                                 'thickness': 1, 'value': get_temp}
                   }
        )],
        'layout': go.Layout(
            title={'text': '',
                   'y': 0.8,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'
                   },
            font=dict(color='white',
                      family="sans-serif",
                      size=12),
            paper_bgcolor='rgba(255, 255, 255, 0)',
            plot_bgcolor='rgba(255, 255, 255, 0)'
        ),
    }


@app.callback(Output('value1', 'children'),
              [Input('update_value', 'n_intervals')])
def update_confirmed(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     OutsideTemperature
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_temp = df['OutsideTemperature'].head(1).iloc[0]

    return [
        html.Div('{0:.1f} °C'.format(get_temp),
                 className='gauge_value')
    ]


@app.callback(Output('gauge_chart2', 'figure'),
              [Input('update_value', 'n_intervals')])
def update_confirmed(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     OutsideHumidity
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_hum = df['OutsideHumidity'].head(1).iloc[0]

    return {
        'data': [go.Indicator(
            mode='gauge',
            value=get_hum,
            title={'text': 'Humidity'},
            gauge={'axis': {'range': [None, 100], 'visible': False},

                   'bar': {'color': '#DFFF00', 'thickness': 1},

                   'steps': [{'range': [0, 100], 'color': 'gray'}],

                   'threshold': {'line': {'color': 'white', 'width': 4},
                                 'thickness': 1, 'value': get_hum}
                   }
        )],
        'layout': go.Layout(
            title={'text': '',
                   'y': 0.8,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'
                   },
            font=dict(color='white',
                      family="sans-serif",
                      size=12),
            paper_bgcolor='rgba(255, 255, 255, 0)',
            plot_bgcolor='rgba(255, 255, 255, 0)'
        ),
    }


@app.callback(Output('value2', 'children'),
              [Input('update_value', 'n_intervals')])
def update_confirmed(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     OutsideHumidity
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 1
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
        get_hum = df['OutsideHumidity'].head(1).iloc[0]

    return [
        html.Div('{0:.1f} %'.format(get_hum),
                 className='gauge_value')
    ]


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value', 'n_intervals')])
def line_chart_values(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     DateTime,
                     OutsideTemperature
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 15
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)

    return {
        'data': [go.Scatter(
            x=df['DateTime'].head(15),
            y=df['OutsideTemperature'].head(15),
            mode='markers+lines',
            line=dict(width=3, color='#1EEC11'),
            marker=dict(size=7, symbol='circle', color='#1EEC11',
                        line=dict(color='#1EEC11', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df['DateTime'].head(15).astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in df['OutsideTemperature'].head(15)] + '<br>'
        )],

        'layout': go.Layout(
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={
                'text': '<b>Temperature (°C)</b>',
                'y': 0.90,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#ffbf00',
                'size': 17},
            margin=dict(t=50, r=10),
            xaxis=dict(
                       title='<b>Hours</b>',
                       color='#ffffff',
                       showline=True,
                       showgrid=True,
                       linecolor='#ffffff',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#ffffff')

                       ),

            yaxis=dict(range=[min(df['OutsideTemperature'].head(15)) - 0.05, max(df['OutsideTemperature'].head(15)) + 0.05],
                       title='<b>Temperature (°C)</b>',
                       color='#ffffff',
                       zeroline=False,
                       showline=True,
                       showgrid=True,
                       linecolor='#ffffff',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#ffffff')

                       ),
            font=dict(
                family="sans-serif",
                size=12,
                color='#ffffff')

        )

    }


@app.callback(Output('line_chart2', 'figure'),
              [Input('update_value', 'n_intervals')])
def line_chart_values(n_intervals):
    if n_intervals == 0:
        raise PreventUpdate
    else:
        credentials = service_account.Credentials.from_service_account_file('weatherdata1.json')
        project_id = 'weatherdata1'
        df_sql = f"""SELECT
                     DateTime,
                     OutsideHumidity
                     FROM
                     `weatherdata1.WeatherSensorsData1.SensorsData1`
                     ORDER BY
                     DateTime DESC LIMIT 15
                     """
        df = pd1.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)

    return {
        'data': [go.Scatter(
            x=df['DateTime'].head(15),
            y=df['OutsideHumidity'].head(15),
            mode='markers+lines',
            line=dict(width=3, color='#DFFF00'),
            marker=dict(size=7, symbol='circle', color='#DFFF00',
                        line=dict(color='#DFFF00', width=2)
                        ),
            hoverinfo='text',
            hovertext=
            '<b>Date Time</b>: ' + df['DateTime'].head(15).astype(str) + '<br>' +
            '<b>Temperature (°C)</b>: ' + [f'{x:,.2f} °C' for x in df['OutsideHumidity'].head(15)] + '<br>'
        )],

        'layout': go.Layout(
            plot_bgcolor='rgba(255, 255, 255, 0)',
            paper_bgcolor='rgba(255, 255, 255, 0)',
            title={
                'text': '<b>Humidity (%)</b>',
                'y': 0.90,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': '#ffbf00',
                'size': 17},
            margin=dict(t=50, r=10),
            xaxis=dict(
                       title='<b>Hours</b>',
                       color='#ffffff',
                       showline=True,
                       showgrid=True,
                       linecolor='#ffffff',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#ffffff')

                       ),

            yaxis=dict(range=[min(df['OutsideHumidity'].head(15)) - 0.05, max(df['OutsideHumidity'].head(15)) + 0.05],
                       title='<b>Humidity (%)</b>',
                       color='#ffffff',
                       zeroline=False,
                       showline=True,
                       showgrid=True,
                       linecolor='#ffffff',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#ffffff')

                       ),
            font=dict(
                family="sans-serif",
                size=12,
                color='#ffffff')

        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
