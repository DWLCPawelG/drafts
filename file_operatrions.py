

import hashlib
import os
import random
import string
from pprint import pprint

from qalibs.cloud import Cloud
from restclients.cloud2 import get_cloud2_client_from_config


def size():
    return 1024 * 1024

def filename():
    return "blob_"+"".join(random.choices(string.ascii_lowercase, k=5))+".svg"
filename = filename()

def blob(size, filename):
    content = os.urandom(size)
    with open(filename, 'w+b') as file:
        print(content)
        file.write(content)
        print(f"Created blob.svg with size: {size} Bytes")
        return file
    # os.remove(filename)

blob = blob(size=size(), filename=filename)


with open('blob1.txt', 'wb') as f:
    f.seek(99999) # przestaw kursor na bajt numer 99999
    f.write("\0") # to dalej utworzy Ci tylko pusty plik