# -*- coding: utf-8 -*-

import unittest

import pytaskmaster

import os
import datetime
import time

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.in_file_name = "test.in.h"
        self.out_file_name = "test.h"
        test_template = "#define ${foo}"
        with open(self.in_file_name, 'w') as open_file:
            open_file.write(test_template)

    def tearDown(self):
        os.remove(self.in_file_name)
        os.remove(self.out_file_name)

    def test_generator(self):
        config = pytaskmaster.Config()
        config.set_default("foo", "bar")
        check_string = "#define bar"
        pytaskmaster.generator(self.in_file_name, self.out_file_name, config)
        out_file_content = ""
        with open(self.out_file_name, 'r') as open_file:
            out_file_content = open_file.read()
        self.assertEqual(out_file_content, check_string)
        out_file_time = modification_date(self.out_file_name)
        pytaskmaster.generator(self.in_file_name, self.out_file_name, config)
        self.assertEqual(out_file_time, modification_date(self.out_file_name))


if __name__ == "__main__":
    unittest.main()
