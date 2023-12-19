from unittest import TestCase

from zeraora.defence import datasize, true


class DefenceTest(TestCase):

    def test_datasize(self):
        self.assertEqual(1, datasize('1B'))
        self.assertEqual(1.0, datasize('8b'))
        self.assertEqual(17 * 1000, datasize('17KB'))
        self.assertEqual(17 * 1024, datasize('17KiB'))
        self.assertEqual(17 * 1000 / 8, datasize('17Kb'))
        self.assertEqual(17 * 1024 / 8, datasize('17Kib'))
        self.assertEqual(29 * 1000 * 1000, datasize('29MB'))
        self.assertEqual(29 * 1024 * 1024, datasize('29MiB'))
        self.assertEqual(29 * 1000 * 1000 / 8, datasize('29Mb'))
        self.assertEqual(29 * 1024 * 1024 / 8, datasize('29Mib'))
        self.assertEqual(31 * 1000 * 1000 * 1000, datasize('31 GB'))
        self.assertEqual(31 * 1024 * 1024 * 1024, datasize('31 GiB'))
        self.assertEqual(31 * 1000 * 1000 * 1000 / 8, datasize('31 Gb'))
        self.assertEqual(31 * 1024 * 1024 * 1024 / 8, datasize('31 Gib'))
        self.assertEqual(0, datasize('47'))
        self.assertEqual(0, datasize('47KiBytes'))
        self.assertRaises(TypeError, datasize, 1024)

    def testMethod_true(self):
        self.assertTrue(true(True))
        self.assertTrue(true('True'))
        self.assertTrue(true('true'))
        self.assertTrue(true('TRUE'))
        self.assertTrue(true(1))
        self.assertTrue(true('1'))
        self.assertFalse(true(False))
        self.assertFalse(true('False'))
        self.assertFalse(true('false'))
        self.assertFalse(true('FALSE'))
        self.assertFalse(true(0))
        self.assertFalse(true('0'))
