#POPULATE THE CSV WITH FORECASTED VALUES FROM METOFFICE, DAILY

import requests
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl

csv_columns = ('F.Date', 'F.Period', 'F.Hour (24)', 'F.Temp (C)', 'F.Feels Like (C)', 'F.Wind (MPH)', 'F.Wind Dir', 'F.Pressure (hPa)', 'F.Humidity (%)', 'F.Weather','F.Sky Condition', 'F.Location')
output_csv_rows = []

def f_period_generator(hour):
    if hour > 7 and hour < 22:
        return "Day"
    else:
        return "Night"
    

r = requests.get('https://www.metoffice.gov.uk/weather/forecast/u10j124jp#?nearestTo=E16%20(United%20Kingdom)')

soup = BeautifulSoup(r.content, "html.parser")
tmrw_dataset = soup.find_all("table")[1] #tmrw's table 

for i in range(0,24):

    f_wind_values = tmrw_dataset.find_all("tr")[9].find_all("td")[i].get_text("-", strip=True).split("-")

    output_csv_row_n = {
    csv_columns[0]  : (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), #forecast's date
    csv_columns[1]  : f_period_generator(i),
    csv_columns[2]  : tmrw_dataset.find(id = "d1t"+str(i)).get_text(strip=True).replace(":",""),
    csv_columns[3]  : tmrw_dataset.find_all("tr")[5].find_all("td")[i].get_text(strip=True).replace("Â°",""),
    csv_columns[4]  : tmrw_dataset.find_all("tr")[7].find_all("td")[i].get_text(strip=True).replace("Â°",""),
    csv_columns[5]  : f_wind_values[1],
    csv_columns[6]  : f_wind_values[0],
    csv_columns[7]  : "-",
    csv_columns[8]  : tmrw_dataset.find_all("tr")[15].find_all("td")[i].get_text(strip=True).replace("%",""),
    csv_columns[9]  : tmrw_dataset.find(id ="d1t"+str(i)+"Wx").img['title'],
    csv_columns[10] : "-",
    csv_columns[11] : "London City Airport, United Kingdom"
    }

    output_csv_rows.append(output_csv_row_n)

df = pd.DataFrame(output_csv_rows, columns = csv_columns) #list to a table, 
df.to_csv('weather_model_forecast_output.csv', encoding='utf-8',index=False, header=False, mode="a")
    
print(df)

output_csv_rows.clear()
del df




