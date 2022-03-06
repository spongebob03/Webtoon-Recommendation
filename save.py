import csv

def save_file(toons):
    file = open("naver.csv", mode="w", encoding="UTF8")
    writer = csv.writer(file)
    writer.writerow(list(toons[0].keys()))
    for toon in toons:
        writer.writerow(list(toon.values()))
    
    return 0