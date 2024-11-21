import streamlit as st 
import Api
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

from io import BytesIO 

from Data import get_hourly_data, get_daily_data

st.set_page_config(layout="wide")
sns.set_theme(style="whitegrid")

st.header("Unsere Wetter App!")
st.write("Hier kannst du die Temperatur an beliebigen Orten vergleichen!")

st.sidebar.header("Einstellungen")
avg = st.sidebar.checkbox("Gemittelte Temperatur anzeigen")

map = st.sidebar.checkbox("Weltkarte anzeigen")

cities = st.sidebar.text_input("Welche Städte interesieren dich?", placeholder="Schreib hier die Städte gefolgt von Leerzeichen")

date_start = st.sidebar.date_input("Startzeitpunkt") 
date_end = st.sidebar.date_input("Endzeitpunkt")

interval = st.sidebar.selectbox("Genauigkeit der Daten", ["Stunden", "Tagen"])

dataframe = []
gps = pd.DataFrame(columns=['lat', 'lon'])

col1, col2 = st.columns([2, 1])

with col1:
    
    if cities:
        for city in cities.split():
            try:
                # API-Anfrage für die Stadt
                data = Api.fetch_data_for_city(city, date_start, date_end)
            except Api.WrongApiKey:
                st.error("Fehlerhafter API-Schlüssel.")
                break
            except Api.UndefinedLocation:
                st.error(f"Ort {city} wurde nicht gefunden.")
                break
            except Api.MaximumRequestsDone:
                st.error("Maximale Anzahl an API-Anfragen erreicht. Bitte morgen erneut versuchen.")
                break
            except Api.WrongDatum:
                st.error("Fehlerhaftes Datum.")
                break

            if data is None:
                continue
            
            gps.loc[len(gps)] = [data["latitude"], data["longitude"]]
            
            if interval == "Stunden":
                df = get_hourly_data(data, avg)
            elif interval == "Tagen":
                df = get_daily_data(data, avg)
                
            dataframe.append(df)
                 
        fig, ax1 = plt.subplots(figsize = (6,6))
        for d in dataframe:
            print(df.dtypes) 
            print(df.head())
            d = d.apply(pd.to_numeric, errors='coerce')
            d.plot(ax=ax1, ylabel="Temperatur [°C]", xlabel="Datum", rot=90, fontsize=8)
            
            if interval == "Stunden":
                ticks = range(0, len(d), 24)
            elif interval == "Tagen":
                ticks = range(0, len(d))
            ax1.set_xticks(ticks=ticks, labels=[s[5:10] for s in d.index[ticks]])    
        
        buf = BytesIO()
        fig.savefig(buf, format = "png")
        
        st.image(buf)       
        
with col2:
    if map:
        st.header("Weltkarte")
        st.map(gps)             