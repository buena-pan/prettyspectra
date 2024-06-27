import utils as u
import matplotlib.pyplot as plt
import numpy as np

# mse(TP(A),TP(B))/VAR
def check_some_cross_metric(cmp_metrics,metric,selector,do_print = True):
    total_counter = 0
    aux = []
    for b in range( len( cmp_metrics["data"] ) ):
        for w in range( len( cmp_metrics["data"][b] ) ):
            for p in range( len( cmp_metrics["data"][b][w] ) ):
                for i in range( len( cmp_metrics["data"] ) ):
                    tarjet_metric = cmp_metrics["data"][b][w][p][selector][metric][i]
                    cosa = "b{}-w{}-p{}-i{}: {}".format(b,w,p,i, tarjet_metric)
                    if do_print:
                        print(cosa)
                    aux.append(cosa)        
                    total_counter += 1
    print(total_counter)
    return aux
                    

print("=============================================")

#json_file = "resources/multi_spectral_w_test/StrategyFullRandomNormal_cmp-metrics.json"
json_file = "resources/progressive_channel_str3-6/StrategyFullRandomNormal_cmp-metrics.json"
#json_file = "resources/multi_spectral_w_test/StrategyFixtureRandom_cmp-metrics.json"
#json_file = "resources/multi_spectral_w_test/StrategyFixture1GhzSin_cmp-metrics.json"

json_object = u.load_json_file(json_file)
#flatten_dict = u.from_json_result_to_flatten_dict(json_object)

"""
for key in flatten_dict:
    if "p3" in key:
        print( "{} - len:{}".format(key,len(flatten_dict[key])) )
"""



bad_counter = 0
total_counter = 0
b_auto = [0,4,7,9]
#b_auto = []
data = np.array([])
for b in range( len( json_object["data"] ) ):
    print("=======")
    if b  not in b_auto:
        
        for w in range( len( json_object["data"][b] ) ):
            if w != 2:
                for p in range( len( json_object["data"][b][w] ) ):
                    for i in range( len( json_object["data"][b][w][p]["cross"]["mse(TP(A),TP(B))/VAR"] ) ):
                        #metric = json_object["data"][b][w][p]["test"]["sum_of_phases"][i]
                        #metric = json_object["data"][b][w][p]["cross"]["mse(TP(A),TP(B))/VAR"][i]
                        metric = json_object["data"][b][w][p]["test"]["total_power"][i]
                        data = np.append(data, metric)
                        if abs(metric ):
                        #if abs(metric - 0) > 1.25:
                        #if metric != 0:    
                            print( "b{}-w{}-p{}-i{}: {}".format(b,w,p,i, metric) )
                            bad_counter+=1
                        total_counter+=1
                        pass
                            
ratio_between = bad_counter/total_counter
print("number of bad results {}, over {}, ratio {}%".format(bad_counter,total_counter,ratio_between*100))

metric = json_object["data"][b][w][p]["test"]["total_power"][i]


#aux = check_some_cross_metric(json_object,"sum_of_phases","ref", do_print=False)
plt.figure()
plt.hist(data)
plt.show()
