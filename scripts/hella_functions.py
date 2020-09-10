from scripts.hash import sha_3_hex_digest
from xml.dom.minidom import parseString
from xml.parsers.expat import ParserCreate, ExpatError, errors


def hash_file(xml_str):
    hashed_vin = __hash_vin(xml_str)
    hash_licence = __hash_licence(hashed_vin)
    return hash_licence


def __hash_vin(xml_str):
    try:
        doc = parseString(xml_str)
        vin = doc.getElementsByTagName("vin_car")[0]
        vin_value = vin.firstChild.data
        hash_string = xml_str.replace("<vin_car>{}</vin_car>".format(vin_value),
                                      "<vin_car>{}</vin_car>".format(sha_3_hex_digest(vin_value)))
        return hash_string
    except ExpatError:
        hash_string = xml_str
        return hash_string
    except IndexError:
        hash_string = xml_str
        return hash_string


def __hash_licence(xml_str):
    try:
        doc = parseString(xml_str)
        licence = doc.getElementsByTagName("licence")[0]
        licence_value = licence.firstChild.data
        hash_licence = xml_str.replace("<licence>{}</licence>".format(licence_value),
                                       "<licence>{}</licence>".format(sha_3_hex_digest(licence_value)))
        return hash_licence
    except ExpatError:
        hash_string = xml_str
        return hash_string
    except IndexError:
        hash_string = xml_str
        return hash_string
