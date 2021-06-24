import json
import statistics
import uvicorn
from fastapi import FastAPI
from itertools import groupby
from operator import itemgetter
from datetime import datetime

# create an app
app = FastAPI()

# route
@app.get("/v1/sensor_aggregation")
def main():
    with open('input/sensor_data.json', 'r') as f:        
        get_data = json.load(f)
        sensor_list = get_data['array']
        # add date field                        
        for data in sensor_list:                        
            sensor_date = datetime.fromtimestamp(data['timestamp']/1000.0).strftime('%d-%m-%y')
            data['date'] = str(sensor_date)                
        
        # groupby roomArea and date
        grouper = itemgetter('roomArea','date')
        sensor_list = sorted(sensor_list, key=grouper)
        output_dict = {}
        output_list = []
        for key, grp in groupby(sorted(sensor_list, key = grouper), grouper):            
            temp_dict = dict(zip(['roomArea','date'], key))                         
            temp_list = [[item["temperature"],item["humidity"]] for item in grp]                                         
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
        output_dict["datas"] = output_list
    return output_dict

if __name__ == "__main__":
    # start server
    uvicorn.run("problem2:app", host="127.0.0.1", port=7676)