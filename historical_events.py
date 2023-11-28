import requests
from datetime import date
from config import YOUR_API_KEY

today = str(date.today())
year, month, day = today.split("-")
api_url = f'https://api.api-ninjas.com/v1/historicalevents?month={month}&day={day}'
response = requests.get(api_url, headers={'X-Api-Key': f'{YOUR_API_KEY}'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)

# reference: https://api-ninjas.com/api/historicalevents
