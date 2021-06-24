import requests
import json 
import uvicorn
from fastapi import FastAPI

# create an app
app = FastAPI()

# functions
def get_users():
    """
    This function is used to get user data
    """
    try:
        response = requests.get('http://jsonplaceholder.typicode.com/users', timeout=5)
        response.raise_for_status()    
        return response.json()    
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err    

def get_latest_usd():
    """
    This function is used to get the latest USD currency
    """
    try:        
        response = requests.get('https://v6.exchangerate-api.com/v6/60a39a6fce38b7c16c7325aa/latest/IDR', timeout=5)
        response.raise_for_status()    
        return response.json()['conversion_rates']['USD']   
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    except requests.exceptions.RequestException as err:
        return err  

# route
@app.get("/v1/salary_conversion")
def main():
    users = get_users()
    latest_usd = get_latest_usd()            
    output_list = []
    output_dict = {}    
    with open('input/salary_data.json', 'r') as f:        
        salary_list = json.load(f)        
        for salary in salary_list['array']:
            # Find matching id
            res = next((match_id for match_id in users if match_id['id'] == salary['id']), None)
            res['salaryInIDR'] = salary['salaryInIDR']
            res['salaryInUSD'] = salary['salaryInIDR'] * latest_usd
            # remove some keys
            res.pop('company')            
            res.pop('website')
            output_list.append(res)
        output_dict["datas"] = output_list
    return output_dict            
                
if __name__ == "__main__":
    # start server
    uvicorn.run("problem1:app", host="127.0.0.1", port=7676)