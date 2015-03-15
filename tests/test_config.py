# -*- coding: utf-8 -*-

import unittest

import pytaskmaster

class TestConfig(unittest.TestCase):
    def setUp(self):
        test_json = '{"foo" : "bar"}'
        self.file_name = "test.json"
        with open(self.file_name, 'w') as open_file:
            open_file.write(test_json)

    def tearDown(self):
        import os
        os.remove(self.file_name)

    def test_config(self):
        config = pytaskmaster.Config()
        self.assertEqual(config.get("path", "/tmp"), "/tmp")
        self.assertEqual(config.get("path"), "")

    def test_config_default_value(self):
        config = pytaskmaster.Config()
        config.set_default("foo", "bar")
        self.assertEqual(config.get("foo"), "bar")
        config.set("moo", "boo")
        config.set_default("moo", "poo")
        self.assertEqual(config.get("moo"), "boo")

    def test_load(self):
        config = pytaskmaster.Config(self.file_name)
        self.assertEqual(config.get("foo"), "")
        config.load()
        self.assertEqual(config.get("foo"), "bar")

    def test_save(self):
        config = pytaskmaster.Config(self.file_name)
        config.set_default("foo", "moo")
        config.save()
        config_other = pytaskmaster.Config(self.file_name)
        self.assertEqual(config_other.get("foo"), "")
        config_other.load()
        self.assertEqual(config_other.get("foo"), "moo")

    def test_get_dict(self):
        config = pytaskmaster.Config(self.file_name)
        config.load()
        self.assertEqual(config.get_dict()["foo"], "bar")

if __name__ == "__main__":
    unittest.main()
