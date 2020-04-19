import requests
url = "https://currency-value.p.rapidapi.com/global/currency_rates"

# querystring = {"keywords":"bikes","marketplace":"US"}

headers = {

    'x-rapidapi-host': "currency-value.p.rapidapi.com",
    'x-rapidapi-key': "5f6997638bmsh0072972d1fcfa8bp129664jsn47872153a2b4"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)