import numpy as np
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py
import sys

def load_json_file(filename):
    # Open the JSON file for reading
    with open(filename, 'r') as file:
    # Load its content and turn it into a Python dictionary
        return json.load(file)

def if_append(a, b):
    try:
        if len(b):
            a.append(b)
    except TypeError:
        # This handles the case where 'a' does not support len()
        print("Provided item 'a' does not have a length.")

def add_bdplot_2_fig(fig, response, row, col, name, scale = 1, color_ = ''):
    """
    Adds a Bode magnitude and phase plot to a specified subplot cell in a Plotly figure.

    Parameters:
    - fig (go.Figure): The figure object to which the plots will be added.
    - frequencies (np.array): Array of frequencies (in Hz).
    - response (np.array): Complex array containing the frequency response of the system.
    - row (int): The subplot row index to place the plots.
    - col (int): The subplot column index to place the plots.
    """
    # Calculate magnitude in dB
    #magnitude = 20 * np.log10(np.abs(response)/scale)
    magnitude = np.abs(response)*scale
    
    # Calculate phase in degrees
    phase = np.angle(response, deg=True)
    fake_x = np.arange(len(response))
    # Adding Magnitude Plot to the specified subplot
    if color_ != '':
        line_color_dict=dict(
            color=color_,       # Color of the line
            width=1            # Width of the line
            )
    else:
        line_color_dict=dict(
            width=1            # Width of the line
            )
    fig.add_trace(
        go.Scatter(x=fake_x, y=magnitude, mode='lines', name=name + " - x" + str(scale),line = line_color_dict),
        row = 2*row+1, col=col+1,
    )
    
    # Adding Phase Plot to the specified subplot
    fig.add_trace(
        go.Scatter(x=fake_x, y=phase, mode='lines', name=name,line = line_color_dict),
        row=2*row+2, col=col+1
    )

