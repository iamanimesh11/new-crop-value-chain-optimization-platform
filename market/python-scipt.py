from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_prices/<selected_crop>/<selected_market>')


def get_prices(selected_crop, selected_market):
    base_url = "https://www.commodityinsightsx.com/commodities/mandi-prices/"

    url = f"{base_url}{selected_crop}-market-price-in-{selected_market}"

    print(url)


    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data from the first table
        first_table = soup.find('table', class_='table table-striped table-bordered')
        data_first = {}
        if first_table:
            rows = first_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    data_first[key] = value

        # Extracting data from the second table
        main_div = soup.find('div', class_='row cont mrkt-summary-table')
        data_second = {}
        if main_div:
            tables = main_div.find_all('table', class_='table table-striped table-bordered')
            if len(tables) > 1:
                second_table = tables[1]
                rows = second_table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        data_second[key] = value

        # Extracting data from the third table
        third_table = soup.find('div', id='priceTable')
        data_third = []
        if third_table:
            table = third_table.find('table',
                                     class_='table table-hover table-bordered table-responsive p-2 w-100 d-block d-md-table table-convertable-stack')
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cells = row.find_all('td')
                entry = {
                    "Arrival Date": cells[0].text.strip(),
                    "Commodity": cells[1].text.strip(),
                    "Variety": cells[2].text.strip(),
                    "Min Price": cells[3].text.strip(),
                    "Max Price": cells[4].text.strip(),
                    "Modal Price": cells[5].text.strip(),
                }
                data_third.append(entry)

        # Combine data from all three tables
        result = {
            "table1": data_first,
            "table2": data_second,
            "table3": data_third
        }

        return jsonify(result), 200

    return jsonify({"error": "Failed to retrieve the web page"}), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
