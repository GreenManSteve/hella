from xml.dom import minidom

hella_file = 'C:/Users/ross.humphrey/Projects/hella-ingester/resources/hella_example_files/hella_hashed_1.xml'


def mini_dom_read_file():
    """

    :return:
    """
    with open(hella_file, 'r') as x:
        doc = minidom.parseString(x)
        print(str(doc))


exact_match = {
    "Ablauf durch Benutzer abgebrochen.": "Failed",
    "Ablauf Grundeinstellung fehlerhaft.": "Passed",
}

prefix_match = {
    "Frontkamera konnte nicht kalibriert werden.": "Failed"
}
