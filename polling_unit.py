import re


# These are hardcoded here rather than being introduced into the database to
# avoid having a huge number of duplicated codes in MapIt. As it is largely a
# presentation thing though I don't think it is too big an issue.
state_number_to_letter_mappings = {
    "1": "AB",
    "2": "AD",
    "3": "AK",
    "4": "AN",
    "5": "BA",
    "6": "BY",
    "7": "BE",
    "8": "BO",
    "9": "CR",
    "10": "DE",
    "11": "EB",
    "12": "ED",
    "13": "EK",
    "14": "EN",
    "15": "GO",
    "16": "IM",
    "17": "JI",
    "18": "KD",
    "19": "KN",
    "20": "KT",
    "21": "KE",
    "22": "KO",
    "23": "KW",
    "24": "LA",
    "25": "NA",
    "26": "NI",
    "27": "OG",
    "28": "ON",
    "29": "OS",
    "30": "OY",
    "31": "PL",
    "32": "RI",
    "33": "SO",
    "34": "TA",
    "35": "YO",
    "36": "ZA",
    "37": "FC",
}


def tidy_up_pun(pun):
    """
    Tidy up the query into something that looks like PUNs we are expecting

    # None returns empty string
    >>> tidy_up_pun(None)
    ''

    # Tidy up and strip as expected
    >>> tidy_up_pun("AB:01:23:45")
    'AB:1:23:45'
    >>> tidy_up_pun("AB--01::23 45")
    'AB:1:23:45'
    >>> tidy_up_pun("  AB--01::23 45  ")
    'AB:1:23:45'

    # Convert state numbers to state code, if found
    >>> tidy_up_pun("01:01:23:45")
    'AB:1:23:45'
    >>> tidy_up_pun("01")
    'AB'
    >>> tidy_up_pun("99:01:23:45")
    '99:1:23:45'
    """

    if not pun:
        pun = ""

    pun = pun.strip().upper()
    pun = re.sub(r'[^A-Z\d]+', ':', pun)  # separators to ':'
    pun = re.sub(r'^0+', '',  pun)  # trim leading zeros at start of string
    pun = re.sub(r':0+', ':', pun)  # trim leading zeros for each component

    # PUNs starting with a number shoud be converted to start with a state code
    if re.match(r'^\d', pun):
        state_number = pun.split(':')[0]
        state_code = state_number_to_letter_mappings.get(state_number,
                                                         state_number)
        pun = re.sub(r'^' + state_number, state_code, pun)

    return pun

# A regular expression to match any PUN after it's been tidied
pun_re = re.compile('''
    ^(
       [A-Z]{2}|
       [A-Z]{2}:\d+|
       [A-Z]{2}:\d+:\d+|
       [A-Z]{2}:\d+:\d+:\d+
    )$
''', re.VERBOSE)
