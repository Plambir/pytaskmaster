# -*- coding: utf-8 -*-

import unittest

import pytaskmaster

class TestRun(unittest.TestCase):
    def test_find_task(self):
        def task_foo(argv):
            self.assertTrue(True)
        def task_help(argv):
            self.assertTrue(False)
        def foo(argv):
            self.assertTrue(False)
        self.assertTrue(pytaskmaster.run(locals(), ["foo"]))

    def test_not_find_task(self):
        def task_foo(argv):
            self.assertTrue(False)
        def task_help(argv):
            self.assertTrue(True)
        def foo(argv):
            self.assertTrue(False)
        self.assertTrue(pytaskmaster.run(locals(), ["foobar"]))

    def test_not_tasks(self):
        self.assertFalse(pytaskmaster.run(locals(), ["foobar"]))


