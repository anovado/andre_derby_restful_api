from flask_restful import Api
from blueprints import app, manager
import logging, sys
from logging.handlers import RotatingFileHandler

api = Api(app, catch_all_404s=True)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()
    except Exception as e:
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" %(app.root_path, '../storage/log/app.log'), maxBytes=10000, backupCount=10)
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.run(debug=False, host='0.0.0.0', port=5050)


# import requests

# url = "https://currency-value.p.rapidapi.com/global/currency_rates"

# payload = "{\n\t\"from\": \"USD\",\n    \"to\": \"HKD\"\n}"
# headers = {
#   'x-rapidapi-host': 'currency-value.p.rapidapi.com',
#   'x-rapidapi-key': '5f6997638bmsh0072972d1fcfa8bp129664jsn47872153a2b4',
#   'Content-Type': 'application/json'
# }

# response = requests.request("GET", url, headers=headers, data = payload)
# data = response.json()
# price = 15446
# data_list = data['currency_rates']
# rows = []
# for _, (ky, val) in enumerate(data_list.items()) :
#   rows.append('%s => %f' % (ky, price*data['currency_rates']['IDR']/val))


