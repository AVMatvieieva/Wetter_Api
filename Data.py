import pandas as pd
#Täglichen Wetterdaten (Option 1)
def get_daily_data(data, avg):
    
    if not isinstance(data, dict):
        print("Hier ist etwas schief gelaufen!")
        return None
    indices = []
    temp = []
    
    for d in data["days"]:
        indices.append(f"{d["datetime"]}")
        temp.append(f"{d["temp"]}")
        
    df = pd.DataFrame(data = {f"{data["address"]}":temp}, index = indices)    
    
    if avg:
        df[f"{data['address']} [Mittel]"] = df[f"{data['address']}"].rolling(5).mean()
    
    return df

def get_hourly_data(data, avg):
    if not isinstance(data, dict):
        print("Hier ist etwas schief gelaufen!")
        return None
    
    indices = []
    temp = []
    
    for day in data["days"]:
        try:
            for hour in day["hours"]:
                indices.append(f"{day['datetime']} {hour['datetime']}")
                temp.append(hour["temp"])
        except KeyError as e:
            print(f"Schlüssel {e} existiert nicht in den Daten.")
    
    df = pd.DataFrame(data = {f"{data["address"]}":temp}, index = indices)  
    if avg:
        df[f"{data['address']} [Mittel]"] = df[f"{data['address']}"].rolling(24).mean()
    return df         