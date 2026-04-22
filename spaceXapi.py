import requests
import pandas as pd
import BeautifulSoup


url = https://api.spacexdata.com/v4/launches/past
response = requests.get(url)
requestResponse = response.json()

data = pd.json_normalize(requestResponse)



