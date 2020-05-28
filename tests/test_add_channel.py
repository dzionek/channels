import unittest
from app import channel_has_invalid_name


class AddChannelTestCase(unittest.TestCase):
    def test_invalid_name(self):
        self.assertTrue(channel_has_invalid_name(''))
        self.assertTrue(channel_has_invalid_name(' leadingspace'))
        self.assertTrue(channel_has_invalid_name('trailingspace '))
        self.assertTrue(channel_has_invalid_name('@=)(%^'))
        self.assertTrue(channel_has_invalid_name('this illegal @ char is in the middle'))
        self.assertTrue(channel_has_invalid_name(' '))
        self.assertTrue(channel_has_invalid_name('Mytitle!'))

        self.assertFalse(channel_has_invalid_name('legal channel'))
        self.assertFalse(channel_has_invalid_name('a'))
        self.assertFalse(channel_has_invalid_name('A'))
        self.assertFalse(channel_has_invalid_name('AbcDeFgHiJkL'))
        self.assertFalse(channel_has_invalid_name('a b c d e f g h i j k l m'))
        self.assertFalse(channel_has_invalid_name('my_title'))
        self.assertFalse(channel_has_invalid_name('my-title'))


if __name__ == '__main__':
    unittest.main()
