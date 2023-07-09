from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import math
from helpers import generate_random_data, generate_random_cluster_data, update_selected_data
import dash_bootstrap_components as dbc

# NEU: gleiche Funktionalität wie Dashboard_4 oder OHNE Inline-Styles und OHNE Bootstrap,
# dafür mit (umfangreichem) CSS -> main_dashboard4.css
# NEU Auslagerung Datengenerierung in eigene Funktion

# define cluster colors
COLORS = {'0': "red",
          '1': "blue",
          '2': "grey"}

external_stylesheets = [
    "'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'"
]

# eigenes .css aus Ordner assets wird automatisch eingebunden
app = Dash(__name__, external_stylesheets=external_stylesheets)

df = generate_random_data(seed=8)
cluster_df = generate_random_cluster_data()

app.layout = html.Div([

    html.Header([html.H1("Dashboard 5a")],
                className="header--title"),

    html.Div([

        dcc.Tabs(id="tabs", children=[

            dcc.Tab(label="Tab1", children=[

                html.Div([

                    html.Div([
                        dcc.Dropdown(options=['red', 'green', 'blue'],
                                     value='red',
                                     id='color',
                                     multi=False,
                                     className="graph_1--dropdown graph-control"),
                        dcc.Graph(id="graph_1", className="graph_1 graph")
                    ], className="graph-component"),

                    html.Div([
                        dcc.Slider(min=math.floor(df['y'].min()),
                                   max=math.ceil(df['y'].max()),
                                   id="min_value",
                                   className="graph_2--slider graph-control"),
                        dcc.Graph(id="graph_2", className="graph_2 graph")

                    ], className="graph-component")
                ], className="tab1--main-container")

            ], className="tab1"),

            dcc.Tab(label="Tab2",
                    children=[
                        html.Div([
                            html.Div(dcc.Graph(id="graph_3"), className="graph_3"),
                            html.Div(dcc.Graph(id="graph_4"), className="graph_4"),
                            html.Div(
                                html.Div([
                                    dbc.Label("Number of bins:",
                                              html_for="graph_5_nbins"),
                                    dcc.Dropdown(options=[str(i) for i in range(5, 100, 5)],
                                                 value='40',
                                                 id='graph_5_nbins',
                                                 multi=False)
                                ])
                                , className="graph_5--bins-dropdown"),
                            html.Div(
                                html.Div(
                                    [
                                        dbc.Label("Color:",
                                                  html_for="graph_5_color"),
                                        dcc.Dropdown(
                                            options=["Viridis", "Magma", "Hot", "GnBu", "Greys"],
                                            value='Hot',
                                            id='graph_5_color',
                                            multi=False)
                                    ])
                                , className="graph_5--color-dropdown"),
                            html.Div(
                                html.Div([
                                    dbc.Label("Separated for Cluster:",
                                              html_for="graph_5_separated"),
                                        dcc.RadioItems(
                                            options=["Yes", "No"],
                                            value='No',
                                            id='graph_5_separated',
                                            className="graph_5_separated")
                                ]
                                )
                                , className="graph_5--separation-radio"),
                            html.Div(dcc.Graph(id="graph_5"), className="graph_5")
                        ], className="tab2--main-container")
                    ],
                    className="tab2")
        ])

    ], className="tabs-content")

], className="container")


@app.callback(
    Output("graph_1", "figure"),
    Input("color", "value")
)
def update_graph_1(dropdown_value_color):
    fig = px.histogram(df,
                       x="y",
                       color_discrete_sequence=[dropdown_value_color])
    fig.update_layout(template="plotly_white")
    return fig


@app.callback(
    Output("graph_2", "figure"),
    Input("min_value", "value")
)
def update_graph_2(min_value):
    if min_value:
        dff = df[df['y'] > min_value]
    else:
        dff = df

    fig = px.scatter(dff, x='x', y='y')
    fig.update_layout(template="plotly_white")
    return fig


@app.callback(Output("graph_3", "figure"),
              Output("graph_4", "figure"),
              Input("graph_3", "relayoutData"))
def update_graph_3_and_4(selected_data):
    PLOT_HEIGHT = 400

    cluster_dff = update_selected_data(cluster_df=cluster_df, selected_data=selected_data)

    fig3 = px.scatter(cluster_dff,
                      x="X",
                      y="Y",
                      color="cluster",
                      color_discrete_map=COLORS,
                      category_orders={"cluster": ["0", "1", "2"]})

    fig3.update_layout(
        height=PLOT_HEIGHT,
        template="plotly_white",
        coloraxis_showscale=False)
    fig3.update_traces(marker=dict(size=8))

    group_counts = cluster_dff[['cluster', 'X']].groupby('cluster').count()

    fig4 = go.Figure(
        data=[go.Bar(
            x=group_counts.index,
            y=group_counts['X'],
            marker_color=[COLORS.get(i) for i in group_counts.index]
        )])

    fig4.update_layout(height=PLOT_HEIGHT,
                       template="plotly_white",
                       title="<b>Counts per cluster</b>",
                       xaxis_title="cluster",
                       title_font_size=25
                       )

    return fig3, fig4


@app.callback(
    Output("graph_5", "figure"),
    Input("graph_5_nbins", "value"),
    Input("graph_5_color", "value"),
    Input("graph_5_separated", "value"),
    Input("graph_3", "relayoutData"),
)
def update_graph_5(nbins, color, separated, selected_data):
    cluster_dff = update_selected_data(cluster_df=cluster_df, selected_data=selected_data)

    fig = px.density_heatmap(
        cluster_dff,
        x="X",
        y="Y",
        nbinsx=int(nbins),
        nbinsy=int(nbins),
        color_continuous_scale=color,
        facet_col=None if separated == "No" else "cluster",
        category_orders={"cluster": ["0", "1", "2"]}
    )
    fig.update_layout(template="plotly_white")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8014)
