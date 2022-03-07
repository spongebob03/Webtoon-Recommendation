import csv

def save_file(data, file_name):
    file = open(file_name+".csv", mode="w", encoding="UTF8")
    writer = csv.writer(file)
    writer.writerow(list(data[0].keys()))
    for toon in data:
        writer.writerow(list(toon.values()))
    
    return 0