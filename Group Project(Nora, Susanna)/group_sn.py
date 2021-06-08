import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json


import plotly.graph_objects as go
from pprint import pprint


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


# Loading our data 
data = pd.read_csv('movie_metadata.csv')
data["genres"] = data["genres"].str.split(pat="|").str[0]

top_10_countries = ["USA","UK","France","Canada", "Germany","Australia","China","Spain","India","Japan" ]
data = data[data['country'].isin(top_10_countries)]

data_genres = data.groupby(['country',"genres"]).size()
data_genres = data_genres.reset_index()

data_new = data.sort_values("actor_1_facebook_likes",ascending = False)[["country","actor_1_name","movie_title","actor_1_facebook_likes"]]

data_director = data.sort_values("movie_facebook_likes",ascending = False)[["movie_facebook_likes","director_name","movie_title","country"]].head(10)


data_imdb = data.groupby(['country']).mean()[['imdb_score']].reset_index()
data_imdb["Code"] = ['AUS','CAN','CHN','FRA','DEU','IND','JPN','ESP','GBR', 'USA']
data_imdb



data1 = data.replace({
    'US' : 'USA', 
    'Canada' : 'CAN', 
    'Australia' : 'AUS', 
    'China' : 'CHN', 
    'France' : 'FRA', 
    'Germany' : 'DEU',
    'India' : 'IND' ,
    'Japan' : 'JPN',
    'Spain' : 'ESP' ,
    'UK' : 'GBR' 
})





color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

country_colors = {
	"USA":		'#29304E',
	"UK":	'#27706B',	
	"France":		'#71AB7F',
	"Canada":		'#9F4440',
	"Germany":	'#FFD37B',
	"Australia":		'#FEADB9',
	"China":		'#B3AB9E',
	"Spain":		'#ED5CD4',
	"India":		'#97C1DF',
	"Japan":	'#8980D4'
}

colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'histogram-color-1':	color_choices['dark-blue'],
		'histogram-color-2':	color_choices['light-red'],
		'block-borders':		color_choices['dark-blue']
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': '290px'
}


#Creating our graphs

