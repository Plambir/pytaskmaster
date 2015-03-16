#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytaskmaster
from pytaskmaster import shell

def run_tests(python_command, argv):
    """Run `test test_module [other_test_module...]` for running current module"""
    if len(argv) > 0:
        for arg in argv:
            shell("{} -m unittest tests.{}".format(python_command, arg), True)
    else:
        if python_command == "python2":
            shell("{} -m unittest tests".format(python_command), True)
        else:
            shell("{} -m unittest".format(python_command), True)


@pytaskmaster.bench
def task_test(argv):
    run_tests("python2", argv)
    run_tests("python3", argv)

def task_build(argv):
    shell("python setup.py bdist_wheel")
    if "--sign" in argv:
        for file in os.listdir("dist"):
            if file.endswith(".whl") and not os.path.isfile("dist/" + file + ".asc"):
                shell("gpg --detach-sign -a dist/{}".format(file))

def task_upload(argv):
    shell("twine upload dist/*")

def task_help(argv):
    """show this help"""
    print("Run: `master <task> <args>`")
    pytaskmaster.help(globals())

if __name__ == "__main__":
    pytaskmaster.run(globals(), sys.argv[1:])
