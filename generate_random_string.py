import random
import string

# random string
print("".join(random.choices(string.ascii_uppercase + string.digits, k=10)))