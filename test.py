import dash_html_components as html
import dash_table as dt
import dash
import dash_core_components as dcc




app = dash.Dash()
app.layout = html.Div(id='circos-control-tabs', className='control-tabs', children=[
            dt.DataTable(),
            dcc.Tabs(id='circos-tabs', value='what-is', children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children="What is Circos?"),

                        html.P('Circos is a circular visualization of data, and can be used '
                               'to highlight relationships between objects in a dataset '
                               '(e.g., genes that are located on different chromosomes '
                               'in the genome of an organism).'),
                        html.P('A Dash Circos graph consists of two main parts: the layout '
                               'and the tracks. '
                               'The layout sets the basic parameters of the graph, such as '
                               'radius, ticks, labels, etc; the tracks are graph layouts '
                               'that take in a series of data points to display.'),
                        html.P('The visualizations supported by Dash Circos are: heatmaps, '
                               'chords, highlights, histograms, line, scatter, stack, '
                               'and text graphs.'),
                        html.P('In the "Data" tab, you can opt to use preloaded datasets; '
                               'additionally, you can download sample data that you would '
                               'use with a Dash Circos component, upload that sample data, '
                               'and render it with the "Render" button.'),
                        html.P('In the "Graph" tab, you can choose the type of Circos graph '
                               'to display, control the size of the graph, and access data '
                               'that are generated upon hovering over parts of the graph. '),
                        html.P('In the "Table" tab, you can view the datasets that define '
                               'the parameters of the graph, such as the layout, the '
                               'highlights, and the chords. You can interact with Circos '
                               'through this table by selecting the "Chords" graph in the '
                               '"Graph" tab, then viewing the "Chords" dataset in the '
                               '"Table" tab.'),

                        html.Div([
                            'Reference: ',
                            html.A('Seminal paper',
                                   href='http://www.doi.org/10.1101/gr.092759.109)')
                        ]),
                        html.Div([
                            'For a look into Circos and the Circos API, please visit the '
                            'original repository ',
                            html.A('here', href='https://github.com/nicgirault/circosJS)'),
                            '.'
                        ]),

                        html.Br()
                    ])
                ),

                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children="What is Circos?"),

                        html.P('Circos is a circular visualization of data, and can be used '
                               'to highlight relationships between objects in a dataset '
                               '(e.g., genes that are located on different chromosomes '
                               'in the genome of an organism).'),


                        html.Div([
                            'Reference: ',
                            html.A('Seminal paper',
                                   href='http://www.doi.org/10.1101/gr.092759.109)')
                        ]),
                        html.Div([
                            'For a look into Circos and the Circos API, please visit the '
                            'original repository ',
                            html.A('here', href='https://github.com/nicgirault/circosJS)'),
                            '.'
                        ]),

                        html.Br()
                    ])
                ),



            ])
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
