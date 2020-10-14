import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import CMS_Inpatient_Claims_Line_Trend_Chart, CMS_Outpatient_Claims_Line_Trend_Chart


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Inpatient Claims|', href='/apps/CMS_Inpatient_Claims_Line_Trend_Chart'),
        dcc.Link('Outpatient Claims', href='/apps/CMS_Outpatient_Claims_Line_Trend_Chart'),
    ], className="row"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/CMS_Inpatient_Claims_Line_Trend_Chart':
        return CMS_Inpatient_Claims_Line_Trend_Chart.layout
    if pathname == '/apps/CMS_Outpatient_Claims_Line_Trend_Chart':
        return CMS_Outpatient_Claims_Line_Trend_Chart.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
