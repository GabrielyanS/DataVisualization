import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

mouse_data = pd.read_csv('Mouse_metadata.csv')
study_results = pd.read_csv('Study_results.csv')
merged_df = pd.merge(mouse_data, study_results, on = 'Mouse ID')

new = pd.crosstab(merged_df['Drug Regimen'],merged_df["Timepoint"])
alive_df = new.stack().reset_index().rename(columns={0:'value'})



new1 = pd.crosstab(merged_df['Drug Regimen'], merged_df['Timepoint'], values=merged_df["Metastatic Sites"], aggfunc='mean')
mean_df = new1.stack().reset_index().rename(columns={0:'value'})
mean_df[mean_df["Drug Regimen"] == "Ceftamin"]
# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

drug_colors = {
	'Placebo':		'#29304E',
	'Capomulin':	'#27706B',	
	'Ramicane':		'#71AB7F',
	'Ceftamin':		'#9F4440',
	'Infubinol':	'#FFD37B',
	'Ketapril':		'#FEADB9',
	'Naftisol':		'#B3AB9E',
	'Propriva':		'#ED5CD4',
	'Stelasyn':		'#97C1DF',
	'Zoniferol':	'#8980D4'
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



# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need to have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Title'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)

# -------------------------------------------------------------------------------------- DIV for first row (1.1 and 1.2)

# -------------------------------------------------------------- inside DIV 1.1
div_1_1_button = dcc.Checklist(
				id = 'weight-histogram-checklist',
		        options=[
		        	{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])
		        ],
		        value=['Placebo'],
		        labelStyle={'display': 'inline-block'}
			)

div_1_1_graph = dcc.Graph(
				id = 'weight-histogram',
		        
			)

div_1_1 = html.Div(children = [div_1_1_button, div_1_1_graph],
				#className = 'test',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					},
					        

				)

div_1_2_button = dcc.RadioItems(
							id = 'radioitems-for-overlay-weights-histogram',
					        options=[
					            {'label': drug, 'value': drug} 
					            		for drug in np.unique(mouse_data['Drug Regimen'])
					        ],
					        labelStyle={'display': 'inline-block'},
		        value='Placebo'
		    )

div_1_2_graph = dcc.Graph(
						id = 'overlay-weights-histogram'
		    )


