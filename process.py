import ocr_extraction as oe
import text2column as tc

# load util.txt from helper_data folder
with open('helper_data/util.txt', 'r') as f:
    util = f.read().split('\n')
    util = [i for i in util if i != '']
# get number after :
util = [i.split(':')[1] for i in util]
default_dpi = int(util[0])
higher_dpi = int(util[1])

# process to handle files from 1994 to 1997


def process9497(pdf_path, pdf_file, country_folder):
    # print('process9497 function called')
    pdf_text = oe.extract_text_from_pdf(pdf_path, default_dpi)
    text_columns = tc.text_to_column(pdf_text)
    row = text_columns[:-1] + [pdf_file[:-4], country_folder] + \
        text_columns[-1:]  # add column K and L
    return row

# process to handle files from 1998


def process98(pdf_path, pdf_file, country_folder):
    # print('process98 function called')
    global higher_dpi
    pdf_text_old = oe.extract_text_from_pdf(pdf_path, default_dpi)
    text_columns, part1_text = tc.text_to_column(pdf_text_old)

    # check if date was extracted correctly
    attempts = 0
    while text_columns[-2] == 'N/A' and attempts < 20:
        pdf_text_new = oe.extract_first_page_only(pdf_path, higher_dpi)
        _, date = tc.get_date_new(pdf_text_new)
        text_columns[-2] = date
        attempts += 1
        # add 1 to higher_dpi every 3 attempts
        if attempts % 3 == 0:
            higher_dpi += 3

    if attempts < 20 and attempts > 0:
        print(f"Get date in the {attempts}th attempt")
    elif attempts == 20:
        print(f"Get date failed with {attempts} attempts")
    row = text_columns[:-1] + [pdf_file[:-4], country_folder] + \
        text_columns[-1:]  # add column K and L
    return row, part1_text
