def read(name: str):
    with open(name) as f:
        return f.read()

def write(text: str, path: str):
    with open(path, 'w') as tf:
        tf.write(text)