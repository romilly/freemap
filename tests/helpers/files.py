import os
import subprocess

TEST_DATA_DIRECTORY = 'data'


def test_file(file_name: str) -> str:
    return os.path.join(TEST_DATA_DIRECTORY, file_name)


def xml_equal(path1: str, path2: str):
    f1 = canconicalize(path1)
    f2 = canconicalize(path2)
    return f1 == f2


def canconicalize(path1: str):
    r = subprocess.run(['xmllint',
                        '--exc-c14n',
                        path1],capture_output=True)
    if r.returncode != 0:
            raise ValueError('%s is not a valid XML file' % path1)
    return r.stdout.decode('utf-8')