from unittest import TestCase


class BaseTestCase(TestCase):

    def assertHasAttribute(self, attr: str, obj):
        self.assertEqual(True, attr in obj.__dict__)

    def assertNoAttribute(self, attr: str, obj):
        self.assertEqual(False, attr in obj.__dict__)
