from indicator import MovingAverage
import json
import pandas as pd

# Stream in
df = pd.read_json("data.json", convert_dates=False, convert_axes=False)
df = df.transpose()

# Initialize moving averages for both assets 24000 == ~6.6 hours
MA_A = MovingAverage(15000)
MA_B = MovingAverage(15000)

# Create position dictionary
positions = {
    "assetA": False,
    "assetB": False
}

# Create result list
result_dict = []

def strategy(row):
    # Calculate a mid price
    mid_A = (row[0]['ask'] + row[0]['bid']) /2
    mid_B = (row[1]['ask'] + row[1]['bid']) /2

    # Calculate spread
    spread_A = round(((row[0]['ask'] - row[0]['bid']) / row[0]['ask'])*100, 3)
    spread_B = round(((row[1]['ask'] - row[1]['bid']) / row[1]['ask'])*100,3)

    # Load into moving averages
    MA_A.update(mid_A)
    MA_B.update(mid_B)

    # check to see if enough data is in indicators/ Pass if not
    if(MA_A.current_avg is None) and (MA_A.current_avg is None):
        pass

    # Create actions list
    actions_list = []

    # strategy begin..
    if (MA_A.current_avg is not None) and (MA_B.current_avg is not None):  # Checks to see if enough data is loaded
        if (positions['assetA'] == False) and (mid_A < MA_A.current_avg):
            if (spread_A >= .05):
                actions_list.append("buyA")
                positions['assetA'] = True
        elif (positions['assetB'] == False) and (mid_B < MA_B.current_avg):
            if (spread_B >= .05):
                actions_list.append("buyB")
                positions['assetB'] = True
        elif (positions['assetA'] == True) and (mid_A > MA_A.current_avg):
            if (spread_A <= .0035):
                actions_list.append("sellA")
                positions['assetA'] = False
        elif (positions['assetB'] == True) and (mid_B > MA_B.current_avg):
            if (spread_B <= .0035):
                actions_list.append("sellB")
                positions['assetB'] = False

    # Return data if any
    if actions_list:
        result_dict.append({
            'time': row.name,          # Check if str is needed
            'actions': actions_list
        })

df.apply(strategy, axis=1)
with open("output.json", 'w+') as outfile:
    json.dump(result_dict, outfile)


