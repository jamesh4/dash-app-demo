import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
from vega_datasets import data
alt.data_transformers.enable('json')

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

def make_plot(year):

    df = data.movies()

    df["Release_Date"] = pd.to_datetime(df["Release_Date"]) # Converting to datetime format
    df["year"] = pd.DatetimeIndex(df['Release_Date']).year # Creating years column for future use
    df = df.query("year < 2010") # years above 2010 are either mislabeled or the sample size is too small 

    df["International_Gross"] = df["Worldwide_Gross"] - df["US_Gross"]

    df_boxoffice = df[["International_Gross", "year", "US_Gross"]]

    df_boxoffice = df_boxoffice.melt(id_vars = "year",
       var_name = "type",
       value_name = "dollars")

    bo_chart = alt.Chart(df_boxoffice).mark_bar().encode(
        alt.Y('dollars', aggregate = "mean", axis=alt.Axis(title='Dollars')),
        alt.X('year:O', axis=alt.Axis(title='Year')),
        color = "type"
    ).properties(
        title = "Average box office of US movies over time overlayed with production budget"
    )

    return bo_chart

app.layout = html.Div([

    html.H1('aaaaaaa'),

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('TfsdfaSAA TITLE'),
    html.H2('This is a subtitle'),

    html.H3('Here is an image'),
    html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            width='20%'),

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='500',
        width='500',
        style={'border-width': '1px'},

        ################ The magic happens here
        srcDoc=make_plot([1950, 2000]).to_html()
        ################ The magic happens here
        ),

    dcc.Markdown('''
        ASDFSAFSAFAFSDFAJFDSAJK:KADFS
        print("helo")
    '''),

    dcc.Dropdown(
        options = [
            {'label': 'New York', 'value': 'NYC'},
            {'label': 'Vancouver', 'value': 'YVR'},

        ],
        value = 'YVR',
    ),

    dcc.RangeSlider(
        id = 'my-slider',
        min = 1930,
        max = 2010,
        step = 1,
        value = [1950, 2000],
        allowCross = False,
    ),

    html.Div(id='slider-output-container')

    
])

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return str(value)




if __name__ == '__main__':
    app.run_server(debug=True)