div_1_2 = html.Div(children = [div_1_2_button, div_1_2_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)

# Collecting DIV 1.1 and 1.2 into the DIV of first row.
# Pay attention to the 'display' and 'flex-flaw' attributes.
# With this configuration you are able to let the DIV-s 1.1 and 1.2 be side-by-side to each other.
# If you skip them, the DIV-s 1.1 and 1.2 will be ordered as separate rows.
# Pay also attention to the 'width' attributes, which specifiy what percentage of full row will each DIV cover.
div_row1 = html.Div(children =	[div_1_1,
								div_1_2],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


# -------------------------------------------------------------------------------------- DIV for second row (2.1 and 2.2)


div_2_1_button_1 = dcc.Checklist(
							id = 'checklist-weights-three-categories-1',
					        options=[
					            {'label': 'lightweight', 'value': 'lightweight'},
					            {'label': 'heavyweight', 'value': 'heavyweight'},
					            {'label': 'placebo', 'value': 'placebo'},
					        ],
					        labelStyle={'display': 'inline-block'},
		        value=['placebo']
		    )

div_2_1_button_2 = dcc.Checklist(
							id = 'checklist-weights-three-categories-2',
					        options=[
					            
					        ],
					        labelStyle={'display': 'inline-block'},
		    )

div_2_1_graph = dcc.Graph(
						id = 'graph-weights-three-categories',
		    )


div_2_1 = html.Div(children = [div_2_1_button_1, div_2_1_button_2, div_2_1_graph],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)

div_2_2_button = dcc.Checklist(
						id = 'checklist-three-categories-survival-function',
					        options=[
					            {'label': 'lightweight', 'value': 'lightweight'},
					            {'label': 'heavyweight', 'value': 'heavyweight'},
					            {'label': 'placebo', 'value': 'placebo'},
					        ],
					        labelStyle={'display': 'inline-block'},
		        value=['placebo']
		    )

div_2_2_graph = dcc.Graph(
						id = 'survival-function'
		    )

div_2_2 = html.Div(children = [div_2_2_button, div_2_2_graph],
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


# -------------------------------------------------------------------------------------- DIV for the last 2 rows (3 and 4)


div_row3 = dcc.Graph(
						id = 'tumor-volume',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )

div_row4 = dcc.Graph(
						id = 'metastatic-sites',
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
					}
		    )


# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV
app.layout = html.Div(	[
						div_title,
						div_row1,
						div_row2,
						div_row3,
						div_row4
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)

# -------------------------------------------------------------------------------------------------------------- 

#											PART 3: CALLBACKS

# --------------------------------------------------------------------------------------------------------------

# histogram of mice weights' for each drug
# it is a stacked histogram which lets us put histograms on top of each other 
@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    
    traces = []

    for drug in drug_names:
    	traces.append(go.Histogram(x=mouse_data[mouse_data['Drug Regimen']==drug]['Weight (g)'],
    							name = drug,
    							opacity = 0.9,
    							marker = dict(color=drug_colors[drug]))
    				)

    return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'mouse weight',
   					'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
   					'showgrid': False
   					},
            yaxis={'title': 'number of mice', 
            		'showgrid': False,
            		'showticklabels': True
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }

# another histogram (this time we create an overlay one)
# it has radioitems (you can choose only 1 drug)
# it will create a chart of all mice's weight distribution as background
# then it will overlay each chosen drug's distribution

@app.callback(
    Output('overlay-weights-histogram', 'figure'),
    [Input('radioitems-for-overlay-weights-histogram', 'value')]
)
def update_overlay_histogram(drug_name):
    
    traces = []
 
    # here we add the overall distribution with a smaller opacity
    traces.append(go.Histogram(x=merged_df['Weight (g)'],
    							opacity=0.9,
    							name = 'all mice',
    							marker = dict(color=colors['histogram-color-1'])
	    			)
	    		)

    # histogram for each drug
    # we use opacity so that we can see the two overlayed distributions
    traces.append(go.Histogram(x=merged_df[merged_df['Drug Regimen']==drug_name]['Weight (g)'],
    							opacity=0.85,
    							name = drug_name,
    							marker = dict(color=drug_colors[drug_name])
			    	)
			    )


    # we return a dictionary which has 2 keys: one for charts, the other one for layout
    return {
        'data': traces,
        'layout': dict(
        	barmode='overlay',
            xaxis={'title': 'mouse weight',
   					'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
   					'showgrid': False
   					},
            yaxis={'title': 'number of mice', 
            		'showgrid': False,
            		# 'showticklabels': True
            		},
            # height = sizes['cha'],
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},

        )
    }



@app.callback(
    [Output('checklist-weights-three-categories-2', 'options'),
    Output('checklist-weights-three-categories-2', 'value')],
    [Input('checklist-weights-three-categories-1', 'value')])
def set_weights_2_options(selected_categories):
	categories = {'lightweight': ['Capomulin','Ramicane'],
					'placebo': ['Placebo'],
					'heavyweight': ['Ceftamin', 'Infubinol', 'Ketapril', 
								'Naftisol', 'Propriva', 'Stelasyn','Zoniferol']}
	output_options = []
	for category in selected_categories:
		output_options.extend(categories[category])
	return [{'label': i, 'value': i} for i in output_options], output_options


@app.callback(
    Output('graph-weights-three-categories', 'figure'),
    [Input('checklist-weights-three-categories-2', 'value')]
)
def update_weight_categories_histogram(drug_list):
    traces = []
    if drug_list:
	    for drug_name in drug_list:
		    traces.append(go.Histogram(x=merged_df[merged_df['Drug Regimen']==drug_name]['Weight (g)'],
		    							opacity=0.6,
		    							name = drug_name,
		    							marker = dict(color=drug_colors[drug_name])
					    	)
					    )

    return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'mouse weight',
   					'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()]
   					},
            yaxis={'title': 'number of mice', 
            		'showgrid': False,
            		'showticklabels': False
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }
@app.callback(
	Output('survival-function', 'figure'),
   	[Input('checklist-three-categories-survival-function', 'value')]
)

