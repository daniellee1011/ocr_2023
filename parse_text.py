import re
from datetime import datetime

date_pattern = r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
# Extract year (A) and date (J)


def extract_date(text):
    """
    Extracts the year and date from the given text.

    Args:
        text (str): The text to extract the date from.

    Returns:
        tuple: A tuple containing the year (str) and date (str) in the format 'mm/dd/yyyy'.
    """
    date_match = re.search(date_pattern, text)
    if date_match:
        date = date_match.group(0)
        # check if the date is in the correct range
        dd = int(date.split()[0])
        if dd > 31:
            return date.split()[-1], 'N/A'

        try:
            date_obj = datetime.strptime(date, '%d %B %Y')
        except ValueError:
            date_obj = None

        if date_obj:
            # change to mm/dd/yyyy format
            formatted_date = date_obj.strftime('%m/%d/%Y')  # column J
            year = formatted_date[-4:]  # column A
        else:
            formatted_date = year = 'N/A'
    else:
        formatted_date = year = 'N/A'
        # print("No date found")
    return year, formatted_date


def remove_empty(text):
    """
    Removes empty spaces and newlines from the given text and returns 'N/A' if the resulting text is empty.

    Args:
        text (str): The text to remove empty spaces and newlines from.

    Returns:
        str: The cleaned text or 'N/A' if the resulting text is empty.
    """
    if not text:
        return 'N/A'
    cleaned_text = ' '.join(text.split())
    return cleaned_text if cleaned_text else 'N/A'


# read council list from text file and store in a list
with open('.\helper_data\council_list.txt', 'r') as f:
    council_list = [line.strip() for line in f]
council_tokens = [council.lower().split() for council in council_list]
# Extract council/committee name (B)


def extract_council(text):
    # print('extract_council function called')
    texts = text.lower().split('\n\n')
    for text in texts:
        # text_tokens = text.split(' ')
        text_tokens = re.split('\n| ', text)
        for council_token in council_tokens:
            if (len(set(council_token).intersection(set(text_tokens))) >= 2):
                return ' '.join(council_token).title()

    print("Council Name not found")
    return 'N/A'


with open('.\helper_data\committee_list.txt', 'r') as f:
    committee_list = [line.strip() for line in f]
committee_tokens = [committee.lower().split() for committee in committee_list]

# Extract committee/commission (D)


def extract_committee(text):
    """
    Extracts the committee/commission name from 'text' arguemnt

    Args:
        text (list): The text to extract the committee/commission from.

    Returns:
        String: the name of extracted committee/commission
    """
    texts = text.lower().split('\n\n')
    for text in texts:
        text_tokens = re.split('\n| ', text)
        # subtract 1 so we don't run out of index on the next line
        for i in range(len(text_tokens) - 1):
            pair = text_tokens[i:i+2]  # create a pair of consecutive tokens
            for committee_token in committee_tokens:
                # convert the committee_token list into a list of pairs for comparison
                committee_pairs = [committee_token[i:i+2]
                                   for i in range(len(committee_token) - 1)]
                if pair in committee_pairs:  # check if the pair of words from the text exists in the committee pairs
                    return ' '.join(committee_token).title()

    print("Committee Name not found")
    return 'N/A'


session_pattern = r'(?P<session>[\w-]+\s*session)'

# Extract session (D)


def extract_session(text):
    """
    Extracts the session information from the given text.

    Args:
        text (str): The text to extract the session information from.

    Returns:
        str: The extracted session information, or 'N/A' if not found.
    """
    match = re.search(session_pattern, text)
    if match:
        session = match.group("session")
    else:
        session = 'N/A'
        print("Session information not found.")
    return session


country_pattern = r'^[A-Za-z]+(, [A-Za-z]+)*( and [A-Za-z]+)?$'


def helper_extract_countries(text):
    """
    Extracts countries and footnotes from the given text.

    Args:
        text (list): The list of text lines to extract countries and footnotes from.

    Returns:
        tuple: A tuple containing countries (str) and footnotes (str).
    """
    footnote = ''
    countries = ''

    if len(text) == 1:
        countries = text[0]
        return countries, footnote

    for i in range(len(text)):
        part = text[i].replace('\n', ' ')
        match = re.search(country_pattern, part)
        temp = part.split(',')

        if part.isupper():
            footnote += part
        elif match:
            countries += ' '.join(text[i:])
            break
        elif len(temp) >= 3:
            countries += ' '.join(text[i:])
            break
        else:
            footnote += part
    return countries, footnote


agenda_pattern = r'Agenda item (\d+)(?: \((\w+)\))?(?:\n\n)?'
agendas_pattern = r'Agenda items (\d+ \(\w+\)? and \d+)'
sp_agenda_pattern = r'Item (\d+ ?)(?: \((\w+)\) ?)?of the provisional agenda'
draft_pattern = r':? *([\w ]*|[\n]*)? ?draft'


