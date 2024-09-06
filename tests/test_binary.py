import unittest

from zeraora.binary import randbytes


class BinaryTest(unittest.TestCase):

    def test_randbytes(self):
        for i in range(100):
            bytestream = randbytes(i)
            self.assertEqual(i, len(bytestream))
