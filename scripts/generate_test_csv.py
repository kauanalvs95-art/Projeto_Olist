import csv
from faker import Faker

fake = Faker()

with open('authors_1m.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name'])

    for _ in range(1_000_000):
        writer.writerow([fake.name()])