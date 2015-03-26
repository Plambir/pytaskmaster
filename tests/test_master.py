# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import subprocess
import pipes
import tempfile

import pytaskmaster

help_origin = """usage: master [-h] [-s] [-f FILE] [-t] [TASK] ...

Run task from script file.

positional arguments:
  TASK                  task for run
  args                  args for task

optional arguments:
  -h, --help            show this help message and exit
  -s, --show-tasks      show all tasks from master file
  -f FILE, --file FILE  use custom FILE for run tasks
  -t, --template        create `master.py` from template
"""

master_test = """
def task_master(argv):
    pass
"""

master_test_show = """Tasks:
  master
"""

example_test = """
def task_example(argv):
    pass
"""

example_test_show = """Tasks:
  example
"""


class TestMaster(unittest.TestCase):
    def setUp(self):
        path = os.pathsep \
               + os.path.abspath(os.path.dirname(__file__)) \
               + "bin"
        os.environ["PATH"] += path
        self.test_dir = "tmp_test"
        self.old_cwd = os.getcwd()
        os.mkdir(self.test_dir)
        os.chdir(self.test_dir)
        os.mkdir("dir")
        self.file_name_master = "master.py"
        self.file_name_example = "example.py"
        with open(self.file_name_master, 'w') as open_file:
            open_file.write(master_test)
        with open(self.file_name_example, 'w') as open_file:
            open_file.write(example_test)
        with open("dir/" + self.file_name_example, 'w') as open_file:
            open_file.write(example_test)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_help_message(self):
        self.assertEqual(self._popen("master"), help_origin)

    def _popen(self, command):
        master = os.popen(command)
        output = master.read()
        master.close()
        return output;

    def _call(self, command):
        stdout = tempfile.TemporaryFile()
        stderr = tempfile.TemporaryFile()
        code = subprocess.call(command, shell=True, stdout=stdout, stderr=stderr)
        stdout.close()
        stderr.close()
        return code

    def test_show_tasks(self):
        self.assertEqual(self._popen("master -s"), master_test_show)

    def test_show_tasks_another_file(self):
        self.assertEqual(self._popen("master -f example.py -s"), example_test_show)
        self.assertEqual(self._popen("master -f dir/example.py -s"), example_test_show)

    def test_run_task(self):
        self.assertEqual(self._call("master master"), 0)

    def test_run_task_another_file(self):
        self.assertEqual(self._call("master -f example.py example"), 0)
        self.assertEqual(self._call("master -f dir/example.py example"), 0)

    def test_create_template(self):
        old_cwd = os.getcwd()
        os.chdir("dir")
        self.assertFalse(os.path.isfile("master.py"))
        self.assertEqual(self._call("master -t"), 0)
        self.assertTrue(os.path.isfile("master.py"))
        os.chdir(self.old_cwd)


if __name__ == "__main__":
    unittest.main()
