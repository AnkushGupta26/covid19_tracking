import requests
import json

respose = requests.get('https://api.covid19india.org/data.json')
total = respose.json()['statewise'][0]
totaltest = respose.json()['tested'][-1]

    