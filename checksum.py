import hashlib

file = 'command_definitions.py'

hasher = hashlib.md5()
with open(file, 'rb') as f:
    content = f.read()
    hasher.update(content)

print(hasher.hexdigest())