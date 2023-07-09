from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd


# neu: einfachst mögliches app, ohne styling oder anderen schnick-schnack

app = Dash(__name__)

# generate random normal distributed data and store it in a pandas DataFrame
df = pd.DataFrame({'number': np.random.normal(loc=0,
                                              scale=10,
                                              size=1000)})

app.layout = html.Div([
    html.H1("Dashboard 1"),
    dcc.Dropdown(options=['red', 'green', 'blue'],
                 value='red',
                 id='color',
                 multi=False),
    dcc.Graph(id="graph")
])


@app.callback(
    Output("graph", "figure"),
    Input("color", "value")
)
def update_graph(dropdown_value_color):

    fig = px.histogram(df,
                       x="number",
                       color_discrete_sequence=[dropdown_value_color] )
    fig.update_layout()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
