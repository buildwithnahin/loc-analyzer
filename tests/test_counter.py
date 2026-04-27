import unittest
import os
import tempfile
from src.loc_analyzer.counter import count_lines, FileStats

class TestCounter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.py_file = os.path.join(self.test_dir.name, "test.py")
        with open(self.py_file, 'w') as f:
            f.write("def hello():\n    # Say hello\n    print('hello')\n\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_python_counting(self):
        stats = count_lines(self.py_file, '.py')
        self.assertEqual(stats.total_lines, 4)
        self.assertEqual(stats.blank_lines, 1)
        self.assertEqual(stats.comment_lines, 1)
        self.assertEqual(stats.code_lines, 2)
        self.assertEqual(stats.methods, 1)

if __name__ == '__main__':
    unittest.main()
