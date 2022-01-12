import os


def normalise(file_root: str, path: str):
    return os.path.normpath(os.path.join(file_root, path))


def check_paths(branch, file_root):
    link = branch.link
    if link is not None and not link.startswith('http'):
        path = normalise(file_root, link)
        if not os.path.isfile(path):
            print('%s is missing from %s' % (path, branch.text))
    for br in branch.branches():
        check_paths(br, file_root)
