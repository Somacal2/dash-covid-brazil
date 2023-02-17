import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis, Marker, Margin

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# ====== Importando e Tratando Dados ========= #
# df = pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")
# df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())]
# df_brasil = df[df['regiao'] == 'Brasil']

# ====== Exportando Dados Tratados ========= # obs: Após tratar e exportar, poder-se comentar os comandos anteriores e usar só os novodas df's
# df_states.to_csv("df_states.csv")
# df_brasil.to_csv("df_brasil.csv")

# ====== Lendo Apenas Dados Tratados ========= #

df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")

df_states_ = df_states[df_states["data"] == "2020-05-13"]
df_data = df_states[df_states["estado"] == "RJ"]

select_columns = {"casosAcumulado": "Casos Acumulados",
                "casosNovos": "Novos Casos",
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}

brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

# ==Analizanso dos dados== #
# type(brazil_states)
# brazil_states.keys()
# brazil_states["features"]
# type(brazil_states["features"])
# brazil_states["features"][0].keys()
# brazil_states["features"][0]["id"]
# brazil_states["features"][0]["geometry"]

# ========= App ============== #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])



# ======== Instanciando o gráfico do MAPA ========== #
fig = px.choropleth_mapbox(df_states_, locations="estado", color="casosNovos",
                            center={"lat": -16.95, "lon": -47.78}, zoom=4,
                            geojson=brazil_states, color_continuous_scale="Redor", opacity=0.4,
                            hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True,
                            "estado": True})
fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

# ======== Instanciando o gráfico de LINHAS ========== #
fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10),
)


# ======== Layout ========== #
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("somacal_logo.png"), height=70),
                html.H5("Evolução COVID-19"),
                dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ], style={}),
            html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
            html.Div(id="div-test", children=[
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=df_brasil["data"].min(),
                    max_date_allowed=df_brasil["data"].max(),
                    initial_visible_month=df_brasil["data"].min(),
                    date=df_brasil["data"].max(),
                    display_format="MMMM D, YYYY",
                    style={"border": "0px solid black"}
                )
            ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Casos recuperados"),
                        html.H5(style={"color": "#adfc92"}, id="casos-recuperaros-text"),
                        html.Span("Em acompanhamento"),
                        html.H5(id="em-acompanhamento-text"),
                    ], style={"height": "210px", "padding": "10px"})
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.9)",
                                        "color": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Casos conformados totais"),
                        html.H5(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                        html.Span("Novos cados na data"),
                        html.H5(id="novos-casos-text"),
                    ], style={"height": "210px", "padding": "10px"})
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.9)",
                                        "color": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Óbitos confirmados"),
                        html.H5(style={"color": "#df2935"}, id="obitos-text"),
                        html.Span("Óbitos na data"),
                        html.H5(id="obitos-na-data-text"),
                    ], style={"height": "210px", "padding": "10px"})
                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.9)",
                                        "color": "#FFFFFF"})
            ], md=4),
        ]),
            html.Div([
                html.P("Selecione o tipo de dado que deseja visualizar:", style={"margin-top": "25px"}),
                dcc.Dropdown(id="location-dropdown",
                            options=[{"label": j, "value": i} for i, j in select_columns.items()],
                            value="casosNovos",
                            style={"margin-top": "10px"}
                            ),
                dcc.Graph(id="line-graph", figure=fig2)
            ]),
        ], md=5, style={"padding": "20px", "background-color": "#242424"}),

        dbc.Col([
            dcc.Loading(id="loading-1", type="default",
                children=[dcc.Graph(id="choropleth-map", figure=fig, style={"height": "100vh", "margin-right": "10px"})
                ]
            )
        ], md=7)
    ], className="g-0")
, fluid=True)


# ===== Callbacks ===== #
@app.callback(
    [
        Output("casos-recuperaros-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ],
    [
        Input("date-picker", "date"),
        Input("location-button", "children")
    ]
)
#aqui dentro dos parênteses coloca-se os inputs. No return deve-se inforar os outputs
def display_status(date, location):
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"]==date]
    else:
        df_data_on_date = df_states[(df_states["estado"]== location) & (df_states["data"] == date)]

    df_data_on_date["Recuperadosnovos"]
    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",","."),
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0] else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",","."),
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",","."),
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",","."),
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",","."),
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",","."),

    return (recuperados_novos,
            acompanhamentos_novos,
            casos_acumulados,
            casos_novos,
            obitos_acumulado,
            obitos_novos)

@app.callback(
    Output("line-graph", "figure")
    ,
    [
        Input("location-dropdown", "value"),
        Input("location-button", "children"),
    ]
)
def plot_line_graph(plot_type, location):
    if location =="BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[df_states["estado"] == location]

    bar_plots = ["casosNovos", "obitosNovos"]

    fig2 = go.Figure(layout={"template": "plotly_dark"})
    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig2

@app.callback(
    Output("choropleth-map", "figure"),
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states,
        center={"lat": CENTER_LAT, "lon": CENTER_LON},
        zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False}
    )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    
    return fig

@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    change_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and change_id != "location-button.n_clicks":
        state=click_data["points"][0]["location"]
        return "{}".format(state)
    else:
        return "BRASIL"


# ====== Run server ===== #
if __name__ == '__main__':
    app.run_server(debug=True) #port=8080, host="0.0.0.0")