def from_json_result_to_flatten_dict(json_file):
    number_of_if = len (json_file['array']['sis'])
    print ("number of IF: " + str(number_of_if))
    flat_dict_results = {}
    b = 0
    for baseline in json_file['data']:
        w = 0
        if baseline ==  None:
            print("redundant baseline ")
        else:
            for window in baseline:
                p = 0
                for polarization in window:
                    i = 0
                    for integration in polarization:
                        spectra = np.array([])
                        for channel in integration:
                            spectra = np.append(spectra,complex(channel[0],channel[1]))
                        IF_A = "A" + str(b//number_of_if)
                        IF_B = "-B" + str(b%number_of_if)
                        composed_name =  IF_A + IF_B + "-w" + format(w,'02') + "-p" +str(p) + "-i" + format(i,'02')
                        flat_dict_results[composed_name] = spectra
                        i+=1
                    p+=1
                w+=1
        b+=1
    return flat_dict_results

def from_json_result_to_nested_list(json_file):
    number_of_if = len (json_file['array']['sis'])
    print ("number of IF: " + str(number_of_if))
    b = []
    for baseline in json_file['data']:
        w = []
        if baseline ==  None:
            print("redundant baseline ")
        else:
            for window in baseline:
                p = []
                for polarization in window:
                    i = []
                    for integration in polarization:
                        spectra = np.array([])
                        for channel in integration:
                            spectra = np.append(spectra,complex(channel[0],channel[1]))
                        i.append(spectra)
                    p.append(i)
                w.append(p)
        b.append(w)
    return b

def get_IF_number(json_file):
    return len (json_file['array']['sis'])

def get_IF_tuple(baseline_numbrer,IF_number):
    return baseline_numbrer//IF_number, baseline_numbrer%IF_number

def get_subplot_names(IF_number):
    names = []
    bode = ['amp', 'phs']
    for i in range(IF_number+1):
            for j in range(IF_number):
                if i==j or (i-1) == j:
                    if i== j:
                        names.append("AUTO IF{} - IF{} - {}".format(i,j,'amp'))
                    else:
                        names.append("AUTO IF{} - IF{} - {}".format(IF_number -i,IF_number-j-1,'amp'))
                else:
                    if i<j:
                        names.append("CROSS IF{} - IF{} - {}".format(i,j,'amp'))
                    else: 
                        names.append("CROSS IF{} - IF{} - {}".format(IF_number -i,IF_number-j-1,'amp'))

            for j in range(IF_number):
                if i==j or (i-1) == j:
                    if i== j:
                        names.append("AUTO IF{} - IF{} - {}".format(i,j,'phs'))
                    else:
                        names.append("AUTO IF{} - IF{} - {}".format(IF_number -i,IF_number-j-1,'phs'))
                else:
                    if i<j:
                        names.append("CROSS IF{} - IF{} - {}".format(i,j,'phs'))
                    else:
                        names.append("CROSS IF{} - IF{} - {}".format(IF_number -i,IF_number-j-1,'phs'))
    return names

if __name__ == "__main__":
    ## Wrong results from 0 delay
    #json_path_ref = os.path.abspath("resources/all_impl/Strategy_optimized4_result_ref.json")
    #json_path_test = os.path.abspath("resources/all_impl/Strategy_optimized6_result_ref.json")
    #json_path_metrics = os.path.abspath("resources/random_normal/cmp_metrics.json")
    ## all random normal input
    #json_path_ref = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureTruth1GhzSin_StrategyOptimized4_results.json")
    #json_path_test = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureTruth1GhzSin_StrategyOptimized6_results.json")
    #json_path_metrics = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureTruth1GhzSin_cmp-metrics.json")
    ## sine 1 ghz experiment
    json_path_ref = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureRandom_StrategyOptimized4_results.json")
    json_path_test = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureRandom_StrategyOptimized6_results.json")
    json_path_metrics = os.path.abspath("resources/20240523_strategy4-6/StrategyFixtureRandom_cmp-metrics.json")
    print(json_path_ref)
    print(json_path_test)
    json_result_ref = load_json_file(json_path_ref)
    json_result_test = load_json_file(json_path_test)
    json_result_metrics = load_json_file(json_path_metrics)

    spectras_ref = from_json_result_to_flatten_dict(json_result_ref)
    spectras_test = from_json_result_to_flatten_dict(json_result_test)

    spectras_ref_list = from_json_result_to_nested_list(json_result_ref)
    spectras_test_list = from_json_result_to_nested_list(json_result_test)

    row_n = 12
    col_n = 6
    fig = make_subplots(rows=row_n, cols=col_n)
    count = 0
    """
    for baseline in spectras_ref:
        print(count)
        IFA = int(baseline.split("-")[0].replace("A",""))
        IFB = int(baseline.split("-")[1].replace("B","")) 
        if "p0-i00" in baseline:    
            add_bdplot_2_fig(fig, spectras_ref[baseline], IFA, IFB, 'ref'  )
            add_bdplot_2_fig(fig, spectras_test[baseline], IFA, IFB, 'tst')
            count+=1
    # Show the figure
    fig.show()
    """
    itg_figs = []
    subplot_titles_figs = []
    IF_number = get_IF_number(json_result_test)
    sub_plot_names = get_subplot_names(IF_number)
    b_fixed = 0
    for b in range(len(spectras_ref_list)):
        for w in range (len(spectras_ref_list[b])):
            for p in range (len(spectras_ref_list[b][w])):
                for i in range (len(spectras_ref_list[b][w][p])):
                    if len(itg_figs)<=i:
                        figure = go.Figure(make_subplots(rows = (IF_number+1)*2, cols = IF_number,subplot_titles=sub_plot_names))
                        fig.update_layout(title="w{}-i{}".format(w,i))
                        itg_figs.append(figure)
                        subplot_titles_figs.append([])
                    A,B = get_IF_tuple(b,IF_number)
                    try:
                        k = json_result_metrics['data'][b_fixed][w][p]['cross']['TP(A)/TP(B)'][i]
                        k = np.sqrt(k)
                        print(k)
                        k=1
                    except:
                        k = 1 
                        print("no scaling factor found")
                    if p:
                        add_bdplot_2_fig(itg_figs[i], spectras_ref_list[b][w][p][i] , A, B, 'ref', color_ = 'red')
                        add_bdplot_2_fig(itg_figs[i], spectras_test_list[b][w][p][i], A, B, 'tst', scale = k ,color_ = 'orange')
                    else:
                        add_bdplot_2_fig(itg_figs[i], spectras_ref_list[b][w][p][i], IF_number-A, IF_number-B -1, 'ref', color_= 'blue')
                        add_bdplot_2_fig(itg_figs[i], spectras_test_list[b][w][p][i], IF_number-A, IF_number-B -1 , 'tst', scale = k, color_= 'aqua' )
                        pass
                    subplot_titles_figs[i].append("IF{} - IF{}".format(A,B))
                    #add_bdplot_2_fig(itg_figs[i], spectras_test_list[b][w][p][i], row= IF_number-A+1, col= IF_number-B +1 )
        if len(spectras_ref_list[b]):
            b_fixed+=1
    
    itg_figs[0].update_layout(
    title={
        'text': 'Integration 0 - orange/red X pol - blut/sky Y pol - amp shows the scaling factor',
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 24,
            'color': 'black'
        }
    }
)
    itg_figs[0].show()
    itg_figs[1].show()
    #itg_figs[5].show()

    
#    for figure in itg_figs:
#        figure.show()

   # print (py.iplot(itg_figs[0]))