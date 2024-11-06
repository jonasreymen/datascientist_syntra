import csv
import os

file_path = os.getcwd() + '/muzikanten_data.csv'
data = []
headers = []

def get_headers() -> list:
    return tuple(headers)

def get_data() -> list[dict]:
    return data

def __hydrate_row(row: list):
    hydrated_row = {}
    for i, header in enumerate(get_headers()):
        hydrated_row[header] = row[i]
    return hydrated_row

def write_csv(modified_rows: list[dict]) -> str:
    """ write to CSV """
    modified_rows = [row.values() for row in modified_rows]
    
    export_path = os.getcwd() + "/updated.csv"
    with open(export_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(modified_rows)
    
    return export_path

def load():
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers.extend(next(reader))
        
        for row in reader:
            data.append(__hydrate_row(row))

load()