div_title = html.Div(children =	html.H1('IMDB 5000 dataset'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)


div_1_1_button = dcc.Checklist(
				id = 'genres-barplot-checklist',
		        options=[
		        	{'label': country, 'value': country} for country in np.unique(data['country'])
		        ],
		        value=['USA'],
		        labelStyle={'display': 'inline-block'}
			)

div_1_1_graph = dcc.Graph(
				id = 'country-barplot',
		        
			)

div_1_1 = html.Div(children = [div_1_1_button, div_1_1_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
					},
					        

				)

div_1_2_graph = dcc.Graph(
				id = 'genres-boxplot',
		        
			)

div_1_2 = html.Div(children = [div_1_2_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)

div_row1 = html.Div(children =	[div_1_1,
								div_1_2],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

div_2_1_graph = dcc.Graph(
						id = 'genres-barplot',

		    )
div_2_1 = html.Div(children = [div_2_1_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)

div_2_2_table = dash_table.DataTable(
				id='table',
    			columns=[{"name": i, "id": i} for i in data_new.columns],
    			data=data_new.to_dict('records')
				)

div_2_2 = html.Div(children = [div_2_2_table],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)


div_row2 = html.Div(children =	[div_2_1,
								div_2_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

div_3_button = dcc.Checklist(
				id = 'genres-histogram-checklist',
		        options=[
		        	{'label': genre, 'value': genre} for genre in np.unique(data['genres'])
		        ],
		        value=['Action'],
		        labelStyle={'display': 'inline-block'}
			)

div_graph3 = dcc.Graph(
						id = 'genres-histogram',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )
div_row3 = html.Div(children =	[div_3_button,
								div_graph3
								])
					# style ={
					# 		'border': '3px {} solid'.format(colors['block-borders']),
					# 		'margin': margins['block-margins'], 
					# 		'display': 'flex',
					# 		'flex-flaw': 'row-wrap'
					# 		})


div_4_slider = dcc.RangeSlider(
        id='slider',
        min = 1.6,
        max=10,
        value=[1, 2],
        step=0.01
    )

div_graph4 = dcc.Graph(
						id = 'money-plot',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )

div_row4 = html.Div(children =	[div_4_slider,
								div_graph4  
								])


div_5_1_table = dash_table.DataTable(
				id='table-director',
    			columns=[{"name": i, "id": i} for i in data_director.columns],
    			data=data_director.to_dict('records')
				)

div_5_1 = html.Div(children = [div_5_1_table],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)


div_5_2_button = dcc.Checklist(
				id = 'director-boxplot-checklist',
		        options=[
		        	{'label': director, 'value': director} for director in np.unique(data_director["director_name"])
		        ],
		        value=['Christopher Nolan'],
		        labelStyle={'display': 'inline-block'}
			)
div_5_2_graph = dcc.Graph(
				id = 'director-boxplot',
		        
			)
div_5_2 = html.Div(children = [div_5_2_button,div_5_2_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)


div_row5 = html.Div(children =	[div_5_1,
								div_5_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'], 
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})
div_6_button = dcc.Checklist(
				id = 'genres-map-checklist',
		        options=[
		        	{'label': genre, 'value': genre} for genre in np.unique(data["genres"])
		        ],
		        value=['Drama'],
		        labelStyle={'display': 'inline-block'}
			)


div_graph6 = dcc.Graph(
					id = 'map-plot',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )

div_row6 = html.Div(children =	[div_6_button,div_graph6  
								])


div_graph7 = dcc.Graph(
					id = 'last-plot',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )

div_row7 = html.Div(children =	[div_graph7 
								])



app.layout = html.Div([
						div_title,
						div_row1,
						div_row2,
						div_row3,
						div_row4,
						div_row5,
						div_row7,
						div_row6
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)


#Barplot:Selecting country get the most popular genres for movies , for each country 
data_country = data.groupby(['country']).size()
data_country = data_country.reset_index()

@app.callback(
    Output(component_id='country-barplot', component_property='figure'),
    [Input(component_id='genres-barplot-checklist', component_property='value')]
)
def update_bar(country_names):
    
    traces = []

    for country in country_names:
    	traces.append(go.Bar( x = data_country[data_country['country']==country]['country'],y = data_country[data_country['country']==country][0],
    							opacity = 0.9,
    							name = country,
    							customdata = [(country,i) for i in np.arange(0,45,5)],
    							marker = dict(color=country_colors[country]),
    							
    				))
    return {
    	'data': traces,
		'layout': dict(
			boxmode='group',
			xaxis={'title': 'Country'
					},
			yaxis={'title': 'Number of movies', 
					'showgrid': False,
					'showticklabels': True
					},
			autosize=False,
			paper_bgcolor = colors['chart-background'],
			plot_bgcolor = colors['chart-background'],
			margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
			legend={'x': 0, 'y': 1},
			clickmode = 'event+select'
		)
	}

#Boxplot:Where we select the country name from previous graph and get the boxplot for that country, on x axis genres and on y axis is imdb score. 
box_data = data.groupby(['country','genres','imdb_score']).size()
box_data = box_data.reset_index()


@app.callback(
    Output('genres-boxplot', 'figure'),
    [Input('country-barplot','selectedData')]
)
def boxplot(selectedData):
	traces = []
	if selectedData:
		country_list = [selection['customdata'][0] for selection in selectedData['points']]
		for country_name in country_list:
			traces.append(go.Box(x = data[data['country']==country_name]['genres'], y = data[data['country']==country_name]['imdb_score'],
											opacity=0.6,
											name = country_name,
											marker = dict(color=country_colors[country_name])	    										
	    					)
					    )

	return {
        'data': traces,
        'layout': dict(
        	boxmode='group',
            xaxis={'title': 'Genre'
   					},
            yaxis={'title': 'IMDB Score', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


@app.callback(
    Output('genres-barplot', 'figure'),
    [Input('country-barplot','selectedData')]
)
def boxplot(selectedData):
	traces = []
	if selectedData:
		country_list = [selection['customdata'][0] for selection in selectedData['points']]
		for country_name in country_list:
			traces.append(go.Bar(x = data_genres[data_genres['country']==country_name]['genres'], y = data_genres[data_genres['country']==country_name][0],
											opacity=0.6,
											name = country_name,
											marker = dict(color=country_colors[country_name])	    										
	    					)
					    )

	return {
        'data': traces,
        'layout': dict(
        	boxmode='group',
            xaxis={'title': 'Genre'
   					},
            yaxis={'title': 'Number of movies', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


#Here is the interactive table i

# @app.callback(
#     Output('table', 'data'),
#     [Input('country-barplot','selectedData')]
# )

# def update_table(selectedData):
# 	if selectedData:
# 		country_list = [selection['customdata'][0] for selection in selectedData['points']]
# 		for country_name in country_list:
# 			dff = dash_table.DataTable(
#     					id='table',
#     					data=data_new[data_new['country']== country_name].to_dict('rows'),
#     					columns=[{"name": i, "id": i} for i in data_new[data_new['country']== country_name].columns],)


# 	return{dff
#     }

# go.Figure(data=[go.Table(
# 				header=dict(values=list(data_new.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     			cells=dict(values=[data_new[data_new['country']==country_name].actor_1_name, data_new[data_new['country']==country_name].movie_title, data_new[data_new['country']==country_name].actor_1_facebook_likes],
#                 fill_color='lavender',
#                 align='left'))
# ])

@app.callback(
    Output('table', 'data'),
    [Input('country-barplot','selectedData')]
)
def update_table(selectedData):
	country_list = ['USA']
	if selectedData:
		country_list = [selection['customdata'][0] for selection in selectedData['points']]
	traces = pd.DataFrame()
	for country_name in country_list:
		traces = traces.append(data_new[data_new['country'] == country_name])
	return traces.head(10).to_dict('records')



#ploting histogram with duration for each genre 
@app.callback(
    Output(component_id='genres-histogram', component_property='figure'),
    [Input(component_id='genres-histogram-checklist', component_property='value')]
)
def update_weight_histogram(genre_names):
    
    traces = []

    for genre in genre_names:
    	traces.append(go.Histogram(x=data[data['genres']==genre]['duration'],
    							name = genre,
    							opacity = 0.9)
    							
    				)

    return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'Duration',
   					'range': [data['duration'].min(), data['duration'].max()],
   					'showgrid': False
   					},
            yaxis={'title': 'Frequency', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1}
        )
    }

#Scatter plot or scatter line with slider (for score range) and with selectedData from previus graph to select the genre for what we want to know the money 


data['money'] = data['gross']-data['budget']

@app.callback(
	Output('money-plot', 'figure'),
   	[
   	Input(component_id='genres-histogram-checklist', component_property='value'),
   	Input('slider','value')
   	]
)
def linechart(genre_names,value):
	x1 = data[(data['imdb_score'] > value[0]) & (data['imdb_score'] < value[1])]

	traces = []
	for genre in genre_names:
		traces.append(go.Scatter(x = x1[x1['genres']== genre]['budget'], y = x1[x1['genres']== genre]['money'],
		    							opacity=0.6,
		    							name = genre,
		    							mode='markers'
					    	)
					    )

	return {
		'data': traces,
		'layout': dict(
			barmode='stack',
			xaxis={'title': 'Budget',
					'range': [-1, x1['budget'].max()]
					},
			yaxis={'title': 'Profit', 
            		'showgrid': False,
            		'showticklabels': False
            		},
			autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, ' r': 10},
          	legend={'x': 0, 'y': 1}
        )
	}


@app.callback(
    Output('director-boxplot', 'figure'),
    [Input('director-boxplot-checklist','value')]
)
def boxplot2(director_list):
	traces = []
	for director_name in director_list:
		traces.append(go.Box(x = data[data['director_name']==director_name]['director_name'], y = data[data['director_name']==director_name]['imdb_score'],											
			opacity=0.6,
			name = director_name,
			#marker = dict(color=country_colors[country_name])	    										
	    	)
	    )

	return {
        'data': traces,
        'layout': dict(
        	boxmode='group',
            xaxis={'title': 'Director name'
   					},
            yaxis={'title': 'IMDB Score', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
            legend={'x': 0, 'y': 1},
        )
    }



@app.callback(
    Output('map-plot', 'figure'),
    [Input('genres-map-checklist','value')]
)
def mapplot(genres_list):
	traces = []
	for genre in genres_list:
		data_temp = data1[data1['genres'] == genre]
		data_temp = data_temp.groupby(['country']).mean()[['imdb_score']].reset_index()
		traces.append(go.Choropleth(locations = data_temp['country'],
                    z = data_temp["imdb_score"],
                    zmin = 1.6,
                    zmax = 10, 
                    geojson = data_temp["country"], 
                    marker_opacity=0.5)
			#marker = dict(color=country_colors[country_name])	    										
	    	)

	return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Director name'
   					},
            yaxis={'title': 'IMDB Score', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
            legend={'x': 0, 'y': 1},
        )
    }




@app.callback(
    Output('last-plot', 'figure'),
    [Input('director-boxplot-checklist','value')]
)
def last(director_list):
	traces = []
	for director_name in director_list:
		traces.append(go.Scatter(x = sorted(data[data['director_name']==director_name]['title_year']), y = data[data['director_name']==director_name]['imdb_score'],											
			opacity=0.6,
			name = director_name,
			#marker = dict(color=country_colors[country_name])	    										
	    	)
	    )

	return {
        'data': traces,
        'layout': dict(
        	boxmode='group',
            xaxis={'title': 'Year'
   					},
            yaxis={'title': 'IMDB Score', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 50, 'b': 40, 't': 10, ' r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


if __name__ == '__main__':
	app.run_server(debug = True, port = 8086)


