
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Example using sample data
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 15, 12]
})


app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
            dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
        ],
        brand="Dashboard",
        brand_href="/",
        sticky="top",
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'margin': '20px'},
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        editable=True,
        row_deletable=True
    ),
    html.Div(id='output-container')
])

# Page 1 layout
page1_layout = html.Div([
    html.H2('Page 1 Content'),
    dcc.Graph(
        id='bar-chart',
        figure=px.bar(df, x='Category', y='Value', title='Bar Chart')
    )
])

# Page 2 layout
page2_layout = html.Div([
    html.H2('Page 2 Content'),
    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x='Category', y='Value', title='Scatter Plot')
    )
])

# Callback to render different pages based on the URL
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/page1':
        return page1_layout
    elif pathname == '/page2':
        return page2_layout
    else:
        return html.H2('404 - Page not found')
    
import datetime

@app.callback(Output('output-container', 'children'), [Input('datatable', 'active_cell')])
def create_new_page(active_cell):
    if active_cell:
        row_index = active_cell['row']
        #cell_value = active_cell['row_id']
        new_page_layout = html.Div([
            html.H2(f'Page for {datetime.datetime.now()}'),
            html.P('This is a new page created by clicking on a cell of the data table.')
        ])
        return new_page_layout
    else:
        return None




if __name__ == '__main__':
    app.run_server(debug=True)
