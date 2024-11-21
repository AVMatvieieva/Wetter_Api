import requests
#All requests to the Timeline Weather API use the following the form: 
#https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/[location]/[date1]/[date2]?key=YOUR_API_KEY 
Base_Url ="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
key = 'LJVUK2UPEVZMQ7HRVXF3SRXPD'

class MaximumRequestsDone(Exception):
    pass
class UndefinedLocation(Exception):
    pass
class WrongApiKey(Exception):
    pass
class WrongDatum(Exception):
    pass

def fetch_data_for_city(city, start, end):
    try:
        url = f"{Base_Url}/{city}/{start}/{end}"
        params= {"key": key, 
                "unitGroup": "metric",
                "contentType": "json"}
        res = requests.get(url, params = params)
        return res.json()
    
    except ValueError as e:
        print(res.text)
        if "maximum number" in res.text:
            raise MaximumRequestsDone("Maximale Anzahl an Anfragen erreicht.")
        if "API key" in res.text:
            raise WrongApiKey("Ungültiger API-Schlüssel.")
        if "cannot be before" in res.text:
            raise WrongDatum("Falsches Datum: Startdatum liegt nach dem Enddatum.")
        if "Invalid location found." in res.text:
            raise UndefinedLocation(f"Ort {city} wurde nicht gefunden.")

    
#fetch_data_for_city("Berlin", "2022-12-01", "2022-12-01")    
