__author__ = 'Lambert Liu'

import unittest


class SMSTestCase(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)


if __name__ == '__main__':
    unittest.main()
