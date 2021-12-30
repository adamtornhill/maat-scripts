import unittest
import subprocess

class GitInteractionsTest(unittest.TestCase):
    def test_reproduce_problem(self):
        process_stdout = subprocess.Popen([ "echo", "first line\nsecond line" ], stdout=subprocess.PIPE).communicate()[0]
        
        lines = process_stdout.split("\n")
        self.assertEqual(1, len(lines))

if __name__ == '__main__':
    unittest.main()