def linechart(selected_categories):
	categories = {'lightweight': ['Capomulin','Ramicane'],
					'placebo': ['Placebo'],
					'heavyweight': ['Ceftamin', 'Infubinol', 'Ketapril', 
								'Naftisol', 'Propriva', 'Stelasyn','Zoniferol']}
	output_options = []
	for category in selected_categories:
		output_options.extend(categories[category])
	traces = []

	if output_options:
		for drug_name in output_options:
			traces.append(go.Scatter(x=alive_df[alive_df['Drug Regimen']==drug_name]['Timepoint'],y=alive_df[alive_df['Drug Regimen']==drug_name]['value'],
    	        	                opacity=0.85,
    								name = drug_name,
    								marker = dict(color=drug_colors[drug_name]),
    								customdata = [(drug_name,i) for i in merged_df["Timepoint"].unique()]
					    	)
					    )

	return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis={'title': 'Timepoint',
   					'range': [alive_df['Timepoint'].min()-4, alive_df['Timepoint'].max()+4]
   					},
            yaxis={'title': 'Number of alive mice', 
            		'showgrid': False,
            		'showticklabels': False
            		},
            autosize=False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            clickmode = 'event+select'
        )
    }


#boxplot
@app.callback(
	Output('tumor-volume', 'figure'),
   	[Input('survival-function', 'selectedData')]
)

def update_boxplot(selectedData):
	traces = []
	drug_names = []
	if selectedData:
		for i in selectedData['points']:
			drug_names.append(i['customdata'][0])
	if drug_names:
	  	for drug_name in drug_names:
	  		print(drug_name)
	  		traces.append(go.Box(x = merged_df[merged_df['Drug Regimen'] == drug_name]['Timepoint'],
				y = merged_df[merged_df['Drug Regimen'] ==  drug_name]['Tumor Volume (mm3)'],
		    							opacity = 0.6,
		    							name =  drug_name,
		    							marker = dict(color=drug_colors[drug_name])
					    	)
					    )

	return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis = {'title': 'Timepoint',
   					'range': [merged_df['Timepoint'].min()-4, merged_df['Timepoint'].max()+4]
   					},
            yaxis = {'title': 'Tumor volume', 
            		'showgrid': False,
            		'showticklabels': False
            		},
            autosize = False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin = {'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend = {'x': 0, 'y': 1},
        )
    }


#last
@app.callback(
	Output('metastatic-sites', 'figure'),
   	[Input('survival-function', 'selectedData')]
)
def update_linechart(selectedData):
	traces = []
	drug_names = []
	if selectedData:
		for i in selectedData['points']:
			drug_names.append(i['customdata'][0])
	if drug_names:
	  	for drug_name in drug_names:
	  		print(drug_name)
	  		traces.append(go.Scatter(x = mean_df[mean_df['Drug Regimen'] == drug_name]['Timepoint'],
				y = mean_df[mean_df['Drug Regimen'] ==  drug_name]['value'],
		    							opacity = 0.6,
		    							name =  drug_name,
		    							marker = dict(color=drug_colors[drug_name])
					    	)
					    )

	return {
        'data': traces,
        'layout': dict(
        	barmode='stack',
            xaxis = {'title': 'Timepoint',
   					'range': [merged_df['Timepoint'].min()-4, merged_df['Timepoint'].max()+4]
   					},
            yaxis = {'title': 'Mean of Metastatic sites', 
            		'showgrid': False,
            		'showticklabels': False
            		},
            autosize = False,
           	paper_bgcolor = colors['chart-background'],
           	plot_bgcolor = colors['chart-background'],
            margin = {'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend = {'x': 0, 'y': 1},
        )
    }




# -------------------------------------------------------------------------------------------------------------- 

#											PART 4: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
if __name__ == '__main__':
	app.run_server(debug = True, port = 8087, host = '0.0.0.0')