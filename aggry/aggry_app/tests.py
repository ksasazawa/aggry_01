from django.test import TestCase

# Create your tests here.

import re

def remove_postal_code(address):
    address = address.replace('　', '').replace(' ', '')
    m = re.search(r'(市|区|町|村|郡)', address[4:])
    murayama = re.search(r'村山市', address)
    if '東京都' not in address or m is None:
        print("This item is not located in Tokyo")
    elif murayama:
        index = murayama.start() + 3
        return address[:index]
    elif m:
        index = m.start() + 5
        return address[:index]
    else:
        return address
    
# print(remove_postal_code('大田区豊南町'))
remove_postal_code('東京都大田区')