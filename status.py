import csv
from datetime import datetime
import json

def convert_to_json(csv_file_path, json_file_path):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        # Convert each row into a dictionary and add it to data
        for rows in csv_reader:
            # Assuming a column named 'No' to be the primary key
            key = rows['OrderID']
            data[key] = rows

    # Open a json writer, and use the json.dumps() function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Method to fetch data based on date range
def get_data_sort_by_date(start_date, end_date):
    json_file_path = r'ShippingJson.json'
    filtered_data = []

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Convert start and end date to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        new_start = start.strftime("%Y/%m/%d")
        new_end = end.strftime("%Y/%m/%d")

        start = datetime.strptime(new_start, "%Y/%m/%d")
        end = datetime.strptime(new_end, "%Y/%m/%d")

        for key, record in data.items():
            order_date_str = record.get('OrderDate')
            order_date = datetime.strptime(order_date_str, "%m/%d/%y")

            # Format the datetime object to the new format (YY/MM/DD)
            formatted_date = order_date.strftime("%Y/%m/%d")

            record_date = datetime.strptime(formatted_date, "%Y/%m/%d")

            # Check if the record's date falls within the range
            if start <= record_date <= end:
                filtered_data.append(record)


    except Exception as e:
        print(f"File Exception Error: {e}")

    return filtered_data
