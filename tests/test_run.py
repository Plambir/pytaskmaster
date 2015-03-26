# -*- coding: utf-8 -*-

import unittest

import pytaskmaster

class TestRun(unittest.TestCase):
    @pytaskmaster.bench
    def test_find_task(self):
        def task_foo(argv):
            self.assertTrue(True)
            self.assertEqual(argv, "argv")
        def task_help(argv):
            self.assertTrue(False)
        def foo(argv):
            self.assertTrue(False)
        self.assertTrue(pytaskmaster.run_task(locals(), "foo", "argv"))

    @pytaskmaster.bench
    def test_not_find_task(self):
        def task_foo(argv):
            self.assertTrue(False)
        def foobar(argv):
            self.assertTrue(False)
        self.assertFalse(pytaskmaster.run_task(locals(), "foobar"))

    @pytaskmaster.bench
    def test_without_tasks(self):
        self.assertFalse(pytaskmaster.run_task(locals(), "foobar"))


if __name__ == "__main__":
    unittest.main()
