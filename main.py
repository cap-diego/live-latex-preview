# From argparse
from argparse import ArgumentParser

# Utils
import os
import time
from datetime import datetime
import logging
import subprocess


# Constants
PATH = os.getcwd()
FILE_NAME_DEFAULT='test.tex'
WRITING_PDF = False
FILE_PATH_DEFAULT = '{path}/{name_file}'.format(path=PATH, name_file=FILE_NAME_DEFAULT)
ERROR = False
WAS_MODIFIED = False

def write_pdf(file_name):
    WRITING_PDF = True
    print("Writing")
    res = subprocess.call(['pdflatex', '-halt-on-error', file_name])
    if res!=0:
        ERROR = True
    WRITING_PDF = False
    print("Finishing")


def get_last_modified_of(file_name):
    last_modified = os.stat(file_name).st_mtime
    return datetime.fromtimestamp(last_modified)

if __name__ == '__main__':
    parser = ArgumentParser(description='Arg: name of .tex file ')
    parser.add_argument('--name_tex_file', dest='name_tex_file', \
        help='The tex file to output pdf. Default: {}'.format(FILE_NAME_DEFAULT), \
        default=FILE_NAME_DEFAULT
    )
    args = parser.parse_args()
    file_name = args.name_tex_file
    last_modified = get_last_modified_of(file_name)

    while not ERROR:
        try:
            if not last_modified == get_last_modified_of(file_name):
                last_modified = get_last_modified_of(file_name)
                WAS_MODIFIED = True
            time.sleep(0.3)
            if WAS_MODIFIED:
                write_pdf(file_name)
                WAS_MODIFIED = False

        except KeyboardInterrupt:
            ERROR = True
