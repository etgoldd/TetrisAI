import csv

TABLE_NAME = "Data/TetrisPlayerScoreboardDB.csv"
fields = ["Index", "Name", "Score"]

if __name__ == "__main__":
    with open(f"../{TABLE_NAME}", encoding="utf-8", newline="", mode="x") as csvfile:
        csvwriter = csv.writer(csvfile, dialect="excel")
        csvwriter.writerow(fields)
