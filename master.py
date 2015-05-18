#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytaskmaster
from pytaskmaster import shell

config = pytaskmaster.Config()
config.set_default("version", "1.1.0")
config.load()
config.save()

def run_tests(python_command, argv):
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
    """Run `test [test_module...]` for running current module"""
    run_tests("python2", argv)
    run_tests("python3", argv)


def task_check(argv):
    shell("pylint")


@pytaskmaster.bench
def task_build(argv):
    """Build package. Use --sigh for create .asc files"""
    pytaskmaster.generator("setup.py.in", "setup.py", config)
    shell("python setup.py bdist_wheel")
    if "--sign" in argv:
        for file in os.listdir("dist"):
            asc_file = "dist/" + file + ".asc"
            if file.endswith(".whl") and not os.path.isfile(asc_file):
                shell("gpg --detach-sign -a dist/{}".format(file))


def task_install(argv):
    if shell("pip install --user --upgrade .", True):
        shell("pip install --user .")


def task_upload(argv):
    shell("twine upload dist/*-{0}-*".format(config.get('version')))
