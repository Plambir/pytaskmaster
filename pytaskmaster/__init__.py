# -*- coding: utf-8 -*-

import time
import subprocess
import json
import os

from string import Template

def generator(in_file_name, out_file_name, config):
    template_string = ""
    with open(in_file_name, 'r') as in_file:
        template_string = in_file.read()
    template = Template(template_string)
    template = template.safe_substitute(config.get_dict())
    out_file_content = ""
    if os.path.isfile(out_file_name):
        with open(out_file_name, 'r') as out_file_read:
            out_file_content = out_file_read.read()
    if(out_file_content != template):
        with open(out_file_name, 'w') as out_file:
            out_file.write(template)


class Config:
    def __init__(self, name="master.json"):
        self._name = name
        self._config = dict()

    def set(self, key, value):
        self._config[key] = value

    def get(self, key, default=""):
        if key in self._config:
            return self._config[key]
        else:
            return default

    def set_default(self, key, value):
        if not key in self._config:
            self._config[key] = value

    def load(self):
        if os.path.isfile(self._name):
            with open(self._name, 'r') as configfile:
                self._config.update(json.load(configfile))

    def save(self):
        with open(self._name, 'w') as configfile:
            json.dump(self._config, configfile, indent=4)

    def get_dict(self):
        return self._config.copy()


def shell(command, ignore_code=False):
    print("Run: `{}`".format(command))
    code = subprocess.call(command, shell=True)
    if code and not ignore_code:
        exit(code)


def help(module):
    print("Tasks:")
    for key in module:
        if "task" in key.split("_") and len(key.split("_")) > 1:
            help_info = "  {}".format(key.split("_")[1])
            if module[key].__doc__:
                help_info = "{} -- {}".format(help_info, module[key].__doc__)
            print(help_info)


def _find_task(module, task_name):
    task = None
    if task_name in module:
        task = module[task_name]
    return task


def run(module, argv):
    """Find and run task

    Simple use:
        import sys
        run(globals(), sys.argv[1:])

    By default call task `help`
    """
    task_name = "task_{}".format(argv[0])
    task = _find_task(module, task_name)
    if task is None:
        return False
    task(argv[1:])
    return True


def bench(function):
    def bench_wrapper(*args, **kwargs):
        ts = time.time()
        result = function(*args, **kwargs)
        te = time.time()
        print('Done {}: {:F} sec'.format(function.__name__, float(te-ts)))
        return result
    return bench_wrapper


def main():
    __template="""# -*- coding: utf-8 -*-
import pytaskmaster

# Load config from `master.json`
config = pytaskmaster.Config()
config.set_default("VERSION", "1.0")
config.load()

def task_example(argv):
    '''It\'s example task'''
    # save config to `master.json`
    config.save()

def task_build(argv):
    '''It\'s example of use generator'''
    with open("build.txt.in", "w") as file:
        file.write("VERSION: $VERSION\\n")
    pytaskmaster.generator("build.txt.in", "build.txt", config)
   """
    def my_input():
        major_ver = sys.version_info[0]
        if major_ver == 2:
            return raw_input()
        else:
            return input()
    def choise(question, default_y=True):
        choise_str = "(Y/n)"
        if not default_y:
            choise_str = "(y/N)"
        print('"{}" {}: '.format(question, choise_str), end="")
        yes = ['y']
        no = ['n']
        if default_y:
            yes.append('')
        else:
            no.append('')
        choice = my_input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            choise(question, default_y)
    try:
        sys.path.append(os.getcwd())
        import master
        if len(sys.argv) <= 1 or not pytaskmaster.run(master.__dict__, sys.argv[1:]):
            print("Usage: master [OPTION...] TASK [ARGS_FOR_TASK...]")
            pytaskmaster.help(master.__dict__)
    except ImportError:
        print("Error: `master.py` no such file")
        if choise("Create `master.py` in `{}`?".format(os.getcwd())):
            with open("master.py", 'w') as file:
                file.write(__template)
