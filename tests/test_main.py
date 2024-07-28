import unittest
from src.main import WIDTH, HEIGHT

class TestConstants(unittest.TestCase):
    def test_width_is_positive_integer(self):
        self.assertIsInstance(WIDTH, int)
        self.assertGreater(WIDTH, 0)

    def test_height_is_positive_integer(self):
        self.assertIsInstance(HEIGHT, int)
        self.assertGreater(HEIGHT, 0)

    def test_width_and_height_are_different(self):
        self.assertNotEqual(WIDTH, HEIGHT)

if __name__ == '__main__':
    unittest.main()
