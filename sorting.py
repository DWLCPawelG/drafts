from operator import itemgetter
import string
import random

my_list = [
    {'timestamp': 1568889841991, 'value': 47},
    {'timestamp': 1368889831991, 'value': 57},
    {'timestamp': 1468889862119, 'value': 77},
    {'timestamp': 1668889892219, 'value': 107}
]
# sortuj wg wartości timestampa
print(sorted(my_list, key=itemgetter("timestamp")))

# to samo można załatwić przez
print(sorted(my_list, key=lambda d: d["timestamp"]))

#random string
print("".join(random.choices(string.ascii_uppercase + string.digits, k=10)))
