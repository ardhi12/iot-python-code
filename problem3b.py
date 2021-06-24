import json
import statistics
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from itertools import groupby

# functions
def visualization(list_dict):
    # visualization    
    x = np.array(list(list_dict["sensors_average"].keys()))
    y = np.array(list(list_dict["sensors_average"].values()))    
    rooms = [x["roomArea"] for x in list_dict["datas"]]
    min_temp = [x["min_temp"] for x in list_dict["datas"]]
    max_temp = [x["max_temp"] for x in list_dict["datas"]]
    min_hum = [x["min_hum"] for x in list_dict["datas"]]
    max_hum = [x["max_hum"] for x in list_dict["datas"]]
    
    # Create 3x3 sub plots
    gs = gridspec.GridSpec(3, 3)        
    plt.figure()    
    plt.subplot(gs[0, :])         
    plt.plot(rooms, min_temp, label = "min")        
    plt.plot(rooms, max_temp, label = "max")            
    plt.title('Temperature')        
    plt.legend()            
    
    plt.subplot(gs[1, :]) 
    plt.plot(rooms, min_hum, label = "min")        
    plt.plot(rooms, max_hum, label = "max")            
    plt.title('Humidity')        
    plt.legend()        

    plt.subplot(gs[2, :]) 
    plt.bar(x,y)    
    plt.title('Average sensors')    
    plt.suptitle("My Dashboard Visualization")
    plt.tight_layout(pad=1.0)    
    plt.show(block=False)  
    plt.pause(900)
    plt.close("all")    

def key_func(k):
    """
    This function is used to filter field as the key for the sorted function
    """
    return k['roomArea']
  
def main():
    with open('output/logs.json', 'r') as f:        
        get_data = json.load(f)
        sensor_list = get_data['logs']                      
        output_dict = {}
        output_list = []
        temp_dict = {}
        sensor_list = sorted(sensor_list, key=key_func)
        # group by roomArea
        for key, value in groupby(sensor_list, key_func):            
            temp_dict["roomArea"] = key
            temp_list = [[item["temperature"],item["humidity"]] for item in value]                                                     
            # aggregation
            temp_dict["min_temp"] = min(x[0] for x in temp_list)
            temp_dict["max_temp"] = max(x[0] for x in temp_list)
            temp_dict["median_temp"] = statistics.median(x[0] for x in temp_list)
            temp_dict["avg_temp"] = statistics.mean(x[0] for x in temp_list)
            temp_dict["min_hum"] = min(x[1] for x in temp_list)            
            temp_dict["max_hum"] = max(x[1] for x in temp_list)
            temp_dict["median_hum"] = statistics.median(x[1] for x in temp_list)
            temp_dict["avg_hum"] = statistics.mean(x[1] for x in temp_list)            
            output_list.append(temp_dict.copy())                        
        # average sensors value from all rooms
        all_avg_temp = statistics.mean(x["avg_temp"] for x in output_list)
        all_avg_hum = statistics.mean(x["avg_hum"] for x in output_list)        
        output_dict["datas"] = output_list
        output_dict["sensors_average"] = {"temperature": all_avg_temp, "humidity": all_avg_hum}            

    # create visualization    
    visualization(output_dict)
    
if __name__ == "__main__":
    while True:
        main()
        