def extract_agenda_countries(text):
    """
    Extracts agenda item, agenda detail, countries, and footnotes from the given text.

    Args:
        text (str): The text to extract the information from.

    Returns:
        tuple: A tuple containing agenda item (str), agenda detail (str), countries (str), and footnotes (str).
    """
    single_agenda_match = re.search(agenda_pattern, text)
    multiple_agenda_match = re.search(agendas_pattern, text)
    special_agenda_match = re.search(sp_agenda_pattern, text)
    start_index = 0

    if single_agenda_match:
        agenda_item_number = single_agenda_match.group(1)
        agenda_item_letter = single_agenda_match.group(2)
        agenda_item = f"{agenda_item_number} ({agenda_item_letter})" if agenda_item_letter else agenda_item_number
        start_index = single_agenda_match.end()
    elif multiple_agenda_match:
        agenda_item = multiple_agenda_match.group(1)
        start_index = multiple_agenda_match.end()
    elif special_agenda_match:
        agenda_item_number = special_agenda_match.group(1)
        agenda_item_letter = special_agenda_match.group(2)
        agenda_item = f"{agenda_item_number} ({agenda_item_letter})" if agenda_item_letter else agenda_item_number
        start_index = special_agenda_match.end()
    else:
        print("Agenda not found")
        agenda_item = 'N/A'

    countries = 'N/A'
    footnote = 'N/A'
    agenda_detail = 'N/A'
    match3 = re.search(draft_pattern, text[start_index:], re.DOTALL)
    if match3:
        end_index = start_index + match3.start()
        content = text[start_index:end_index]
        parts = content.split("\n\n")
        parts = [s for s in parts if s != '']
        if len(parts) == 1:
            parts = content.split("\n")
        parts = [s for s in parts if s != '']
        agenda_detail = parts[0]
        remain_parts = parts[1:]
        for i in range(1, len(parts)):
            if parts[i].isupper():
                agenda_detail += parts[i]
            else:
                remain_parts = parts[i:]
                break
        countries, footnote = helper_extract_countries(remain_parts)
    else:
        print('Agenda match3 error')
        countries = 'N/A'
        footnote = 'N/A'
        agenda_detail = 'N/A'

    # print(agenda_detail)
    if 'UNITED\nNATIONS S' in agenda_detail:
        agenda_detail = 'N/A'

    return agenda_item, agenda_detail, countries, footnote


def split_text(text):
    """
    Splits the given text into two parts based on the draft_pattern.

    Args:
        text (str): The text to be split.

    Returns:
        tuple: A tuple containing the two parts of the split text.
    """
    # Delete extracted text
    split_text = re.split(draft_pattern, text)

    part1_text = split_text[0]
    part2_text = split_text[2:]
    part2_text = '\n\n'.join(part2_text)

    return part1_text, part2_text


number_title_pattern = r'^\s*(\d{4})?/?\W*(.*)'
draft_title_pattern = r'^Draft decision'


def extract_body_title(text):
    """
    Extracts body title number (G), body title (H), and body text from the given text.

    Args:
        text (str): The text to extract the information from.

    Returns:
        tuple: A tuple containing body title number (str), body title (str), and body text (str).
    """
    if text == '':
        return 'N/A', 'N/A', 'N/A'
    title_body_text = text.split('\n\n')
    title_text = title_body_text[1].replace('\n', ' ')
    title = 'N/A'
    title_number = 'N/A'
    idx = 1
    number_match = re.match(number_title_pattern, title_text)
    if number_match:
        match = re.match(draft_title_pattern, title_text)
        if match:
            title = title_body_text[2].replace('\n', ' ')
            idx = 3
        elif title_text and title_text[-1] != ',':
            title_number = number_match.group(1)
            title = number_match.group(2)
            idx = 2

    title_body_text = title_body_text[idx:]
    title_text = title_body_text[0]
    title_text = title_text.replace('\n', ' ')

    title = remove_empty(title)
    if len(title.split('/')) == 3:
        title = 'N/A'

    return title_number, title, title_body_text


def is_footnote(s):
    if s.strip().startswith('*'):
        return True
    if re.match(r'^\d+\s[^.]+$', s):
        return True

    return False


def is_not_body(s):
    # Generalized pattern to catch footnotes like E/CN.4/1999/L.3/Rev.1\npage 2
    if re.search(r'(?i)page\s+\d+$', s):
        return True

    if re.search(r'page \d+', s):
        return True

    # Check for patterns like * at the beginning, more generically
    if s.strip().startswith('*'):
        return True

    # Check for patterns like GE.99-12041 (E) or 99-02091 (E) 280199 /...
    if re.search(r'GE?\.\d{2}-\d{5} \(E\)', s) or re.search(r'\d{2}-\d{5} \(E\) \d{6} \/...', s):
        return True

    # Pattern like S/1999/79 English Page 2
    if re.search(r'S\/\d+\/\d+\s+English\s+Page \d+', s):
        return True

    # If the string is just whitespace or empty
    if s.strip() == '':
        return True

    # Pattern like /..
    if re.match(r'^\/\.\.$', s):
        return True

    # Pattern like 150199
    if re.match(r'^\d{6}$', s):
        return True

    # Pattern like '99-00881 (E)' and 'V.99-83730'
    # if re.match(r'^\d{2}-\d{5} \(E\).*', s):
    if re.match(r'^(?:[A-Z]\.)?\d{2}-\d{5}( \(E\))?.*$', s):
        return True

    # Pattern like 'A/C.3/54/L.17/Rev.1' and 'A/54/L.6'
    # if re.match(r'^[A-Z]/([A-Z]\.\d+/)?\d+/[A-Z]\.\d+(/Rev\.\d+)?$', s):
    if re.match(r'^[A-Z]/([A-Z]{1,2}\.\d+/)?\d+/[A-Z]\.\d+(/Rev\.\d+)?$', s):
        return True

    # Pattern like '2 Resolution 34/180, annex.' and '4 A/54/224'
    if re.match(r'^\d+\s.+$', s):
        return True

    return False


def extract_body(text_list):
    body_texts = [text for text in text_list if not is_not_body(text)]
    footnote_texts = [text for text in text_list if is_footnote(text)]

    body_text = '\n\n'.join(body_texts)
    footnote = '\n\n'.join(footnote_texts)

    return body_text, footnote
