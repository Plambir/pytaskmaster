# -*- coding: utf-8 -*-

import subprocess

def shell(command):
    code = subprocess.call(command, shell=True)
    if code:
        exit(code)

def help(module):
    print("Tasks:")
    for key in module:
        if "task" in key.split("_"):
            help_info = key.split("_")[1]
            if module[key].__doc__:
                help_info = help_info + " -- " + module[key].__doc__
            print(help_info)

def _find_task(module, task_name):
    import types
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
    if len(argv) < 1:
        argv = ['help']
    task_name = "task_{}".format(argv[0])
    task = _find_task(module, task_name)
    if task is None:
        print("Task `{}` not found".format(task_name))
        task = _find_task(module, "task_help")
        if task is None:
            print("Please add `task_help`")
            print("def task_help(argv):")
            print('    print("Run: master <task> <args>")')
            print('    pytaskmaster.help(globals())')
            return False
    task(argv[1:])
    return True
