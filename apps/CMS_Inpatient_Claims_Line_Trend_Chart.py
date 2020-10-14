import pandas as pd
import plotly.express as px
import dash
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pathlib
from app import app
# To get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# app = dash.Dash(__name__)

# -----------------------------------------------------------------
df = pd.read_csv(DATA_PATH.joinpath('2008_to_2010_Inpatient_Claims.csv'), parse_dates=['CLM_THRU_DT'])
df['year'] = df['CLM_THRU_DT']
# print(df['year'][:10])
payout_set = ['CLM_PMT_AMT', 'NCH_PRMRY_PYR_CLM_PD_AMT', 'CLM_PASS_THRU_PER_DIEM_AMT']

df_sum = ()
for i in payout_set:
    df_sum += (df[i].sum(axis=0, skipna=True),)

# ======================================================================================================================
# Yearly_Payout_Inpatient Claims
year = sorted(list(dict.fromkeys(df['year'])))
# print(year[:10])
payout_yearly_set = []
for i in year:
    df_filter = df[df['year'] == i]
    claims = len(df_filter)
    claim_payment_amount_yearly = (df_filter['CLM_PMT_AMT'].sum(axis=0, skipna=True))
    Primary_Payer_Claim_Paid_Amount = (df_filter['NCH_PRMRY_PYR_CLM_PD_AMT'].sum(axis=0, skipna=True))
    Claim_Pass_Thru_Per_Diem_Amount = (df_filter['CLM_PASS_THRU_PER_DIEM_AMT'].sum(axis=0, skipna=True))
    payout_yearly_set += [[i, claims, claim_payment_amount_yearly, Primary_Payer_Claim_Paid_Amount,
                           Claim_Pass_Thru_Per_Diem_Amount], ]
    # print(payout_yearly_set)
yearly_payout = pd.DataFrame(payout_yearly_set,
                             columns=['year', 'claims', 'claim_payment_amount_yearly',
                                      'Primary_Payer_Claim_Paid_Amount',
                                      'Claim_Pass_Thru_Per_Diem_Amount'])
df = df.groupby(['CLM_THRU_DT', 'CLM_PMT_AMT', 'NCH_PRMRY_PYR_CLM_PD_AMT', 'CLM_PASS_THRU_PER_DIEM_AMT'],
                as_index=False).sum()
row, col = df.shape
# print(payout_progress.shape)
# print(payout_progress.iat[0,1])
for i in range(1, row):
    for j in range(1, col):
        df.iat[i, j] = df.iat[i, j] + df.iat[i - 1, j]
print("Progress Report Done")
# print(df[:5])

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The App Layout.
app.layout = html.Div([
    html.H2('CMS-Medicare Data Analysis For Inpatient Claims',
            style={'border-radius': '10px', 'background-color': '#3aaab2', 'color': 'yellow', 'display': 'inline-block',
                   'width': '100%', 'text-align': 'center', 'padding': '50px', 'padding-top': '20px',
                   'padding-bottom': '20px'}
            ),
    html.H3(['Total Inpatient Claims Filed', html.Br(), len(df), '+'],
            style={'border-radius': '10px', 'background-color': 'orange', 'color': 'white',
                   'display': 'inline-block', 'width': '20%', 'height': '100px', 'text-align': 'center',
                   'margin-right': '3%', 'margin-left': '5%', 'padding-top': '5px', }),
    html.H3(['Total Claim Payment Amount', html.Br(), int(df_sum[0]), '+'],
            style={'border-radius': '10px', 'background-color': 'orange', 'color': 'white',
                   'display': 'inline-block', 'width': '20%', 'height': '100px', 'text-align': 'center',
                   'margin-right': '3%', 'padding-top': '5px', }),
    html.H3(['Total NCH Claim Paid Amount', html.Br(), int(df_sum[1]), '+'],
            style={'border-radius': '10px', 'background-color': 'orange', 'color': 'white',
                   'display': 'inline-block', 'width': '20%', 'height': '100px', 'text-align': 'center',
                   'margin-right': '3%', 'padding-top': '5px', }),
    html.H3(['Total Claim Diem Amount', html.Br(), int(df_sum[2]), '+'],
            style={'border-radius': '10px', 'background-color': 'orange', 'color': 'white',
                   'display': 'inline-block', 'width': '22%', 'height': '100px', 'text-align': 'center',
                   'margin-right': '3%', 'padding-top': '5px', }),
    html.Div([
        dcc.Dropdown(id='my_dropdown',
                     options=[
                         {'label': 'Claim Payment Amount', 'value': "CLM_PMT_AMT"},
                         {'label': 'Primary Payer Claim Paid Amount', 'value': "NCH_PRMRY_PYR_CLM_PD_AMT"},
                         {'label': 'Claim Pass Thru Per Diem Amount', 'value': "CLM_PASS_THRU_PER_DIEM_AMT"}
                     ],
                     value='CLM_PMT_AMT',
                     multi=False,
                     clearable=False,

                     ),
    ], className='six columns'),

    html.Div([
        dcc.Graph(id='line_graph', style={'width': "80%"})
    ], className='twelve columns'),
])


# - - - - - - -  - - The Call Back - - - - - - -

@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value'), ]
)
def plot_graph(column_chosen):
    dff = df
    fig = px.line(dff, x="CLM_THRU_DT", y=column_chosen, title="Line Chart Analysis for CMS-Inpatient Claims",
                  height=600)
    fig.layout.plot_bgcolor = 'white'

    return fig


# ---------------------------------------------------------------

# if __name__ == '__main__':
#     app.run_server(debug=False)
