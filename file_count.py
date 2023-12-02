import os
import re
import csv


def count_files(dir):
    pdf_pattern = re.compile('\.pdf$')
    files = [f for f in os.listdir(dir) if os.path.isfile(
        os.path.join(dir, f)) and pdf_pattern.search(f)]
    scanned = [f for f in files if int(f[:4]) < 1993]
    typed = [f for f in files if int(f[:4]) > 1993]

    return len(files), len(scanned), len(typed)


def count_dirs_and_write_csv(dir, csv_path):
    dirs = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]

    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['country', 'scanned', 'digitalized', 'total'])

        for d in dirs:
            full_path = os.path.join(dir, d)
            total, scanned, typed = count_files(full_path)
            writer.writerow([d, scanned, typed, total])


def main(dir):
    csv_path = r"C:\Users\kauvo\Desktop\github\ocr_2023\stats.csv"
    count_dirs_and_write_csv(dir, csv_path)
    print(f"Data has been written to {csv_path}")


main(r"C:\Users\kauvo\Desktop\github\ocr_2023\Dataset")
