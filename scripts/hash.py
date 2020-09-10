import hashlib


def sha_3_hex_digest(input_string):
    """
    Given an input string a sha3 - 384 bit hex digest result
    :param input_string: string to hash
    :return: hexdigest string representation of input_string
    """
    encoded_input = input_string.encode("utf-8")
    return hashlib.sha3_384(encoded_input).hexdigest()