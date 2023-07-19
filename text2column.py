from parse_text import (
    extract_date, extract_council, extract_session,
    extract_agenda_countries, split_text, extract_body_title,
    extract_body, remove_empty
)

def get_date_new(text):
    """
    Get the date from the text.
    
    Args:
        text (str): The input text to be classified.
        
    Returns:
        str: The date in the format of YYYY-MM-DD.
    """
    # Split based on : draft, which is the end of countries
    part1_text, _ = split_text(text)
    # Get year(A) and date(J)
    year, date = extract_date(part1_text)
    return year, date

# Function to classify text into column A to N
def text_to_column(text):
    """
    Classify the given text into columns A to N based on the extracted information.
    
    Args:
        text (str): The input text to be classified.
        
    Returns:
        list: A list containing the classified information in the following order:
            - year (A)
            - council/committee name (B)
            - session (C)
            - agenda item (D)
            - agenda detail (E)
            - countries (F)
            - title number (G)
            - title text (H)
            - body text (I)
            - date (J)
            - footnote (M)
    """

    result = []
    #print(text)

    # Split based on : draft, which is the end of countries
    part1_text, part2_text = split_text(text)
    # Get year(A) and date(J)
    #print('A,J')
    year, date = extract_date(part1_text)
    
    # Get council/committe name (B)
    #print('B')
    council = extract_council(part1_text)

    # Get session (C)
    #print('C')
    session = extract_session(part1_text)

    # Get agenda item (D), agend detail (E), and countries (F)
    #print('D, E, F')
    agenda_item, agenda_detail, countries, footnote1 = extract_agenda_countries(text)

    # Get title number (G) and title body (H)
    #print('G, H')
    title_number, title_text, body = extract_body_title(part2_text)

    # Get Body text (I) and footnote(M)
    #print('I, M')
    body_text, footnote2 = extract_body(body)
    footnote = footnote1 + footnote2

    # check body title is not 'The' only
    if title_text == 'The':
        title_text = 'N/A'
        body_text = 'The' + body_text
    
    # Add into result list
    result = [year, council, session, agenda_item, agenda_detail, countries, title_number, title_text, body_text, date, footnote]
    update_result = [remove_empty(_) for _ in result]
    return update_result
