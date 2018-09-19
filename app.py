import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go

app = dash.Dash() # make python obj with Dash() method
dfTips = sns.load_dataset('tips') # load tips dataset from seaborn
color_set = {
    'sex': ['#ff3fd8','#4290ff'],
    'smoker': ['#32fc7c','#ed2828'],
    'time': ['#0059a3','#f2e200'],
    'day': ['#ff8800','#ddff00','#3de800','#00c9ed']
}

# function to generate HTML Table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col,className='table_dataset') for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],className='table_dataset') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
        className='table_dataset'
    )

app.title = 'Purwadhika Dash Plotly'; # set web title

#the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value="tab-1", children=[
            dcc.Tab(label='Tips Data Set', value="tab-1", children=[
                html.Div([
                    html.H1(
                        children='Tips Data Set',
                        className='h1FirstTab'
                    ),
                    generate_table(dfTips)
                ])
            ]),
            dcc.Tab(label='Scatter Plot', value="tab-2", children=[
                html.Div([
                    html.H1(
                        children='Scatter Plot Tips Data Set',
                        className='h1FirstTab'
                    ),
                    html.Table([
                        html.Tr([
                            html.Td([html.P('Hue : '),
                                    dcc.Dropdown(
                                        id='ddl-hue-scatter-plot',
                                        options=[{'label': 'Sex', 'value': 'sex'},
                                                {'label': 'Smoker', 'value': 'smoker'},
                                                {'label': 'Day', 'value': 'day'},
                                                {'label': 'Time', 'value': 'time'}],
                                        value='sex'
                                    )]
                            )
                        ])
                    ],style={ 'width': '300px' }),
                    dcc.Graph(
                        id='scatterPlot',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=dfTips[dfTips['sex'] == col]['total_bill'], 
                                    y=dfTips[dfTips['sex'] == col]['tip'], 
                                    mode='markers', 
                                    # line=dict(color=color_set[i], width=1, dash='dash'), 
                                    marker=dict(color=color_set['sex'][i], size=10, line={'width': 0.5, 'color': 'white'}), name=col)
                                for col,i in zip(dfTips['sex'].unique(),range(len(color_set['sex'])))
                            ],
                            'layout': go.Layout(
                                xaxis={'title': 'Total Bill'},
                                yaxis={'title': 'Tip'},
                                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                hovermode='closest'
                            )
                        }
                    )
                ])
            ]),
            dcc.Tab(label='Bar Plot', value="tab-3", children=[
                html.Div([
                    html.H1(
                        children='Bar Plot Tips Data Set',
                        className='h1FirstTab'
                    )
                ]),
                html.Table([
                    html.Tr([
                        html.Td([html.P('X Axis : '),
                                dcc.Dropdown(
                                    id='ddl-x-bar-plot',
                                    options=[{'label': 'Sex', 'value': 'sex'},
                                            {'label': 'Smoker', 'value': 'smoker'},
                                            {'label': 'Day', 'value': 'day'},
                                            {'label': 'Time', 'value': 'time'}],
                                    value='sex'
                                )]
                        ),
                        html.Td([html.P('Text : '),
                                dcc.Dropdown(
                                    id='ddl-text-bar-plot',
                                    options=[{'label': 'Sex', 'value': 'sex'},
                                            {'label': 'Smoker', 'value': 'smoker'},
                                            {'label': 'Day', 'value': 'day'},
                                            {'label': 'Time', 'value': 'time'},
                                            {'label': 'Size', 'value': 'size'}],
                                    value='sex'
                                )]
                        )
                    ])
                ],style={ 'width': '900px' }),
                dcc.Graph(
                    id='barPlot',
                    figure={
                        'data': [
                            go.Bar(
                                x=dfTips['sex'],
                                y=dfTips['tip'],
                                text=dfTips['day'],
                                opacity=0.7,
                                name='Tip'
                            ),
                            go.Bar(
                                x=dfTips['sex'],
                                y=dfTips['total_bill'],
                                text=dfTips['day'],
                                opacity=0.7,
                                name='Total Bill'
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Sex'}, yaxis={'title': 'US$'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1}, hovermode='closest',
                            # plot_bgcolor= 'black', paper_bgcolor= 'black',
                        )
                    }
                )
            ])
        ],
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        }
    )], 
    style={
        'maxWidth': '1000px',
        'margin': '0 auto'
    }
)

@app.callback(
    dash.dependencies.Output('scatterPlot', 'figure'),
    [dash.dependencies.Input('ddl-hue-scatter-plot', 'value')])
def update_scatter_graph(ddlHueScatterPlot):
    return {
            'data': [
                go.Scatter(
                    x=dfTips[dfTips[ddlHueScatterPlot] == col]['total_bill'], 
                    y=dfTips[dfTips[ddlHueScatterPlot] == col]['tip'], 
                    mode='markers', 
                    # line=dict(color=color_set[i], width=1, dash='dash'), 
                    marker=dict(color=color_set[ddlHueScatterPlot][i], size=10, line={'width': 0.5, 'color': 'white'}), name=col)
                for col,i in zip(dfTips[ddlHueScatterPlot].unique(),range(len(color_set[ddlHueScatterPlot])))
            ],
            'layout': go.Layout(
                xaxis={'title': 'Total Bill'},
                yaxis={'title': 'Tip'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
    };

@app.callback(
    dash.dependencies.Output('barPlot', 'figure'),
    [dash.dependencies.Input('ddl-x-bar-plot', 'value'),
    dash.dependencies.Input('ddl-text-bar-plot', 'value')])
def update_bar_graph(ddlXBarPlot, ddlTextBarPlot):
    return {
            'data': [
                go.Bar(
                    x=dfTips[ddlXBarPlot],
                    y=dfTips['tip'],
                    text=dfTips[ddlTextBarPlot],
                    opacity=0.7,
                    name='Tip'
                ),
                go.Bar(
                    x=dfTips[ddlXBarPlot],
                    y=dfTips['total_bill'],
                    text=dfTips[ddlTextBarPlot],
                    opacity=0.7,
                    name='Total Bill'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': ddlXBarPlot.capitalize()},
                yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
    };


if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=2000) 

    


