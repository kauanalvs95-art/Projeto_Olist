import csv
from faker import Faker

with open('authors_1m.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name'])

    fake = Faker()
    for _ in range(1_000_000):
        name = fake.name()
        writer.writerow([name])