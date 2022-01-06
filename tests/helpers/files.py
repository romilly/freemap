import os
import re
import subprocess

from hamcrest import assert_that, equal_to

TEST_DATA_DIRECTORY = 'data'


def test_file(file_name: str) -> str:
    return os.path.join(TEST_DATA_DIRECTORY, file_name)

TS_RE = re.compile(' (CREATED|MODIFIED)="\d*"')

def remove_timestmps(text: str):
    return TS_RE.sub('',text)


def assert_xml_equal(path1: str, path2: str, ignore_timestamps=True):
    f1 = canconicalize(path1)
    f2 = canconicalize(path2)
    if ignore_timestamps == True:
        f1 = remove_timestmps(f1)
        f2 = remove_timestmps(f2)
    if f1 != f2:
        for i in range(min(len(f1),len(f2))):
            if f1[i] != f2[i]:
                print('at %d' % i)
                print(f1[max(0,i-20):i+20])
                print(f2[max(0,i-20):i+20])
                break
    assert_that(f1, equal_to(f2))


def canconicalize(path1: str):
    r = subprocess.run(['xmllint',
                        '--exc-c14n',
                        path1],capture_output=True)
    if r.returncode != 0:
            raise ValueError('%s is not a valid XML file' % path1)
    return r.stdout.decode('utf-8')