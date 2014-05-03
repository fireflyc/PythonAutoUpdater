#coding=utf-8
from ui import TkUI
from updater import Updater

__author__ = 'fireflyc'

import unittest
import os


class TestUpdater(unittest.TestCase):
    def setUp(self):
        self.updater = Updater("http://localhost/check.php")

    def test_check(self):
        self.updater.check()

    @staticmethod
    def next_file(remote_file):
        print "download file %s" % remote_file

    @staticmethod
    def download_progress(read_size, total_size):
        if total_size == 0:
            print "read size %d" % read_size
            return

        percent = float(read_size) / total_size
        print "read size %d of %d (%0.2f)" % (read_size, total_size, round(percent * 100, 2))

    def test_update(self):
        self.updater.check()
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        print cur_dir
        self.updater.update(cur_dir, self.next_file, self.download_progress)


class TestUI(unittest.TestCase):
    def test_tk(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.tk = TkUI(cur_dir, "http://localhost/check.php")
        self.tk.show()

cur_dir = os.path.dirname(os.path.abspath(__file__))
tk = TkUI(cur_dir, "http://localhost/check.php")
tk.show()