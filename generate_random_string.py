import random
import string

# random string
print("_"+"".join(random.choices(string.ascii_uppercase + string.digits, k=3)))

print("latitude: ", random.uniform(50, 54))
print("longitude: ", random.uniform(16, 23.5))


def geolocation(config) -> dict:
    geolocation = {"address": config["RSC"]["rsc_name"], "latitude": random.uniform(50, 54), "longitude": random.uniform(16, 23.5)}
    return geolocation

def suffix():
    return "_"+"".join(random.choices(string.ascii_uppercase, k=3))

def blob_name():
    return "blob_"+"".join(random.choices(string.ascii_lowercase, k=5))+".svg"

print(blob_name())