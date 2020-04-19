import requests

url = "https://amazon-price1.p.rapidapi.com/search"

querystring = {"keywords":"bikes","marketplace":"ES"}

headers = {
    'x-rapidapi-host': "amazon-price1.p.rapidapi.com",
    'x-rapidapi-key': "8b8b1523f5msh19d30ba49e79629p176612jsn8f3bef635c79"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)