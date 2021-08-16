from hashlib import sha1


def encode_to_sha1(lang: str):
    if type(lang) != str:
        raise TypeError('Invalid language. Must be a string.')
    return sha1(lang.encode('utf-8')).hexdigest()
