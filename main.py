# import packages
import os
import time
import pandas as pd
import process as pB


# Path to the folder containing the PDF files
pdf_folder = './Dataset'
# Path to the folder where the CSV files will be saved
csv_folder = './csv_folder'
# csv file column list
column_list = ['year', 'Council', 'Committee', 'Session', 'Agenda item', 'Agenda detail', 'cosponsored countries',
               'body title number',	'body title detail', 'body text', 'date', 'file', 'filecountry', 'footnote', 'scanned']

# get input country name
input_country = input(
    "Start to processing files from Country: ") or "Afghanistan"

# Loop through each folder and PDF file and extract text
for country_folder in os.listdir(pdf_folder):
    # check if the country starts with the input country name
    if country_folder < input_country:
        continue
    # record the time to process each country
    times = []

    print('---------------' + country_folder + '---------------')
    if not os.path.isdir(os.path.join(pdf_folder, country_folder)):
        continue

    rows = []
    part1_texts = []
    part2_texts = []
    df = []
    # Loop through each file
    for pdf_file in os.listdir(os.path.join(pdf_folder, country_folder)):
        # calculate the time to process each file
        start_time = time.time()
        # check if the file is pdf
        if not pdf_file.endswith('.pdf'):
            continue

        # check if this file is old-version
        year = int(pdf_file.split('_')[0])

        # skip files before 1994 for now
        if year < 2001:
            continue

        if year >= 2002:  # targeted year should be stated as bigger, unless it is disaster
            df = pd.DataFrame(rows, columns=column_list)
            csv_path = os.path.join(
                csv_folder, f"{country_folder}_{year-1}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8')

            df_part1_texts = pd.DataFrame(part1_texts)
            if not os.path.exists('./raw_text_part1'):
                os.makedirs('./raw_text_part1')
            csv_path = os.path.join(
                './raw_text_part1', f'{country_folder}_part1_text_1999.csv')
            df_part1_texts.to_csv(csv_path, index=False, encoding='utf-8')

            df_part2_texts = pd.DataFrame(part2_texts)
            if not os.path.exists('./raw_text_part2'):
                os.makedirs('./raw_text_part2')
            csv_path = os.path.join(
                './raw_text_part2', f'{country_folder}_part2_text_1999.csv')
            df_part2_texts.to_csv(csv_path, index=False, encoding='utf-8')

            break

        pdf_path = os.path.join(
            pdf_folder, country_folder, pdf_file).replace('\\', '/')
        print(pdf_path)

        if year >= 1994 and year < 1998:
            row = pB.process9497(pdf_path, pdf_file, country_folder)
        else:  # targeted year should be stated, unless it is disaster
            row, part1_text, part2_text = pB.process98(
                pdf_path, pdf_file, country_folder)

        # check if year was extracted correctlys
        if row[0] != year:
            row[0] = year

        # scanned (N), cannot know
        if int(year) > 1994:
            scanned = 'yes'
        else:
            scanned = 'no'
        row.append(scanned)

        rows.append(row)
        part1_text = part1_text.split('\n\n')
        part1_texts.append(part1_text)

        part2_text = part2_text.split('\n\n')
        part2_texts.append(part2_text)
        # print the time to process each file in seconds, celling to 2 decimal places
        times.append(time.time() - start_time)
        # print("--- %s seconds ---" % round(time.time() - start_time, 2))

    # print the average time to process each file in seconds, celling to 2 decimal places
    print("Total files: " + str(len(times)) +
          " takes: " + str(sum(times)) + " seconds")
    try:
        print("--- Average %s seconds ---" % round(sum(times)/len(times), 2))
    except ZeroDivisionError:
        print("No times to calculate an average. Probably no files at this year.")

    try:
        print("--- NaN rate for date is: ",
              df['date'].isnull().sum()/len(df), " ---")
    except NameError:
        print("DataFrame df is not defined!")
    except TypeError:
        print("df is not a DataFrame or has other type-related issues!")

    print('---------------' + country_folder + '---------------')
