import csv
import sys

from sqlalchemy import insert

from app.database import SessionLocal
from app.models.author import Author
from app.models.book import Book  # noqa: F401  (precisa estar importado pro SQLAlchemy resolver a relação N:N)

BATCH_SIZE = 10_000


def import_authors(csv_path: str) -> int:
    db = SessionLocal()
    total = 0
    try:
        with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            batch = []

            for row in reader:
                batch.append({"name": row["name"]})

                if len(batch) >= BATCH_SIZE:
                    db.execute(insert(Author), batch)
                    db.commit()
                    total += len(batch)
                    batch = []

            if batch:  # sobra do último lote
                db.execute(insert(Author), batch)
                db.commit()
                total += len(batch)
    finally:
        db.close()

    return total


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python -m scripts.import_authors caminho/do/arquivo.csv")
        sys.exit(1)

    count = import_authors(sys.argv[1])
    print(f"{count} autores importados.")