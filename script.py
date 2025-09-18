import requests
import os
from dotenv import load_dotenv
load_dotenv()
import csv

POLYGON_API_Key = os.getenv("POLYGON_API_Key")

LIMIT = 1000

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_Key}"
response = requests.get(url)

tickers =[]

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print('requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f"&apiKey={POLYGON_API_Key}")
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)

example_ticker = {'ticker': 'ZWS', 
                  'name': 'Zurn Water Solutions Corp', 
                  'market': 'stocks', 
                  'locale': 'us', 
                  'primary_exchange': 'XNYS', 
                  'type': 'CS', 
                  'active': True, 
                  'currency_name': 'usd', 
                  'cik': '0000912052', 
                  'composite_figi': 'BBG000C2V3D6', 'share_class_figi': 'BBG001S5N8V8', 'last_updated_utc': '2024-06-14T10:31:09Z'}

fieldnames = list(example_ticker.keys())
output_csv = 'tickers.csv'
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for ticker in tickers:
        row = {key: ticker.get(key, '') for key in fieldnames}
        writer.writerow(row)
print(f"Wrote {len(tickers)} rows to {output_csv}")
