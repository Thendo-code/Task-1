
import unittest
from mastermind import compare_codes

class TestMastermind(unittest.TestCase):

    def test_all_correct(self):
        self.assertEqual(compare_codes("RGBY", "RGBY"), (4, 0))

    def test_some_correct_some_correct_ish(self):
        self.assertEqual(compare_codes("RBYG", "RGBY"), (1, 3))

    def test_all_correct_ish(self):
        self.assertEqual(compare_codes("YRGB", "RGBY"), (0, 4))

    def test_some_correct(self):
        self.assertEqual(compare_codes("RGBO", "RGBY"), (3, 0))

    def test_no_matches(self):
        self.assertEqual(compare_codes('HFDS', "RGBY"), (0, 0))

if __name__== "__main__":
   unittest.main    